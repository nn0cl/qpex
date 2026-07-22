"""Type checker — Lit-Lift, Type-First decls, dimensional analysis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .ast_nodes import (
    AssignStmt,
    Attr,
    BinOp,
    Call,
    ClassDecl,
    Coin,
    CompilationUnit,
    Dirac,
    EnumDecl,
    EvolveExpr,
    Expr,
    Inspect,
    KetLit,
    Lambda,
    LitBool,
    LitFloat,
    LitInt,
    LitString,
    Measure,
    Pipe,
    Snapshot,
    StateBind,
    StructDecl,
    TensorExpr,
    TupleExpr,
    TypeRef,
    UnaryNot,
    Vacuum,
    Var,
    WhenExpr,
)
from .dimensions import (
    DIMLESS,
    TYPE_DIMS,
    UNIT_TABLE,
    Dim,
    dim_of_type_name,
    format_dim_mismatch,
    product_payload,
    split_product_payload,
)


@dataclass(frozen=True, slots=True)
class Ty:
    """Runtime/static type: State wrapper, Classical scalar, Operator, + physical dimension."""

    kind: str  # "State" | "Classical" | "Operator"
    payload: str  # Int, Float, Length, Mass, …
    dim: Dim = DIMLESS

    def __str__(self) -> str:
        if self.kind == "Classical":
            return f"Classical<{self.payload}>"
        if self.kind == "Operator":
            return f"Operator<{self.payload}>"
        if self.dim.is_dimensionless():
            return f"State<{self.payload}>"
        return f"State<{self.payload}>{self.dim}"


RELATIONAL = {"==", "!=", "<", "<=", ">", ">="}
ARITH = {"+", "-", "*", "/"}
TRIG_AND_TRANS = frozenset({"sin", "cos", "tan", "exp", "log", "cis"})


@dataclass
class TypedExpr:
    expr: Expr
    ty: Ty


class TypeChecker:
    def __init__(self) -> None:
        self.env: dict[str, Ty] = {}
        self.diagnostics: list[dict] = []
        self.typed: dict[int, Ty] = {}  # id(expr) → ty
        self.class_meta: dict[str, ClassDecl] = {}
        self._in_class: str | None = None  # qualified/simple name while checking methods

    def check_unit(self, unit: CompilationUnit) -> list[dict]:
        if unit.main is None:
            return self.diagnostics

        # ADR 0062: prelude classical constants (pi, …)
        from .stdlib.prelude import PRELUDE_CONSTANTS

        for name in PRELUDE_CONSTANTS:
            self.env[name] = Ty("Classical", "Float", DIMLESS)

        enum_names: set[str] = set()
        struct_names: set[str] = set()
        class_meta: dict[str, ClassDecl] = {}
        for d in unit.decls:
            if isinstance(d, EnumDecl):
                enum_names.add(d.qualified_name)
                enum_names.add(d.name)
            elif isinstance(d, StructDecl):
                struct_names.add(d.qualified_name)
                struct_names.add(d.name)
            elif isinstance(d, ClassDecl):
                class_meta[d.qualified_name] = d
                class_meta[d.name] = d
                self._in_class = d.qualified_name
                for m in d.methods:
                    self._check_method_assigns(m, d)
                self._in_class = None
        self.class_meta = class_meta

        for p in unit.main.params:
            if p.ty is not None:
                self.env[p.name] = self._ty_from_ref(p.ty)
            else:
                self.env[p.name] = Ty("State", "Any", DIMLESS)

        for stmt in unit.main.body.stmts:
            if isinstance(stmt, AssignStmt):
                self._check_assign_stmt(stmt, class_meta)
                continue
            if isinstance(stmt, StateBind):
                # Operator H = … — not a State coordinate (ADR 0041)
                if stmt.ty is not None and stmt.ty.name == "Operator":
                    for n in stmt.names:
                        self.env[n] = Ty("Operator", "Hamiltonian", DIMLESS)
                    continue
                # Enum / struct / class object binds
                if stmt.ty is not None:
                    tname = stmt.ty.name
                    if tname in enum_names:
                        if not self._expr_is_enum_variant(stmt.expr, tname, enum_names):
                            # Integer / float literals are never enum tags
                            if isinstance(stmt.expr, (LitInt, LitFloat, LitBool, LitString)):
                                self.diagnostics.append(
                                    {
                                        "code": "ENUM_TYPE_MISMATCH",
                                        "line": stmt.span.line,
                                        "col": stmt.span.col,
                                        "message": (
                                            f"cannot assign literal to enum `{tname}`; "
                                            f"use `{tname}.Variant`"
                                        ),
                                    }
                                )
                        for n in stmt.names:
                            self.env[n] = Ty("Enum", tname, DIMLESS)
                        continue
                    if tname in struct_names or tname in class_meta:
                        for n in stmt.names:
                            kind = "Struct" if tname in struct_names else "Object"
                            self.env[n] = Ty(kind, tname, DIMLESS)
                        continue
                    is_quantity = tname in TYPE_DIMS or tname in {
                        "State",
                        "Operator",
                        "Delta",
                        "Tuple",
                    }
                    if not is_quantity and (
                        "." in tname or (tname[:1].isupper() and "(" not in tname)
                    ):
                        for n in stmt.names:
                            self.env[n] = Ty("Object", tname, DIMLESS)
                        continue
                # Evolve working coords shadow seeds (names ← seed types) for body check.
                if isinstance(stmt.expr, EvolveExpr):
                    seed_tys = []
                    for name, seed in zip(stmt.names, stmt.expr.seeds):
                        st = self._infer(seed)
                        self.env[name] = st
                        seed_tys.append(st)
                    inferred = self._infer(stmt.expr)
                    # Pairwise dim match for tuple evolve results
                    if (
                        isinstance(stmt.expr.body, type(None)) is False
                        and stmt.expr.body is not None
                        and isinstance(stmt.expr.body.result, TupleExpr)
                        and len(stmt.names) == len(stmt.expr.body.result.items)
                    ):
                        for i, (name, item) in enumerate(
                            zip(stmt.names, stmt.expr.body.result.items)
                        ):
                            item_ty = self.typed.get(id(item)) or self._infer(item)
                            if i < len(seed_tys):
                                seed_ty = seed_tys[i]
                                if not seed_ty.dim.matches(item_ty.dim):
                                    self._dim_error(
                                        stmt.span.line,
                                        stmt.span.col,
                                        seed_ty.dim,
                                        item_ty.dim,
                                        "evolve-result",
                                    )
                                self.env[name] = Ty(
                                    "State", item_ty.payload, item_ty.dim
                                )
                                self._assert_is_state(
                                    self.env[name], stmt.span.line, stmt.span.col, name
                                )
                        continue
                    if stmt.ty is not None:
                        declared = self._ty_from_ref(stmt.ty)
                        self._check_assign(
                            declared, inferred, stmt.span.line, stmt.span.col
                        )
                        ty = declared
                    else:
                        ty = inferred
                    for n in stmt.names:
                        self.env[n] = ty
                        self._assert_is_state(ty, stmt.span.line, stmt.span.col, n)
                    continue
                # Product / tensor bind: (a, b) = left *|* right  or typed State<(A,B)> (a,b)=…
                if len(stmt.names) > 1 and self._bind_product_components(stmt):
                    continue
                inferred = self._infer(stmt.expr)
                if stmt.ty is not None:
                    declared = self._ty_from_ref(stmt.ty)
                    # Single name must not declare a product carrier (needs tuple bind)
                    if (
                        split_product_payload(declared.payload) is not None
                        and len(stmt.names) == 1
                    ):
                        self.diagnostics.append(
                            {
                                "code": "PRODUCT_BIND_ERROR",
                                "line": stmt.span.line,
                                "col": stmt.span.col,
                                "message": (
                                    f"product type {declared} requires tuple bind "
                                    f"`State<(…)> (a, b) = …`, not a single name"
                                ),
                            }
                        )
                    self._check_assign(declared, inferred, stmt.span.line, stmt.span.col)
                    ty = declared
                else:
                    ty = inferred
                for n in stmt.names:
                    self.env[n] = ty
                    self._assert_is_state(ty, stmt.span.line, stmt.span.col, n)
            elif isinstance(stmt, (Measure, Snapshot)):
                ty = self._infer(stmt.expr)
                self._assert_is_state(ty, stmt.span.line, stmt.span.col, "measure/snapshot")
        return self.diagnostics

    def _bind_product_components(self, stmt: StateBind) -> bool:
        """Split product/tensor into per-coordinate types. Returns True if handled."""
        names = stmt.names
        expr = stmt.expr
        declared_parts: list[str] | None = None
        if stmt.ty is not None:
            declared = self._ty_from_ref(stmt.ty)
            declared_parts = split_product_payload(declared.payload)
            if declared_parts is None:
                # Non-product annotation on multi-name → fall through (evolve already handled)
                return False
            if len(declared_parts) != len(names):
                self.diagnostics.append(
                    {
                        "code": "PRODUCT_ARITY_ERROR",
                        "line": stmt.span.line,
                        "col": stmt.span.col,
                        "message": (
                            f"product type has {len(declared_parts)} components, "
                            f"bind has {len(names)} names"
                        ),
                    }
                )
                return True

        if isinstance(expr, TensorExpr):
            left_ty = self._infer(expr.left)
            right_ty = self._infer(expr.right)
            if len(names) != 2:
                self.diagnostics.append(
                    {
                        "code": "PRODUCT_ARITY_ERROR",
                        "line": stmt.span.line,
                        "col": stmt.span.col,
                        "message": "`*|*` bind expects exactly two names `(a, b)`",
                    }
                )
                return True
            components = [
                Ty("State", left_ty.payload, left_ty.dim),
                Ty("State", right_ty.payload, right_ty.dim),
            ]
            product = Ty(
                "State",
                product_payload([c.payload for c in components]),
                DIMLESS,
            )
            self.typed[id(expr)] = product
            if declared_parts is not None:
                for name, part, comp in zip(names, declared_parts, components):
                    want = Ty("State", part, comp.dim)
                    self._check_payload_assign(want, comp, stmt.span.line, stmt.span.col)
                    self.env[name] = want
                    self._assert_is_state(want, stmt.span.line, stmt.span.col, name)
            else:
                for name, comp in zip(names, components):
                    self.env[name] = comp
                    self._assert_is_state(comp, stmt.span.line, stmt.span.col, name)
            return True

        # Multi-name with product annotation but non-tensor RHS (e.g. evolve seeds)
        if declared_parts is not None:
            inferred = self._infer(expr)
            inf_parts = split_product_payload(inferred.payload)
            for i, name in enumerate(names):
                payload = declared_parts[i]
                if inf_parts is not None and i < len(inf_parts):
                    got = Ty("State", inf_parts[i], DIMLESS)
                    want = Ty("State", payload, DIMLESS)
                    self._check_payload_assign(want, got, stmt.span.line, stmt.span.col)
                self.env[name] = Ty("State", payload, DIMLESS)
                self._assert_is_state(self.env[name], stmt.span.line, stmt.span.col, name)
            return True

        return False

    def _check_payload_assign(self, declared: Ty, inferred: Ty, line: int, col: int) -> None:
        if inferred.payload in {"Any", declared.payload}:
            return
        if declared.payload in {"Any", "Int"} and inferred.payload in {
            "Int",
            "Qubit",
            "Coin",
            "Position",
            "Any",
        }:
            # Discrete carriers are Int-compatible at MVP
            return
        if inferred.payload in {"Int", "Qubit", "Coin"} and declared.payload in {
            "Qubit",
            "Coin",
            "Int",
        }:
            return
        if inferred.payload in {"Int", "Position"} and declared.payload in {
            "Position",
            "Int",
        }:
            return
        self.diagnostics.append(
            {
                "code": "PRODUCT_TYPE_MISMATCH",
                "line": line,
                "col": col,
                "message": f"cannot assign {inferred} to declared {declared}",
            }
        )

    def type_of(self, expr: Expr) -> Ty | None:
        return self.typed.get(id(expr))

    def _ty_from_ref(self, ref: TypeRef) -> Ty:
        if ref.name == "State":
            if not ref.args:
                return Ty("State", "Any", DIMLESS)
            inner = ref.args[0]
            payload, dim = self._payload_dim_from_ref(inner)
            return Ty("State", payload, dim)
        if ref.name == "Delta":
            # Delta<Time> → same dim as Time (increment of that quantity)
            if not ref.args:
                return Ty("State", "Delta", DIMLESS)
            payload, dim = self._payload_dim_from_ref(ref.args[0])
            return Ty("State", f"Delta<{payload}>", dim)
        payload, dim = self._payload_dim_from_ref(ref)
        return Ty("State", payload, dim)

    def _payload_dim_from_ref(self, ref: TypeRef) -> tuple[str, Dim]:
        if ref.name == "Tuple":
            parts: list[str] = []
            for a in ref.args:
                p, _d = self._payload_dim_from_ref(a)
                parts.append(p)
            return product_payload(parts), DIMLESS
        if ref.name == "Delta" and ref.args:
            inner_p, inner_d = self._payload_dim_from_ref(ref.args[0])
            return f"Delta<{inner_p}>", inner_d
        if ref.name in TYPE_DIMS:
            return ref.name, TYPE_DIMS[ref.name]
        return ref.name, dim_of_type_name(ref.name)

    def _check_assign(self, declared: Ty, inferred: Ty, line: int, col: int) -> None:
        # Dimensionless numeric may not silently become a dimensioned quantity.
        if declared.dim.is_dimensionless() and inferred.dim.is_dimensionless():
            return
        if declared.dim.matches(inferred.dim):
            return
        # Allow Any/Float dimensionless only when declared is also dimensionless
        if inferred.payload == "Any" and inferred.dim.is_dimensionless():
            return
        self.diagnostics.append(
            {
                "code": "DIMENSION_MISMATCH_ERROR",
                "line": line,
                "col": col,
                "message": (
                    f"cannot assign {inferred} to declared {declared}: "
                    + format_dim_mismatch(declared.dim, inferred.dim, "=")
                ),
            }
        )

    def _assert_is_state(self, ty: Ty, line: int, col: int, what: str) -> None:
        if ty.kind not in {"State", "Classical", "Operator", "Object", "Enum", "Struct"}:
            self.diagnostics.append(
                {
                    "code": "TYPE_NOT_STATE",
                    "line": line,
                    "col": col,
                    "message": f"{what} has non-State type {ty}",
                }
            )

    def _expr_is_enum_variant(
        self, expr: Expr, enum_name: str, enum_names: set[str]
    ) -> bool:
        if not isinstance(expr, Attr):
            return False
        q = None
        if isinstance(expr.obj, Var):
            q = expr.obj.name
        elif isinstance(expr.obj, Attr):
            # Namespace.Enum.Variant — obj is Namespace.Enum
            parts: list[str] = []
            cur: Expr = expr.obj
            while isinstance(cur, Attr):
                parts.append(cur.name)
                cur = cur.obj
            if isinstance(cur, Var):
                parts.append(cur.name)
                q = ".".join(reversed(parts))
        return q is not None and q in enum_names

    def _check_assign_stmt(
        self, stmt: AssignStmt, class_meta: dict[str, ClassDecl]
    ) -> None:
        target = stmt.target
        if not isinstance(target, Attr):
            return
        # struct field write is always illegal; var class field OK
        if isinstance(target.obj, Var):
            recv_ty = self.env.get(target.obj.name)
            if recv_ty is not None and recv_ty.kind == "Struct":
                self.diagnostics.append(
                    {
                        "code": "IMMUTABLE_ASSIGNMENT_ERROR",
                        "line": stmt.span.line,
                        "col": stmt.span.col,
                        "message": (
                            f"struct `{recv_ty.payload}` fields are immutable"
                        ),
                    }
                )
                return
            if recv_ty is not None and recv_ty.kind == "Object":
                cls = class_meta.get(recv_ty.payload)
                if cls is not None:
                    mem = next(
                        (m for m in cls.members if m.name == target.name), None
                    )
                    if mem is not None and not mem.mutable:
                        self.diagnostics.append(
                            {
                                "code": "IMMUTABLE_ASSIGNMENT_ERROR",
                                "line": stmt.span.line,
                                "col": stmt.span.col,
                                "message": (
                                    f"field `{target.name}` is `val` (immutable)"
                                ),
                            }
                        )

    def _check_method_assigns(self, method, cls: ClassDecl) -> None:
        # `fun init` may assign `val` fields once (constructor initialization).
        if method.name == "init":
            return
        mutable = {m.name for m in cls.members if m.mutable}
        for stmt in method.body.stmts:
            if not isinstance(stmt, AssignStmt):
                continue
            t = stmt.target
            if not isinstance(t, Attr):
                continue
            if isinstance(t.obj, Var) and t.obj.name == "this":
                if t.name not in mutable:
                    self.diagnostics.append(
                        {
                            "code": "IMMUTABLE_ASSIGNMENT_ERROR",
                            "line": stmt.span.line,
                            "col": stmt.span.col,
                            "message": (
                                f"field `{t.name}` is not `var` "
                                f"(cannot assign through `this`)"
                            ),
                        }
                    )

    def check_access_bounds(
        self,
        *,
        visibility: str,
        name: str,
        decl_package: list[str] | None,
        use_package: list[str] | None,
        span_line: int,
        span_col: int,
        same_class: bool = False,
        is_subclass: bool = False,
        same_module: bool = True,
        same_file: bool = False,
    ) -> None:
        """ADR 0058 — static access control (`pub` / module / `_`)."""
        from .access import access_violation

        viol = access_violation(
            visibility=visibility,
            name=name,
            decl_package=decl_package,
            use_package=use_package,
            span_line=span_line,
            span_col=span_col,
            same_class=same_class,
            is_subclass=is_subclass,
            same_module=same_module,
            package_exported=True,
            same_file=same_file,
        )
        if viol is not None:
            self.diagnostics.append(viol)

    def _member_visibility(self, cls: ClassDecl | None, member: str) -> str:
        from .access import effective_member_visibility

        if cls is None:
            return effective_member_visibility(member, "module")
        for f in cls.members or []:
            if f.name == member:
                return effective_member_visibility(member, f.visibility)
        for m in cls.methods or []:
            if m.name == member:
                return effective_member_visibility(member, m.visibility)
        return effective_member_visibility(member, "module")

    def _check_external_member_access(
        self, recv_ty: Ty, member: str, span_line: int, span_col: int
    ) -> None:
        """Reject `_` / private members unless inside the defining class."""
        from .access import is_underscore_private

        cls = self.class_meta.get(recv_ty.payload)
        if cls is None and recv_ty.kind not in {"Object", "Struct"}:
            return
        same_class = False
        if self._in_class is not None and cls is not None:
            same_class = self._in_class in {cls.name, cls.qualified_name}
        if same_class:
            return
        vis = self._member_visibility(cls, member)
        if vis == "private" or is_underscore_private(member):
            self.diagnostics.append(
                {
                    "code": "PRIVATE_ACCESS_VIOLATION_ERROR",
                    "line": span_line,
                    "col": span_col,
                    "message": (
                        f"cannot access private member `{member}` outside its class"
                    ),
                }
            )

    def _dim_error(self, line: int, col: int, left: Dim, right: Dim, op: str) -> None:
        self.diagnostics.append(
            {
                "code": "DIMENSION_MISMATCH_ERROR",
                "line": line,
                "col": col,
                "message": format_dim_mismatch(left, right, op),
            }
        )

    def _infer(self, expr: Expr) -> Ty:
        ty = self._infer_inner(expr)
        self.typed[id(expr)] = ty
        return ty

    def _infer_inner(self, expr: Expr) -> Ty:
        if isinstance(expr, LitInt):
            return Ty("State", "Int", DIMLESS)
        if isinstance(expr, LitFloat):
            return Ty("State", "Float", DIMLESS)
        if isinstance(expr, LitBool):
            return Ty("State", "Bool", DIMLESS)
        if isinstance(expr, LitString):
            return Ty("State", "String", DIMLESS)
        if isinstance(expr, Coin):
            return Ty("State", "Coin", DIMLESS)
        if isinstance(expr, Vacuum):
            return Ty("State", "Any", DIMLESS)
        if isinstance(expr, Dirac):
            inner = self._infer(expr.arg)
            return Ty("State", inner.payload, inner.dim)
        if isinstance(expr, KetLit):
            return Ty("State", "Qubit", DIMLESS)
        if isinstance(expr, Var):
            return self.env.get(expr.name, Ty("State", "Any", DIMLESS))
        if isinstance(expr, BinOp):
            return self._infer_binop(expr)
        if isinstance(expr, WhenExpr):
            self._infer(expr.ctrl)
            payloads: list[str] = []
            dims: list[Dim] = []
            for arm in expr.arms:
                t = self._infer(arm.body)
                payloads.append(t.payload)
                dims.append(t.dim)
            payload = payloads[0] if payloads else "Any"
            dim = dims[0] if dims else DIMLESS
            for i in range(1, len(payloads)):
                payload = _promote(payload, payloads[i])
                if not dim.matches(dims[i]) and not (
                    dim.is_dimensionless() and dims[i].is_dimensionless()
                ):
                    # when arms must share dimension
                    self._dim_error(
                        expr.span.line, expr.span.col, dim, dims[i], "when-arm"
                    )
            return Ty("State", payload, dim)
        if isinstance(expr, Call):
            return self._infer_call(expr)
        if isinstance(expr, Pipe):
            self._infer(expr.lhs)
            return self._infer(expr.rhs)
        if isinstance(expr, Lambda):
            self._infer(expr.body)
            return Ty("State", "Any", DIMLESS)
        if isinstance(expr, Attr):
            return self._infer_attr(expr)
        if isinstance(expr, Inspect):
            return self._infer(expr.expr)
        if isinstance(expr, TupleExpr):
            for it in expr.items:
                self._infer(it)
            return Ty("State", "Any", DIMLESS)
        if isinstance(expr, EvolveExpr):
            return self._infer_evolve(expr)
        if isinstance(expr, TensorExpr):
            left = self._infer(expr.left)
            right = self._infer(expr.right)
            return Ty(
                "State",
                product_payload([left.payload, right.payload]),
                DIMLESS,
            )
        if isinstance(expr, UnaryNot):
            # Open-control marker; carrier follows inner wire
            return self._infer(expr.expr)
        return Ty("State", "Any", DIMLESS)

    def _infer_attr(self, expr: Attr) -> Ty:
        # ADR 0062: Math.pi is classical Float (alias of prelude pi)
        if (
            isinstance(expr.obj, Var)
            and expr.obj.name == "Math"
            and expr.name == "pi"
        ):
            return Ty("Classical", "Float", DIMLESS)
        obj_ty = self._infer(expr.obj)
        # Unit suffix: 0.05.s / 1.0.kg
        if isinstance(expr.obj, (LitInt, LitFloat)) and expr.name in UNIT_TABLE:
            payload, dim = UNIT_TABLE[expr.name]
            return Ty("State", payload, dim)
        # `this.field` inside methods is same-class
        if isinstance(expr.obj, Var) and expr.obj.name == "this":
            if self._in_class is not None:
                cls = self.class_meta.get(self._in_class)
                vis = self._member_visibility(cls, expr.name)
                _ = vis  # allowed
            return Ty("State", obj_ty.payload, obj_ty.dim)
        self._check_external_member_access(
            obj_ty, expr.name, expr.span.line, expr.span.col
        )
        return Ty("State", obj_ty.payload, obj_ty.dim)

    def _infer_binop(self, expr: BinOp) -> Ty:
        left = self._infer(expr.lhs)
        right = self._infer(expr.rhs)
        # Classical scalars (`expect`, prelude `pi`, …) must not mix into State wires
        if left.kind == "Classical" or right.kind == "Classical":
            if left.kind == "State" or right.kind == "State":
                # Allow `pi / 2.0` / `2 * pi`: numeric literals are State-typed sugar
                lit_side = expr.rhs if left.kind == "Classical" else expr.lhs
                other = right if left.kind == "Classical" else left
                if (
                    isinstance(lit_side, (LitInt, LitFloat))
                    and other.payload in {"Int", "Float", "Any"}
                    and other.dim.is_dimensionless()
                ):
                    return Ty("Classical", "Float", DIMLESS)
                self.diagnostics.append(
                    {
                        "code": "TYPE_MISMATCH",
                        "line": expr.span.line,
                        "col": expr.span.col,
                        "message": (
                            "cannot mix classical Float (e.g. `pi` / `expect`) "
                            f"with quantum State via `{expr.op}` "
                            "(Never Leave the State / Born-rule boundary)"
                        ),
                    }
                )
                # Legacy alias still used by SV-18 / HARD_CODES
                self.diagnostics.append(
                    {
                        "code": "EXPECT_CLASSICAL_ONLY_ERROR",
                        "line": expr.span.line,
                        "col": expr.span.col,
                        "message": (
                            "cannot mix classical scalar with quantum State "
                            f"via `{expr.op}` (Born rule / Hilbert space confusion)"
                        ),
                    }
                )
            # Classical ⊕ Classical → classical float
            return Ty("Classical", "Float", DIMLESS)
        if expr.op in RELATIONAL:
            # Both sides must match; one-sided dimensionless bypass is banned
            if not left.dim.matches(right.dim):
                self._dim_error(
                    expr.span.line, expr.span.col, left.dim, right.dim, expr.op
                )
            return Ty("State", "Bool", DIMLESS)
        if expr.op in {"+", "-"}:
            if not left.dim.matches(right.dim):
                self._dim_error(
                    expr.span.line, expr.span.col, left.dim, right.dim, expr.op
                )
            payload = _promote(left.payload, right.payload)
            # Prefer dimensioned payload name when present
            if not left.dim.is_dimensionless():
                payload = left.payload if left.payload not in {"Int", "Float", "Any"} else right.payload
            return Ty("State", payload, left.dim)
        if expr.op == "*":
            dim = left.dim.mul(right.dim)
            payload = _payload_for_dim(dim, _promote(left.payload, right.payload))
            return Ty("State", payload, dim)
        if expr.op == "/":
            dim = left.dim.div(right.dim)
            payload = _payload_for_dim(dim, _promote(left.payload, right.payload))
            return Ty("State", payload, dim)
        return Ty("State", "Any", DIMLESS)

    def _infer_call(self, expr: Call) -> Ty:
        # Math.sin(x) / sin(x) / cis(theta): argument must be dimensionless
        op_name = _call_op_name(expr)
        for a in expr.args:
            at = self._infer(a)
            if op_name in TRIG_AND_TRANS and not at.dim.is_dimensionless():
                self.diagnostics.append(
                    {
                        "code": "DIMENSION_MISMATCH_ERROR",
                        "line": expr.span.line,
                        "col": expr.span.col,
                        "message": (
                            f"`{op_name}` requires a dimensionless argument, got {at.dim}"
                        ),
                    }
                )
        if isinstance(expr.callee, Attr):
            recv = self._infer(expr.callee.obj)
            if not (isinstance(expr.callee.obj, Var) and expr.callee.obj.name == "this"):
                self._check_external_member_access(
                    recv,
                    expr.callee.name,
                    expr.span.line,
                    expr.span.col,
                )
        elif not isinstance(expr.callee, Var):
            self._infer(expr.callee)
        # phase(src, theta): theta dimensionless
        if op_name == "phase" and len(expr.args) >= 2:
            th = self._infer(expr.args[1])
            if not th.dim.is_dimensionless():
                self.diagnostics.append(
                    {
                        "code": "DIMENSION_MISMATCH_ERROR",
                        "line": expr.span.line,
                        "col": expr.span.col,
                        "message": f"`phase` angle must be dimensionless, got {th.dim}",
                    }
                )
            if expr.args:
                return self._infer(expr.args[0])
        if op_name == "dirac" and expr.args:
            return self._infer(expr.args[0])
        if op_name == "expect":
            # ⟨O⟩ is a classical scalar — not a quantum State coordinate
            return Ty("Classical", "Float", DIMLESS)
        if op_name == "occupation":
            # |⟨k|ψ⟩|² Born weight — classical Float
            return Ty("Classical", "Float", DIMLESS)
        if op_name == "trace_out":
            # Discard named subsystem; remaining joint stays State (placeholder bind)
            if expr.args and isinstance(expr.args[0], Var):
                traced = expr.args[0].name
                # Drop traced coordinate from env knowledge for subsequent use
                # (bind name is Classical placeholder; other coords keep types)
                _ = traced
            return Ty("State", "Any", DIMLESS)
        return Ty("State", "Any", DIMLESS)

    def _infer_evolve(self, expr: EvolveExpr) -> Ty:
        seed_tys = [self._infer(s) for s in expr.seeds]
        if expr.hamiltonian is not None:
            self._infer(expr.hamiltonian)
            if expr.duration is not None:
                dt = self._infer(expr.duration)
                # Same rule as block evolve: Time / Delta<Time> / dimensionless phase
                if not (
                    dt.dim.matches(Dim(T=1))
                    or dt.dim.is_dimensionless()
                ):
                    self.diagnostics.append(
                        {
                            "code": "DIMENSION_MISMATCH_ERROR",
                            "line": expr.span.line,
                            "col": expr.span.col,
                            "message": (
                                f"`evolve … under H for` expects Time / Delta<Time> "
                                f"(or dimensionless angle), got {dt.dim}"
                            ),
                        }
                    )
            # Schrödinger evolve preserves qubit State payload
            return seed_tys[0] if seed_tys else Ty("State", "Int", DIMLESS)
        if expr.duration is not None:
            dt = self._infer(expr.duration)
            # Delta<Time> / Time / dimensionless step count
            if not (
                dt.dim.matches(Dim(T=1))
                or dt.dim.is_dimensionless()
            ):
                self.diagnostics.append(
                    {
                        "code": "DIMENSION_MISMATCH_ERROR",
                        "line": expr.span.line,
                        "col": expr.span.col,
                        "message": (
                            f"`evolve … for` expects Time / Delta<Time> "
                            f"(or dimensionless steps), got {dt.dim}"
                        ),
                    }
                )
        if expr.body is None:
            return seed_tys[0] if seed_tys else Ty("State", "Any", DIMLESS)
        for let in expr.body.lets:
            self.env[let.name] = self._infer(let.expr)
        return self._infer(expr.body.result)


def _call_op_name(expr: Call) -> str:
    from .ast_nodes import Attr, Var

    cal = expr.callee
    if isinstance(cal, Var):
        return cal.name
    if isinstance(cal, Attr):
        return cal.name
    return ""


def _payload_for_dim(dim: Dim, fallback: str) -> str:
    if dim.is_dimensionless():
        return fallback if fallback in {"Int", "Float", "Any"} else "Float"
    for name, d in TYPE_DIMS.items():
        if name in {"Int", "Float", "Bool", "String", "Any", "Angle", "Dimensionless"}:
            continue
        if d.matches(dim):
            return name
    return fallback


def _promote(a: str, b: str) -> str:
    if a == b:
        return a
    if {a, b} <= {"Int", "Float"}:
        return "Float"
    if a == "Any":
        return b
    if b == "Any":
        return a
    # Prefer physical payload over numeric
    if a in TYPE_DIMS and a not in {"Int", "Float", "Bool", "String", "Any"}:
        return a
    if b in TYPE_DIMS and b not in {"Int", "Float", "Bool", "String", "Any"}:
        return b
    return "Any"


def assert_expr_is_state(checker: TypeChecker, expr: Expr) -> bool:
    """Helper for harness assertTypeIsState against typed AST."""
    ty = checker.type_of(expr) or checker._infer(expr)
    return ty.kind == "State"


def lit_lift_demo(value: Any) -> Ty:
    if isinstance(value, bool):
        return Ty("State", "Bool", DIMLESS)
    if isinstance(value, int):
        return Ty("State", "Int", DIMLESS)
    if isinstance(value, float):
        return Ty("State", "Float", DIMLESS)
    if isinstance(value, str):
        return Ty("State", "String", DIMLESS)
    return Ty("State", "Any", DIMLESS)
