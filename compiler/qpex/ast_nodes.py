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
    Vacuum,
    BinOp,
    Call,
    WhenExpr,
    Pipe,
    Lambda,
    Attr,
    Inspect,
]


# --- Statements / decls ---


@dataclass
class StateBind:
    name: str
    expr: Expr
    span: Span


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
