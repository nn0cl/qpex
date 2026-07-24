"""Static lowering for the accepted finite mathematical binder slice."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .ast_nodes import (
    CompilationUnit,
    OpBin,
    OpBinder,
    OpCall,
    OpExpr,
    OpIndexed,
    OpLit,
    OpPauli,
    OpVar,
    StateBind,
    TypeRef,
)

MAX_EXPANSION_TERMS = 1_000_000


@dataclass(frozen=True)
class _Context:
    variable: str
    register_size: int | None


def _diagnostic(code: str, node: Any, message: str) -> dict[str, Any]:
    return {
        "code": code,
        "line": node.span.line,
        "col": node.span.col,
        "message": message,
    }


def _register_size(unit: CompilationUnit) -> int | None:
    if unit.main is None:
        return None
    for stmt in unit.main.body.stmts:
        if (
            isinstance(stmt, StateBind)
            and stmt.ty is not None
            and stmt.ty.name == "QubitRegister"
        ):
            if stmt.ty.args and stmt.ty.args[0].name.isdigit():
                return int(stmt.ty.args[0].name)
    return None


def _inclusive_bounds(domain: TypeRef) -> tuple[int, int] | None:
    if domain.name != "Index" or len(domain.args) != 2:
        return None
    try:
        return int(domain.args[0].name), int(domain.args[1].name)
    except ValueError:
        return None


def _resolve_index(expr: OpExpr, variable: str, value: int) -> int | None:
    if isinstance(expr, OpVar) and expr.name == variable:
        return value
    if isinstance(expr, OpCall) and expr.name == "next" and len(expr.args) == 1:
        index = _resolve_index(expr.args[0], variable, value)
        return None if index is None else index + 1
    if isinstance(expr, OpLit):
        return int(expr.value)
    return None


def _lower_expr(expr: OpExpr, context: _Context, value: int) -> Any:
    if isinstance(expr, OpBin):
        if expr.op != "*":
            raise ValueError("finite binder body only supports multiplication")
        return {
            "kind": "Binary",
            "operator": expr.op,
            "left": _lower_expr(expr.lhs, context, value),
            "right": _lower_expr(expr.rhs, context, value),
        }
    if isinstance(expr, OpIndexed):
        if not isinstance(expr.base, OpPauli):
            raise ValueError("indexed binder body must use Pauli operators")
        index = _resolve_index(expr.index, context.variable, value)
        if index is None:
            raise ValueError("indexed Pauli must use the binder or next(binder)")
        if index < 0 or (
            context.register_size is not None and index >= context.register_size
        ):
            raise IndexError(index)
        return {"kind": "Pauli", "name": expr.base.kind, "site": index}
    if isinstance(expr, OpLit):
        return {"kind": "Scalar", "value": expr.value}
    raise ValueError("binder body is outside the accepted Pauli slice")


def _operator_metadata(
    name: str, expr: OpExpr, unit: CompilationUnit
) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    if (
        not isinstance(expr, OpBinder)
        or expr.kind != "sum"
        or not isinstance(expr.domain, TypeRef)
    ):
        return None, []
    bounds = _inclusive_bounds(expr.domain)
    if bounds is None:
        return None, []
    start, end = bounds
    if start < 0 or end < start:
        return None, [
            _diagnostic(
                "BINDER_DOMAIN_ERROR",
                expr,
                "inclusive binder range is empty or invalid",
            )
        ]
    register_size = _register_size(unit)
    count = end - start + 1
    if count > MAX_EXPANSION_TERMS:
        return None, [
            _diagnostic(
                "BINDER_RESOURCE_ERROR",
                expr,
                "finite binder expansion exceeds the Kernel resource budget",
            )
        ]
    if register_size is not None and end >= register_size:
        return None, [
            _diagnostic(
                "BINDER_DOMAIN_ERROR",
                expr,
                "inclusive binder range exceeds the static register shape",
            )
        ]
    terms: list[Any] = []
    context = _Context(expr.variable, register_size)
    for value in range(start, end + 1):
        try:
            terms.append(_lower_expr(expr.body, context, value))
        except IndexError:
            return None, [
                _diagnostic(
                    "BINDER_INDEX_OUT_OF_BOUNDS",
                    expr,
                    "next(i) crosses the Open binder boundary",
                )
            ]
        except ValueError:
            return None, [
                _diagnostic(
                    "BINDER_DOMAIN_ERROR",
                    expr,
                    "binder body is outside the accepted Pauli slice",
                )
            ]
    domain = {"start": start, "end": end, "inclusive": True}
    return (
        {
            "operator": name,
            "domain": domain,
            "expanded_terms": count,
            "resource_check": "passed",
            "operator_tree": {"kind": "Sum", "terms": terms},
            "provenance": {
                "source_span": {"line": expr.span.line, "col": expr.span.col},
                "binder_variable": expr.variable,
                "domain": domain,
                "expanded_terms": count,
                "resource_check": "passed",
            },
        },
        [],
    )


def lower_finite_binders(
    unit: CompilationUnit,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if unit.main is None:
        return {}, []
    lowered: dict[str, Any] = {}
    diagnostics: list[dict[str, Any]] = []
    for stmt in unit.main.body.stmts:
        if (
            isinstance(stmt, StateBind)
            and stmt.ty is not None
            and stmt.ty.name == "Operator"
        ):
            metadata, errors = _operator_metadata(stmt.names[0], stmt.expr, unit)
            diagnostics.extend(errors)
            if metadata is not None:
                lowered[stmt.names[0]] = metadata
    return lowered, diagnostics
