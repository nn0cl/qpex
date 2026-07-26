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
        return {
            "kind": "Binary",
            "operator": expr.op,
            "left": _lower_expr(expr.lhs, context, value),
            "right": _lower_expr(expr.rhs, context, value),
        }
    if isinstance(expr, OpIndexed):
        index = _resolve_index(expr.index, context.variable, value)
        if not isinstance(expr.base, OpPauli):
            return {
                "kind": "Indexed",
                "base": _lower_expr(expr.base, context, value),
                "index": (
                    {"kind": "Index", "value": index}
                    if index is not None
                    else {"kind": "Expression"}
                ),
            }
        if index is None:
            raise ValueError("indexed Pauli must use the binder or next(binder)")
        if index < 0 or (
            context.register_size is not None and index >= context.register_size
        ):
            raise IndexError(index)
        return {"kind": "Pauli", "name": expr.base.kind, "site": index}
    if isinstance(expr, OpLit):
        return {"kind": "Scalar", "value": expr.value}
    if isinstance(expr, OpVar):
        return {"kind": "Reference", "name": expr.name}
    if isinstance(expr, OpCall):
        return {
            "kind": "Call",
            "name": expr.name,
            "args": [_lower_expr(arg, context, value) for arg in expr.args],
        }
    if isinstance(expr, OpBinder):
        return {
            "kind": "Binder",
            "binder": expr.kind,
            "variable": expr.variable,
            "body": "symbolic",
        }
    raise ValueError("binder body is outside the accepted Pauli slice")


def _lower_expr_ast(expr: OpExpr, context: _Context, value: int) -> OpExpr:
    """Materialize the accepted binder slice as executable Operator AST."""
    if isinstance(expr, OpBin):
        return OpBin(
            op=expr.op,
            lhs=_lower_expr_ast(expr.lhs, context, value),
            rhs=_lower_expr_ast(expr.rhs, context, value),
            span=expr.span,
        )
    if isinstance(expr, OpIndexed):
        if not isinstance(expr.base, OpPauli):
            raise ValueError("indexed non-Pauli operator is not executable yet")
        index = _resolve_index(expr.index, context.variable, value)
        if index is None:
            raise ValueError("indexed Pauli must use the binder or next(binder)")
        if index < 0 or (
            context.register_size is not None and index >= context.register_size
        ):
            raise IndexError(index)
        return OpPauli(kind=expr.base.kind, site=index, span=expr.base.span)
    if isinstance(expr, OpLit):
        return OpLit(value=expr.value, span=expr.span)
    if isinstance(expr, OpVar):
        return expr
    if isinstance(expr, OpCall):
        raise ValueError("operator helper calls are not executable yet")
    if isinstance(expr, OpBinder):
        raise ValueError("nested binders are not executable yet")
    raise ValueError("binder body is outside the accepted Pauli slice")


def _sum_operator_terms(terms: list[OpExpr], span: Any) -> OpExpr:
    result = terms[0]
    for term in terms[1:]:
        result = OpBin(op="+", lhs=result, rhs=term, span=span)
    return result


def _expanded_terms(
    body: OpExpr,
    context: _Context,
    start: int,
    end: int,
    lowerer: Any,
) -> list[Any]:
    return [lowerer(body, context, value) for value in range(start, end + 1)]


def _operator_metadata(
    name: str, expr: OpExpr, unit: CompilationUnit
) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    if not isinstance(expr, OpBinder):
        return None, []
    if expr.kind not in {"sum", "product"}:
        return None, []
    if not isinstance(expr.domain, TypeRef):
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
    try:
        terms = _expanded_terms(expr.body, context, start, end, _lower_expr)
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
    operation = "Sum" if expr.kind == "sum" else "Product"
    return (
        {
            "operator": name,
            "domain": domain,
            "expanded_terms": count,
            "resource_check": "passed",
            "operator_tree": {"kind": operation, "terms": terms},
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


def lower_finite_binder_operators(
    unit: CompilationUnit,
) -> tuple[dict[str, OpExpr], list[dict[str, Any]]]:
    """Lower accepted finite binders into execution-ready Operator AST values.

    Inspection metadata is produced by ``lower_finite_binders`` separately;
    this function only supplies the executable representation consumed by the
    simulator and QASM lowering paths.
    """
    if unit.main is None:
        return {}, []
    lowered: dict[str, OpExpr] = {}
    diagnostics: list[dict[str, Any]] = []
    for stmt in unit.main.body.stmts:
        if not (
            isinstance(stmt, StateBind)
            and stmt.ty is not None
            and stmt.ty.name == "Operator"
        ):
            continue
        if not _contains_binder(stmt.expr):
            continue
        try:
            lowered[stmt.names[0]] = _lower_operator_expr(stmt.expr, unit)
        except (IndexError, ValueError):
            # qpu_ir_diagnostics is the authoritative validation path; an
            # invalid binder must not replace the original AST here.
            continue
    return lowered, diagnostics


def _lower_operator_expr(expr: OpExpr, unit: CompilationUnit) -> OpExpr:
    """Recursively lower finite sums while preserving ordinary operators."""
    if not _contains_binder(expr):
        return expr
    if isinstance(expr, OpBinder):
        if expr.kind != "sum":
            raise ValueError(f"unsupported binder `{expr.kind}`")
        if not isinstance(expr.domain, TypeRef):
            raise ValueError("binder domain is not a finite Index")
        bounds = _inclusive_bounds(expr.domain)
        if bounds is None:
            raise ValueError("binder domain is not a finite Index")
        start, end = bounds
        register_size = _register_size(unit)
        if start < 0 or end < start:
            raise ValueError("invalid binder range")
        if register_size is not None and end >= register_size:
            raise IndexError(end)
        context = _Context(expr.variable, register_size)
        terms = [
            _lower_expr_ast(expr.body, context, value)
            for value in range(start, end + 1)
        ]
        return _sum_operator_terms(terms, expr.span)
    if isinstance(expr, OpBin):
        return OpBin(
            op=expr.op,
            lhs=_lower_operator_expr(expr.lhs, unit),
            rhs=_lower_operator_expr(expr.rhs, unit),
            span=expr.span,
        )
    return expr


def _contains_binder(expr: OpExpr) -> bool:
    if isinstance(expr, OpBinder):
        return True
    if isinstance(expr, OpBin):
        return _contains_binder(expr.lhs) or _contains_binder(expr.rhs)
    return False
