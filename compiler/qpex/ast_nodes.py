"""QPex AST nodes (design baseline subset for Phase 2.1)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Union

# Modern visibility (ADR 0058 revised):
#   public  — `pub` / `public` (cross-module API)
#   module  — default (same compilation module only)
#   private — leading `_` or legacy `private` keyword (class / same-file)
# Legacy alias: "package" is treated as "module" by access checks.
Visibility = Literal["public", "module", "private", "package"]


@dataclass
class Span:
    line: int
    col: int


# --- Expressions ---


@dataclass
class LitInt:
    value: int
    span: Span


@dataclass
class LitFloat:
    value: float
    span: Span


@dataclass
class LitBool:
    value: bool
    span: Span


@dataclass
class LitString:
    value: str
    span: Span


@dataclass
class Var:
    name: str
    span: Span


@dataclass
class Coin:
    span: Span


@dataclass
class Dirac:
    arg: "Expr"
    span: Span


@dataclass
class KetLit:
    """Dirac ket literal: `|0>`, `|+>`, `|01>`, … (ADR 0038)."""

    label: str
    span: Span


@dataclass
class Vacuum:
    span: Span


@dataclass
class BinOp:
    op: str  # + - * / == != < <= > >=
    lhs: "Expr"
    rhs: "Expr"
    span: Span


@dataclass
class Call:
    callee: "Expr"
    args: list["Expr"]
    span: Span


@dataclass
class WhenArm:
    pat: Any  # literal value or None for else
    body: "Expr"
    is_else: bool = False


@dataclass
class WhenExpr:
    ctrl: "Expr"
    arms: list[WhenArm]
    span: Span


@dataclass
class Pipe:
    lhs: "Expr"
    rhs: "Expr"
    span: Span


@dataclass
class Lambda:
    """Unary fn sugar: `x -> expr` (map / project)."""

    param: str
    body: "Expr"
    span: Span


@dataclass
class Attr:
    """Attribute / static path segment: `Math.sin` or `x.inspect`."""

    obj: "Expr"
    name: str
    span: Span


@dataclass
class Inspect:
    """Non-destructive debug view (ADR 0030); identity on joint."""

    expr: "Expr"
    label: str | None
    span: Span


@dataclass
class TupleExpr:
    """Product / simultaneous values: (x, p)."""

    items: list["Expr"]
    span: Span


@dataclass
class LetBind:
    """`let name = expr` inside evolve body."""

    name: str
    expr: "Expr"
    span: Span


@dataclass
class EvolveBody:
    lets: list[LetBind]
    result: "Expr"
    span: Span


@dataclass
class EvolveExpr:
    """Block evolve or Hamiltonian `evolve psi under H for t` (ADR 0038)."""

    seeds: list["Expr"]
    times: "Expr | int"  # Expr after ADR 0060; int kept for under/for default
    body: EvolveBody | None
    span: Span
    duration: "Expr | None" = None
    hamiltonian: "Expr | None" = None  # set for `under H`


@dataclass
class OpPauli:
    """Pauli atom: `X` / `Z(1)` inside Operator expressions."""

    kind: str  # I X Y Z
    site: int | None  # None → single-qubit / global
    span: Span


@dataclass
class OpNumber:
    """Number operator N on Fock levels."""

    span: Span


@dataclass
class OpQuadrature:
    """Position/momentum in truncated Fock: Q, P (ℏ=m=ω=1)."""

    kind: str  # Q | P
    span: Span


@dataclass
class OpGridQuad:
    """Deprecated alias node — grid uses bare X/P via context (ADR 0053)."""

    kind: str  # Xx | Px (legacy parse only)
    span: Span


@dataclass
class OpLit:
    """Scalar coefficient in an operator polynomial (multiplies identity)."""

    value: float
    span: Span


@dataclass
class OpBin:
    op: str  # + - *
    lhs: "OpExpr"
    rhs: "OpExpr"
    span: Span


@dataclass
class OpPow:
    base: "OpExpr"
    exp: int
    span: Span


@dataclass
class OpHop:
    """Tight-binding matrix unit `|i⟩⟨j|` on a discrete site basis (SSH / TB)."""

    i: int
    j: int
    span: Span


@dataclass
class OpVar:
    """Reference to a bound Operator name."""

    name: str
    span: Span


OpExpr = Union[
    OpPauli, OpNumber, OpQuadrature, OpGridQuad, OpHop, OpLit, OpBin, OpPow, OpVar
]


@dataclass
class TensorExpr:
    """State tensor product: `a *|* b` or `tensor(a, b)`."""

    left: "Expr"
    right: "Expr"
    span: Span


@dataclass
class UnaryNot:
    """Open-control polarity: `!c` in `capply(c0, !c1, X, t)` (ADR 0048)."""

    expr: "Expr"
    span: Span


@dataclass
class TypeRef:
    name: str
    args: list["TypeRef"] = field(default_factory=list)


Expr = Union[
    LitInt,
    LitFloat,
    LitBool,
    LitString,
    Var,
    Coin,
    Dirac,
    KetLit,
    Vacuum,
    BinOp,
    Call,
    WhenExpr,
    Pipe,
    Lambda,
    Attr,
    Inspect,
    TupleExpr,
    EvolveExpr,
    TensorExpr,
    UnaryNot,
]


# --- Statements / decls ---


@dataclass
class StateBind:
    """`state x = e`, Type-First `Mass m = e` / `Operator H = …`, or `(x, p) = e`."""

    names: list[str]
    expr: Any  # Expr | OpExpr
    span: Span
    ty: TypeRef | None = None  # Type-First head; None for `state` / bare tuple
    visibility: Visibility = "module"

    @property
    def name(self) -> str:
        return self.names[0]


@dataclass
class Measure:
    expr: Expr
    span: Span
    sink: str | None = None


@dataclass
class Snapshot:
    expr: Expr
    sink: str
    span: Span


Stmt = Union[StateBind, Measure, Snapshot]


@dataclass
class Block:
    stmts: list[Stmt]
    span: Span
    # A measure-free function/method may end with one expression.  `main`
    # keeps this empty and terminates through its final `measure` statement.
    result: Expr | None = None


@dataclass
class Param:
    name: str
    ty: TypeRef | None


@dataclass
class MainDecl:
    params: list[Param]
    body: Block
    span: Span
    return_type: TypeRef | None = None


@dataclass
class FieldDecl:
    """`val name: Type [= expr]` / `var name: Type [= expr]` (ADR 0056 OOP)."""

    name: str
    ty: TypeRef
    mutable: bool
    default: "Expr | None"
    span: Span
    visibility: Visibility = "module"


@dataclass
class EnumDecl:
    """`enum BoundaryCondition { Periodic, Open }` (ADR 0055/0056 OOP)."""

    name: str
    variants: list[str]
    span: Span
    namespace: list[str] = field(default_factory=list)
    visibility: Visibility = "module"

    @property
    def qualified_name(self) -> str:
        if self.namespace:
            return ".".join([*self.namespace, self.name])
        return self.name


@dataclass
class StructDecl:
    """`struct SSHParams { val v: Energy, val w: Energy }` — immutable value type."""

    name: str
    fields: list[FieldDecl]
    span: Span
    namespace: list[str] = field(default_factory=list)
    visibility: Visibility = "module"

    @property
    def qualified_name(self) -> str:
        if self.namespace:
            return ".".join([*self.namespace, self.name])
        return self.name


@dataclass
class AssignStmt:
    """`this.field = expr` or `obj.field = expr` (mutable `var` only)."""

    target: "Expr"  # Attr
    value: "Expr"
    span: Span


@dataclass
class ClassDecl:
    name: str
    ifaces: list[str]
    span: Span
    fields: list[StateBind] = field(default_factory=list)  # Type-First
    members: list[FieldDecl] = field(default_factory=list)  # val/var :
    methods: list[FunDecl] = field(default_factory=list)
    namespace: list[str] = field(default_factory=list)  # ADR 0055
    visibility: Visibility = "module"

    @property
    def qualified_name(self) -> str:
        if self.namespace:
            return ".".join([*self.namespace, self.name])
        return self.name


@dataclass
class NamespaceDecl:
    """`namespace A.B { … }` (ADR 0055). Flattened before typecheck/eval."""

    path: list[str]
    decls: list[Any]
    span: Span


@dataclass
class InterfaceDecl:
    name: str
    span: Span


@dataclass
class FunDecl:
    name: str
    params: list[Param]
    body: Block
    span: Span
    return_type: TypeRef | None = None
    visibility: Visibility = "module"
    namespace: list[str] = field(default_factory=list)  # ADR 0055

    @property
    def qualified_name(self) -> str:
        if self.namespace:
            return ".".join([*self.namespace, self.name])
        return self.name


@dataclass
class ModuleInfoDecl:
    """`module com.foo { exports …; requires …; }` (ADR 0058)."""

    name: list[str]
    exports: list[list[str]]
    requires: list[list[str]]
    span: Span

    @property
    def qualified_name(self) -> str:
        return ".".join(self.name)


@dataclass
class PackageDecl:
    path: list[str]
    span: Span


@dataclass
class ImportDecl:
    path: list[str]
    name: str
    span: Span


@dataclass
class CompilationUnit:
    package: PackageDecl | None
    imports: list[ImportDecl]
    decls: list[Any]
    main: MainDecl | None
    span: Span
