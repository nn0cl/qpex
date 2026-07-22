"""Type checker — Lit-Lift to State<T> and relational ops → State<Bool>."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .ast_nodes import (
    BinOp,
    Call,
    Coin,
    CompilationUnit,
    Dirac,
    Expr,
    LitBool,
    LitFloat,
    LitInt,
    LitString,
    Measure,
    Pipe,
    Snapshot,
    StateBind,
    Vacuum,
    Var,
    WhenExpr,
)


@dataclass(frozen=True, slots=True)
class Ty:
    """Runtime/static type in QPex: always a State wrapper at expression level."""

    kind: str  # "State"
    payload: str  # Int, Float, Bool, String, Sys, Any, ...

    def __str__(self) -> str:
        return f"State<{self.payload}>"


RELATIONAL = {"==", "!=", "<", "<=", ">", ">="}
ARITH = {"+", "-", "*", "/"}


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
                payload = p.ty.args[0].name if p.ty.name == "State" and p.ty.args else p.ty.name
                if p.ty.name == "State":
                    self.env[p.name] = Ty("State", payload)
                else:
                    # parameter written as State<Sys> or bare — lift bare to State
                    self.env[p.name] = Ty("State", p.ty.name)
            else:
                self.env[p.name] = Ty("State", "Any")

        for stmt in unit.main.body.stmts:
            if isinstance(stmt, StateBind):
                ty = self._infer(stmt.expr)
                self.env[stmt.name] = ty
                self._assert_is_state(ty, stmt.span.line, stmt.span.col, stmt.name)
            elif isinstance(stmt, (Measure, Snapshot)):
                ty = self._infer(stmt.expr)
                self._assert_is_state(ty, stmt.span.line, stmt.span.col, "measure/snapshot")
        return self.diagnostics

    def type_of(self, expr: Expr) -> Ty | None:
        return self.typed.get(id(expr))

    def _assert_is_state(self, ty: Ty, line: int, col: int, what: str) -> None:
        if ty.kind != "State":
            self.diagnostics.append(
                {
                    "code": "TYPE_NOT_STATE",
                    "line": line,
                    "col": col,
                    "message": f"{what} has non-State type {ty}",
                }
            )

    def _infer(self, expr: Expr) -> Ty:
        ty = self._infer_inner(expr)
        self.typed[id(expr)] = ty
        return ty

    def _infer_inner(self, expr: Expr) -> Ty:
        if isinstance(expr, LitInt):
            return Ty("State", "Int")  # Lit-Lift
        if isinstance(expr, LitFloat):
            return Ty("State", "Float")
        if isinstance(expr, LitBool):
            return Ty("State", "Bool")
        if isinstance(expr, LitString):
            return Ty("State", "String")
        if isinstance(expr, Coin):
            return Ty("State", "Int")
        if isinstance(expr, Vacuum):
            return Ty("State", "Any")
        if isinstance(expr, Dirac):
            inner = self._infer(expr.arg)
            return Ty("State", inner.payload)
        if isinstance(expr, Var):
            return self.env.get(expr.name, Ty("State", "Any"))
        if isinstance(expr, BinOp):
            left = self._infer(expr.lhs)
            right = self._infer(expr.rhs)
            if expr.op in RELATIONAL:
                return Ty("State", "Bool")
            if expr.op in ARITH:
                payload = _promote(left.payload, right.payload)
                return Ty("State", payload)
            return Ty("State", "Any")
        if isinstance(expr, WhenExpr):
            self._infer(expr.ctrl)
            payloads = []
            for arm in expr.arms:
                payloads.append(self._infer(arm.body).payload)
            payload = payloads[0] if payloads else "Any"
            for p in payloads[1:]:
                payload = _promote(payload, p)
            return Ty("State", payload)
        if isinstance(expr, Call):
            self._infer(expr.callee)
            for a in expr.args:
                self._infer(a)
            return Ty("State", "Any")
        if isinstance(expr, Pipe):
            self._infer(expr.lhs)
            return self._infer(expr.rhs)
        # Lambda / Attr / Inspect
        from .ast_nodes import Attr, Inspect, Lambda

        if isinstance(expr, Lambda):
            self._infer(expr.body)
            return Ty("State", "Any")
        if isinstance(expr, Attr):
            self._infer(expr.obj)
            return Ty("State", "Any")
        if isinstance(expr, Inspect):
            return self._infer(expr.expr)
        return Ty("State", "Any")


def _promote(a: str, b: str) -> str:
    if a == b:
        return a
    if {a, b} <= {"Int", "Float"}:
        return "Float"
    if a == "Any":
        return b
    if b == "Any":
        return a
    return "Any"


def assert_expr_is_state(checker: TypeChecker, expr: Expr) -> bool:
    """Helper for harness assertTypeIsState against typed AST."""
    ty = checker.type_of(expr) or checker._infer(expr)
    return ty.kind == "State"


def lit_lift_demo(value: Any) -> Ty:
    if isinstance(value, bool):
        return Ty("State", "Bool")
    if isinstance(value, int):
        return Ty("State", "Int")
    if isinstance(value, float):
        return Ty("State", "Float")
    if isinstance(value, str):
        return Ty("State", "String")
    return Ty("State", "Any")
