"""Type checker — Lit-Lift, Type-First decls, dimensional analysis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .ast_nodes import (
    Attr,
    BinOp,
    Call,
    Coin,
    CompilationUnit,
    Dirac,
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
    TupleExpr,
    TypeRef,
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
)


@dataclass(frozen=True, slots=True)
class Ty:
    """Runtime/static type: State wrapper, Classical scalar, + physical dimension."""

    kind: str  # "State" | "Classical"
    payload: str  # Int, Float, Length, Mass, …
    dim: Dim = DIMLESS

    def __str__(self) -> str:
        if self.kind == "Classical":
            return f"Classical<{self.payload}>"
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

    def check_unit(self, unit: CompilationUnit) -> list[dict]:
        if unit.main is None:
            return self.diagnostics
        for p in unit.main.params:
            if p.ty is not None:
                self.env[p.name] = self._ty_from_ref(p.ty)
            else:
                self.env[p.name] = Ty("State", "Any", DIMLESS)

        for stmt in unit.main.body.stmts:
            if isinstance(stmt, StateBind):
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
                inferred = self._infer(stmt.expr)
                if stmt.ty is not None:
                    declared = self._ty_from_ref(stmt.ty)
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
        if ty.kind not in {"State", "Classical"}:
            self.diagnostics.append(
                {
                    "code": "TYPE_NOT_STATE",
                    "line": line,
                    "col": col,
                    "message": f"{what} has non-State type {ty}",
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
            return Ty("State", "Int", DIMLESS)
        if isinstance(expr, Vacuum):
            return Ty("State", "Any", DIMLESS)
        if isinstance(expr, Dirac):
            inner = self._infer(expr.arg)
            return Ty("State", inner.payload, inner.dim)
        if isinstance(expr, KetLit):
            return Ty("State", "Int", DIMLESS)
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
        return Ty("State", "Any", DIMLESS)

    def _infer_attr(self, expr: Attr) -> Ty:
        obj_ty = self._infer(expr.obj)
        # Unit suffix: 0.05.s / 1.0.kg
        if isinstance(expr.obj, (LitInt, LitFloat)) and expr.name in UNIT_TABLE:
            payload, dim = UNIT_TABLE[expr.name]
            return Ty("State", payload, dim)
        # Math.sin etc. handled via Call(Attr(...)); bare attr → opaque
        return Ty("State", obj_ty.payload, obj_ty.dim)

    def _infer_binop(self, expr: BinOp) -> Ty:
        left = self._infer(expr.lhs)
        right = self._infer(expr.rhs)
        # expect() result is classical — must not mix into quantum coordinates
        if left.kind == "Classical" or right.kind == "Classical":
            if left.kind == "State" or right.kind == "State":
                self.diagnostics.append(
                    {
                        "code": "EXPECT_CLASSICAL_ONLY_ERROR",
                        "line": expr.span.line,
                        "col": expr.span.col,
                        "message": (
                            "cannot mix `expect` classical scalar with quantum State "
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
            self._infer(expr.callee.obj)
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
