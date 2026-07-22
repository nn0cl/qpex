"""QPex AST nodes (design baseline subset for Phase 2.1)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Union


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
    times: int
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
    """Position-grid quadratures Xx, Px (ADR 0051)."""

    kind: str  # Xx | Px
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
class OpVar:
    """Reference to a bound Operator name."""

    name: str
    span: Span


OpExpr = Union[OpPauli, OpNumber, OpQuadrature, OpGridQuad, OpLit, OpBin, OpPow, OpVar]


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


@dataclass
class Param:
    name: str
    ty: TypeRef | None


@dataclass
class MainDecl:
    params: list[Param]
    body: Block
    span: Span


@dataclass
class ClassDecl:
    name: str
    ifaces: list[str]
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
    visibility: Literal["public", "private"] = "private"


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
