"""Static lowering for the accepted finite mathematical binder slice."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .ast_nodes import (
    CompilationUnit,
    OpBin,
    OpBinder,
    OpCall,
    OpExpr,
    OpIdentity,
    OpIndexed,
    OpLit,
    OpPauli,
    OpVar,
    StateBind,
    TypeRef,
)
from .second_quantization import SecondQuantizationMappingError, jordan_wigner_map

MAX_EXPANSION_TERMS = 1_000_000
_BINDER_KINDS = frozenset({"sum", "product"})
_GUARD_OPERATORS = frozenset({"<", "<=", ">", ">=", "==", "!="})
_INDEX_ACCESSORS = frozenset({"next", "wrap"})
_INDEX_ACCESS_ERROR = (
    "indexed Pauli must use the binder, next(binder), or wrap(binder)"
)
IDENTITY_ACTING_SPACE_UNDETERMINED = "IDENTITY_ACTING_SPACE_UNDETERMINED"


@dataclass(frozen=True)
class _Context:
    bindings: Mapping[str, int]
    register_size: int | None
    domain_start: int | None = None
    domain_end: int | None = None


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


def _raw_binder_bounds(expr: OpBinder) -> tuple[int, int]:
    if not isinstance(expr.domain, TypeRef):
        raise ValueError("binder domain is not a finite Index")
    bounds = _inclusive_bounds(expr.domain)
    if bounds is None:
        raise ValueError("binder domain is not a finite Index")
    return bounds


def _binder_bounds(expr: OpBinder) -> tuple[int, int]:
    start, end = _raw_binder_bounds(expr)
    if start < 0 or end < start:
        raise ValueError("invalid binder range")
    return start, end


def _resolve_index(expr: OpExpr, context: _Context) -> int | None:
    if isinstance(expr, OpVar) and expr.name in context.bindings:
        return context.bindings[expr.name]
    if isinstance(expr, OpCall) and expr.name in _INDEX_ACCESSORS:
        if len(expr.args) != 1:
            return None
        index = _resolve_index(expr.args[0], context)
        return _resolve_accessor(expr.name, index, context)
    if isinstance(expr, OpLit):
        return int(expr.value)
    return None


def _resolve_accessor(
    name: str, index: int | None, context: _Context
) -> int | None:
    if index is None:
        return None
    if name == "next":
        return index + 1
    if name != "wrap" or context.domain_start is None or context.domain_end is None:
        return None
    width = context.domain_end - context.domain_start + 1
    return context.domain_start + (index + 1 - context.domain_start) % width


def _resolve_bound_index(expr: OpExpr, bindings: Mapping[str, int]) -> int | None:
    if isinstance(expr, OpVar) and expr.name in bindings:
        return bindings[expr.name]
    if isinstance(expr, OpLit):
        return int(expr.value)
    return None


def _lower_metadata_expr(expr: OpExpr, context: _Context) -> Any:
    if isinstance(expr, OpBin):
        return {
            "kind": "Binary",
            "operator": expr.op,
            "left": _lower_metadata_expr(expr.lhs, context),
            "right": _lower_metadata_expr(expr.rhs, context),
        }
    if isinstance(expr, OpIndexed):
        index = _resolve_index(expr.index, context)
        if not isinstance(expr.base, OpPauli):
            return {
                "kind": "Indexed",
                "base": _lower_metadata_expr(expr.base, context),
                "index": (
                    {"kind": "Index", "value": index}
                    if index is not None
                    else {"kind": "Expression"}
                ),
            }
        if index is None:
            raise ValueError(_INDEX_ACCESS_ERROR)
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
            "args": [_lower_metadata_expr(arg, context) for arg in expr.args],
        }
    if isinstance(expr, OpBinder):
        return {
            "kind": "Binder",
            "binder": expr.kind,
            "variable": expr.variable,
            "body": "symbolic",
        }
    raise ValueError("binder body is outside the accepted Pauli slice")


def _lower_executable_expr(expr: OpExpr, context: _Context) -> OpExpr:
    """Materialize the accepted binder slice as executable Operator AST."""
    if _contains_second_quantized(expr) and not _contains_pauli(expr):
        substituted = _substitute_indices(expr, context.bindings)
        try:
            mapped, _ = jordan_wigner_map(substituted, span=expr.span)
            return mapped
        except SecondQuantizationMappingError as error:
            raise ValueError(error.message) from error
    if isinstance(expr, OpBin):
        return OpBin(
            op=expr.op,
            lhs=_lower_executable_expr(expr.lhs, context),
            rhs=_lower_executable_expr(expr.rhs, context),
            span=expr.span,
        )
    if isinstance(expr, OpIndexed):
        index = _resolve_index(expr.index, context)
        if index is None:
            raise ValueError(_INDEX_ACCESS_ERROR)
        if index < 0 or (
            context.register_size is not None and index >= context.register_size
        ):
            raise IndexError(index)
        if isinstance(expr.base, OpPauli):
            return OpPauli(kind=expr.base.kind, site=index, span=expr.base.span)
        raise ValueError("indexed operator is not executable yet")
    if isinstance(expr, OpLit):
        return OpLit(value=expr.value, span=expr.span)
    if isinstance(expr, OpVar):
        return expr
    if isinstance(expr, OpCall):
        raise ValueError("operator helper calls are not executable yet")
    if isinstance(expr, OpBinder):
        return _lower_binder_ast(expr, context)
    raise ValueError("binder body is outside the accepted Pauli slice")


def _fold_operator_terms(
    terms: list[OpExpr], kind: str, span: Any, acting_space: int | None = None
) -> OpExpr:
    if not terms:
        return OpIdentity(kind=kind, acting_space=acting_space, span=span)
    result = terms[0]
    operator = "+" if kind == "sum" else "*"
    for term in terms[1:]:
        result = OpBin(op=operator, lhs=result, rhs=term, span=span)
    return result


def _contains_second_quantized(expr: OpExpr) -> bool:
    if isinstance(expr, OpIndexed):
        return isinstance(expr.base, OpVar) and expr.base.name in {"create", "annihilate"}
    if isinstance(expr, OpBin):
        return _contains_second_quantized(expr.lhs) or _contains_second_quantized(expr.rhs)
    return False


def _contains_pauli(expr: OpExpr) -> bool:
    if isinstance(expr, OpPauli):
        return True
    if isinstance(expr, OpIndexed):
        return _contains_pauli(expr.base)
    if isinstance(expr, OpBin):
        return _contains_pauli(expr.lhs) or _contains_pauli(expr.rhs)
    return False


def _substitute_indices(expr: OpExpr, bindings: Mapping[str, int]) -> OpExpr:
    if isinstance(expr, OpIndexed):
        index = _resolve_bound_index(expr.index, bindings)
        if index is None:
            raise ValueError("indexed operator requires a static binder index")
        return OpIndexed(
            base=expr.base,
            index=OpLit(value=index, span=expr.index.span),
            span=expr.span,
        )
    if isinstance(expr, OpBin):
        return OpBin(
            op=expr.op,
            lhs=_substitute_indices(expr.lhs, bindings),
            rhs=_substitute_indices(expr.rhs, bindings),
            span=expr.span,
        )
    return expr


def _static_value(expr: OpExpr, bindings: Mapping[str, int]) -> int:
    value = _resolve_bound_index(expr, bindings)
    if value is None:
        raise ValueError("where guard must use static binder indices")
    return value


def _guard_matches(guard: OpExpr | None, bindings: Mapping[str, int]) -> bool:
    if guard is None:
        return True
    if not isinstance(guard, OpBin) or guard.op not in _GUARD_OPERATORS:
        raise ValueError("unsupported where guard")
    lhs = _static_value(guard.lhs, bindings)
    rhs = _static_value(guard.rhs, bindings)
    return {
        "<": lhs < rhs,
        "<=": lhs <= rhs,
        ">": lhs > rhs,
        ">=": lhs >= rhs,
        "==": lhs == rhs,
        "!=": lhs != rhs,
    }[guard.op]


def _binder_values(
    expr: OpBinder, context: _Context, *, apply_guard: bool = True
):
    start, end = _raw_binder_bounds(expr)
    if end < start:
        return
    register_size = context.register_size
    if register_size is not None and end >= register_size:
        raise IndexError(end)
    for value in range(start, end + 1):
        bindings = dict(context.bindings)
        bindings[expr.variable] = value
        if not apply_guard or _guard_matches(expr.guard, bindings):
            yield _Context(bindings, register_size, start, end)


def _lower_binder_ast(expr: OpBinder, context: _Context) -> OpExpr:
    start, end = _raw_binder_bounds(expr)
    if end < start:
        return OpIdentity(
            kind=expr.kind,
            acting_space=context.register_size,
            span=expr.span,
        )
    terms = [
        _lower_executable_expr(expr.body, child)
        for child in _binder_values(expr, context)
    ]
    return _fold_operator_terms(
        terms, expr.kind, expr.span, acting_space=context.register_size
    )


def _candidate_count(expr: OpBinder, context: _Context) -> int:
    start, end = _raw_binder_bounds(expr)
    if end < start:
        return 0
    count = end - start + 1
    if isinstance(expr.body, OpBinder):
        child_context = next(
            iter(_binder_values(expr, context, apply_guard=False)), None
        )
        if child_context is None:
            return 0
        inner = _candidate_count(expr.body, child_context)
        return count * inner
    return count


def _retained_leaf_count(expr: OpBinder, context: _Context) -> int:
    total = 0
    for child in _binder_values(expr, context):
        if isinstance(expr.body, OpBinder):
            total += _retained_leaf_count(expr.body, child)
        else:
            total += 1
    return total


def _accessor_names(expr: OpExpr) -> list[str]:
    if isinstance(expr, OpCall):
        names = [expr.name] if expr.name in _INDEX_ACCESSORS else []
        for arg in expr.args:
            names.extend(_accessor_names(arg))
        return names
    if isinstance(expr, OpIndexed):
        return _accessor_names(expr.base) + _accessor_names(expr.index)
    if isinstance(expr, OpBin):
        return _accessor_names(expr.lhs) + _accessor_names(expr.rhs)
    if isinstance(expr, OpBinder):
        return _accessor_names(expr.body)
    return []


def _operator_metadata(
    name: str, expr: OpExpr, unit: CompilationUnit
) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    if not isinstance(expr, OpBinder):
        return None, []
    if expr.kind not in _BINDER_KINDS:
        return None, []
    if not isinstance(expr.domain, TypeRef):
        return None, []
    bounds = _inclusive_bounds(expr.domain)
    if bounds is None:
        return None, []
    start, end = bounds
    if end < start:
        domain = {"start": start, "end": end, "inclusive": True}
        return (
            {
                "operator": name,
                "domain": domain,
                "expanded_terms": 0,
                "resource_check": "passed",
                "operator_tree": {"kind": "Identity", "identity": expr.kind},
                "provenance": {
                    "source_span": {"line": expr.span.line, "col": expr.span.col},
                    "binder_variable": expr.variable,
                    "domain": domain,
                    "expanded_terms": 0,
                    "retained_terms": 0,
                    "identity": expr.kind,
                    "resource_check": "passed",
                },
            },
            [],
        )
    try:
        start, end = _binder_bounds(expr)
    except ValueError:
        return None, [
            _diagnostic(
                "BINDER_DOMAIN_ERROR",
                expr,
                "inclusive binder range is empty or invalid",
            )
        ]
    register_size = _register_size(unit)
    count = _candidate_count(expr, _Context({}, register_size))
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
    context = _Context({}, register_size)
    try:
        for child in _binder_values(expr, context):
            terms.append(_lower_metadata_expr(expr.body, child))
    except IndexError:
        return None, [
            _diagnostic(
                "BINDER_INDEX_OUT_OF_BOUNDS",
                expr,
                "next(i) crosses the Open binder boundary",
            )
        ]
    except ValueError as error:
        return None, [
            _diagnostic(
                "BINDER_GUARD_UNSUPPORTED" if expr.guard is not None else "BINDER_DOMAIN_ERROR",
                expr,
                str(error),
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
                "binder_variables": list(expr.origin.variables) if expr.origin else [expr.variable],
                "desugared": expr.origin.desugared if expr.origin else False,
                "domain": domain,
                "expanded_terms": count,
                "retained_terms": _retained_leaf_count(expr, context),
                "accessors": _accessor_names(expr),
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


def identity_acting_space_diagnostics(
    unit: CompilationUnit,
) -> list[dict[str, Any]]:
    """Validate empty-fold identities at an execution boundary."""
    if _register_size(unit) is not None:
        return []
    lowered, _ = lower_finite_binders(unit)
    diagnostics: list[dict[str, Any]] = []
    for metadata in lowered.values():
        if metadata.get("operator_tree", {}).get("kind") != "Identity":
            continue
        provenance = metadata.get("provenance", {})
        diagnostics.append(
            {
                "code": IDENTITY_ACTING_SPACE_UNDETERMINED,
                "line": provenance.get("source_span", {}).get("line", 0),
                "col": provenance.get("source_span", {}).get("col", 0),
                "message": (
                    "cannot determine the space this identity acts on; "
                    "specify QubitRegister<N>"
                ),
            }
        )
    return diagnostics


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
        if expr.kind not in _BINDER_KINDS:
            raise ValueError(f"unsupported binder `{expr.kind}`")
        start, end = _raw_binder_bounds(expr)
        register_size = _register_size(unit)
        if end < start:
            return _lower_binder_ast(expr, _Context({}, register_size))
        if register_size is not None and end >= register_size:
            raise IndexError(end)
        return _lower_binder_ast(expr, _Context({}, register_size))
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
