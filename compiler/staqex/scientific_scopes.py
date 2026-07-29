"""Resolution of phase-separated scientific scope contracts (LISS-0034 / 0076)."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any

from .ast_nodes import (
    Attr,
    BinOp,
    Call,
    ClassDecl,
    FunDecl,
    OpBinder,
    OpBin,
    OpCall,
    OpExpr,
    OpIndexed,
    OpPow,
    OpVar,
    ReturnStmt,
    ScientificScopeContract,
    ScientificScopeDecl,
    StateBind,
    TypeRef,
    Var,
)

_ALLOWED_REFERENCES = {
    "theory": {"theory"},
    "experiment": {"theory", "experiment"},
    "workflow": {"theory", "experiment", "workflow"},
    "execution": {"theory", "experiment", "workflow", "execution"},
    "report": {"execution", "report"},
}

# Lexeme rejects stay PHASE_SCOPE_DEPENDENCY_ERROR (parser); not this code.
_LEXEME_EXECUTION_SYMBOLS = frozenset({"shots", "backend", "retry", "Host"})

# Phases that must not name symbols bound in execution or report bodies.
_PHASES_BLOCKED_FROM_LATER_SYMBOLS = frozenset(
    {"theory", "experiment", "workflow"}
)
# Backward-compatible alias (LISS-0076 naming).
_PHASES_BLOCKED_FROM_EXECUTION_SYMBOLS = _PHASES_BLOCKED_FROM_LATER_SYMBOLS


def resolve_scientific_scopes(
    declarations: Iterable[ScientificScopeDecl],
    *,
    unit_decls: Iterable[Any] | None = None,
) -> tuple[dict[str, ScientificScopeContract], list[dict]]:
    """Seal scope declarations and validate their dependency direction."""

    declarations = tuple(declarations)
    names = {declaration.name for declaration in declarations}
    contracts: dict[str, ScientificScopeContract] = {}
    diagnostics: list[dict] = []

    for declaration in declarations:
        for reference in declaration.references:
            if reference not in names:
                diagnostics.append(
                    {
                        "code": "PHASE_SCOPE_REFERENCE_ERROR",
                        "line": declaration.span.line,
                        "col": declaration.span.col,
                        "message": (
                            f"scope `{declaration.name}` references unknown "
                            f"scope `{reference}`"
                        ),
                    }
                )
                continue
            referenced = next(
                item for item in declarations if item.name == reference
            )
            allowed = _ALLOWED_REFERENCES.get(declaration.kind, set())
            if referenced.kind not in allowed:
                diagnostics.append(
                    {
                        "code": "PHASE_SCOPE_DIRECTION_ERROR",
                        "line": declaration.span.line,
                        "col": declaration.span.col,
                        "message": (
                            f"{declaration.kind} scope `{declaration.name}` "
                            f"cannot depend on {referenced.kind} scope "
                            f"`{reference}`"
                        ),
                    }
                )
        contracts[declaration.name] = ScientificScopeContract(
            kind=declaration.kind,
            name=declaration.name,
            references=tuple(declaration.references),
            symbols=tuple(declaration.symbols),
        )

    companions = tuple(unit_decls) if unit_decls is not None else ()
    diagnostics.extend(
        check_execution_symbol_body_visibility(declarations, unit_decls=companions)
    )
    return contracts, diagnostics


def check_execution_symbol_body_visibility(
    declarations: tuple[ScientificScopeDecl, ...],
    *,
    unit_decls: tuple[Any, ...] = (),
) -> list[dict]:
    """Reject later-phase symbols inside Theory/Experiment/Workflow bodies.

    LISS-0076: Execution-bound names + call/method taint.
    LISS-0118 Slice B: Report-bound names are also invisible upward; Report
    itself may still reference Execution symbols.
    """

    execution_symbols = {
        symbol: scope
        for scope in declarations
        if scope.kind == "execution"
        for symbol in scope.symbols
        if symbol not in _LEXEME_EXECUTION_SYMBOLS
    }
    report_symbols = {
        symbol: scope
        for scope in declarations
        if scope.kind == "report"
        for symbol in scope.symbols
    }
    hidden_symbols = {**execution_symbols, **report_symbols}
    if not hidden_symbols and not execution_symbols:
        return []

    tainted = _execution_tainted_callables(unit_decls, execution_symbols)
    diagnostics: list[dict] = []
    for scope in declarations:
        if scope.kind not in _PHASES_BLOCKED_FROM_LATER_SYMBOLS:
            continue
        for declaration in scope.body_declarations:
            expr = getattr(declaration, "expr", None)
            if expr is None:
                continue
            for ref in _iter_name_refs(expr):
                owner = hidden_symbols.get(ref.name)
                if owner is None:
                    continue
                diagnostics.append(
                    {
                        "code": "PHASE_TYPE_VISIBILITY_ERROR",
                        "line": ref.span.line,
                        "col": ref.span.col,
                        "message": (
                            f"{scope.kind} scope `{scope.name}` cannot "
                            f"reference {owner.kind} symbol `{ref.name}` from "
                            f"`{owner.name}`"
                        ),
                    }
                )
            for target, span in _iter_call_targets(expr):
                if not _call_target_is_tainted(target, tainted):
                    continue
                diagnostics.append(
                    {
                        "code": "PHASE_TYPE_VISIBILITY_ERROR",
                        "line": span.line,
                        "col": span.col,
                        "message": (
                            f"{scope.kind} scope `{scope.name}` cannot call "
                            f"`{target}` because it references an execution "
                            f"symbol"
                        ),
                    }
                )
        for _lhs, rhs, span in scope.field_bindings:
            owner = hidden_symbols.get(rhs)
            if owner is None:
                continue
            diagnostics.append(
                {
                    "code": "PHASE_TYPE_VISIBILITY_ERROR",
                    "line": span.line,
                    "col": span.col,
                    "message": (
                        f"{scope.kind} scope `{scope.name}` cannot "
                        f"reference {owner.kind} symbol `{rhs}` from "
                        f"`{owner.name}`"
                    ),
                }
            )
        for _key, value in scope.workflow_fields:
            owner = hidden_symbols.get(value)
            if owner is None:
                continue
            diagnostics.append(
                {
                    "code": "PHASE_TYPE_VISIBILITY_ERROR",
                    "line": scope.span.line,
                    "col": scope.span.col,
                    "message": (
                        f"{scope.kind} scope `{scope.name}` cannot "
                        f"reference {owner.kind} symbol `{value}` from "
                        f"`{owner.name}`"
                    ),
                }
            )
    return diagnostics


# Backward-compatible alias for Slice A call sites / traces.
check_theory_execution_body_visibility = check_execution_symbol_body_visibility


def _execution_tainted_callables(
    unit_decls: tuple[Any, ...],
    execution_symbols: dict[str, ScientificScopeDecl],
) -> set[str]:
    """Names of fn/methods that (transitively) reference Execution symbols.

    LISS-0076: one-hop direct body refs. LISS-0118 Slice A: fixpoint over
    call targets so ``mid() → leak()`` taints ``mid`` when ``leak`` is tainted.
    """

    direct: set[str] = set()
    call_edges: dict[str, set[str]] = {}

    def _register(name: str, block: Any) -> None:
        if _block_refs_execution(block, execution_symbols):
            direct.add(name)
        targets = {
            target for target, _span in _iter_block_call_targets(block)
        }
        call_edges.setdefault(name, set()).update(targets)

    for decl in unit_decls:
        if isinstance(decl, FunDecl):
            _register(decl.name, decl.body)
        elif isinstance(decl, ClassDecl):
            for method in decl.methods:
                # LISS-0118 Slice C: methods are keyed as Class.method only.
                # Bare short names fail closed via `_call_target_is_tainted`.
                _register(f"{decl.name}.{method.name}", method.body)

    tainted = set(direct)
    changed = True
    while changed:
        changed = False
        for name, targets in call_edges.items():
            if name in tainted:
                continue
            if any(_call_target_is_tainted(t, tainted) for t in targets):
                tainted.add(name)
                changed = True
    return tainted


def _call_target_is_tainted(target: str, tainted: set[str]) -> bool:
    """Qualified names match exactly; bare names fail closed on any peer.

    ``Pure.k`` stays precise. Bare ``k`` matches FunDecl ``k`` or any
    ``*.k`` method that is already tainted (LISS-0118 Slice C).
    """

    if target in tainted:
        return True
    if "." in target:
        return False
    return any(name == target or name.endswith(f".{target}") for name in tainted)


def _block_refs_execution(
    block: Any,
    execution_symbols: dict[str, ScientificScopeDecl],
) -> bool:
    for stmt in getattr(block, "stmts", ()):
        if isinstance(stmt, StateBind):
            if any(ref.name in execution_symbols for ref in _iter_name_refs(stmt.expr)):
                return True
        elif isinstance(stmt, ReturnStmt):
            expr = getattr(stmt, "expr", None)
            if expr is not None and any(
                ref.name in execution_symbols for ref in _iter_name_refs(expr)
            ):
                return True
    return False


def _iter_block_call_targets(block: Any) -> Iterator[tuple[str, Any]]:
    for stmt in getattr(block, "stmts", ()):
        if isinstance(stmt, StateBind):
            yield from _iter_call_targets(stmt.expr)
        elif isinstance(stmt, ReturnStmt):
            expr = getattr(stmt, "expr", None)
            if expr is not None:
                yield from _iter_call_targets(expr)


def _iter_call_targets(expr: object) -> Iterator[tuple[str, Any]]:
    if isinstance(expr, Call):
        callee = expr.callee
        if isinstance(callee, Var):
            yield callee.name, expr.span
        elif isinstance(callee, Attr):
            obj = callee.obj
            if isinstance(obj, Var):
                yield f"{obj.name}.{callee.name}", expr.span
            elif isinstance(obj, Call) and isinstance(obj.callee, Var):
                yield f"{obj.callee.name}.{callee.name}", expr.span
            else:
                yield callee.name, expr.span
        yield from _iter_call_targets(callee)
        for arg in expr.args:
            yield from _iter_call_targets(arg)
        return
    if isinstance(expr, BinOp):
        yield from _iter_call_targets(expr.lhs)
        yield from _iter_call_targets(expr.rhs)
        return
    if isinstance(expr, Attr):
        yield from _iter_call_targets(expr.obj)
        return
    if isinstance(expr, OpBin):
        yield from _iter_call_targets(expr.lhs)
        yield from _iter_call_targets(expr.rhs)
        return
    if isinstance(expr, OpCall):
        yield expr.name, expr.span
        for arg in expr.args:
            yield from _iter_call_targets(arg)
        return
    if isinstance(expr, OpIndexed):
        yield from _iter_call_targets(expr.base)
        yield from _iter_call_targets(expr.index)
        return
    if isinstance(expr, OpPow):
        yield from _iter_call_targets(expr.base)
        return
    if isinstance(expr, OpBinder):
        if not isinstance(expr.domain, TypeRef):
            yield from _iter_call_targets(expr.domain)
        yield from _iter_call_targets(expr.body)
        if expr.guard is not None:
            yield from _iter_call_targets(expr.guard)
        return


def _iter_name_refs(expr: OpExpr | object) -> Iterator[OpVar | Var]:
    if isinstance(expr, (OpVar, Var)):
        yield expr
        return
    if isinstance(expr, (OpBin, BinOp)):
        yield from _iter_name_refs(expr.lhs)
        yield from _iter_name_refs(expr.rhs)
        return
    if isinstance(expr, OpPow):
        yield from _iter_name_refs(expr.base)
        return
    if isinstance(expr, OpIndexed):
        yield from _iter_name_refs(expr.base)
        yield from _iter_name_refs(expr.index)
        return
    if isinstance(expr, OpCall):
        for arg in expr.args:
            yield from _iter_name_refs(arg)
        return
    if isinstance(expr, Call):
        yield from _iter_name_refs(expr.callee)
        for arg in expr.args:
            yield from _iter_name_refs(arg)
        return
    if isinstance(expr, Attr):
        yield from _iter_name_refs(expr.obj)
        return
    if isinstance(expr, OpBinder):
        if not isinstance(expr.domain, TypeRef):
            yield from _iter_name_refs(expr.domain)
        yield from _iter_name_refs(expr.body)
        if expr.guard is not None:
            yield from _iter_name_refs(expr.guard)
        return


def _iter_op_vars(expr: OpExpr | object) -> Iterator[OpVar]:
    """Yield only OpVar nodes (kept for callers that need operator trees)."""
    for ref in _iter_name_refs(expr):
        if isinstance(ref, OpVar):
            yield ref
