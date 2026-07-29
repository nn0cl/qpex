"""Immutable phase-resolved typed HIR view (LISS-0080).

Additive extraction from TypeChecker — no evaluator rewire in Slices A–D.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from .ast_nodes import CompilationUnit, FunDecl, ScientificScopeContract, ScientificScopeDecl
from .typecheck import Ty, TypeChecker

_KERNEL_PHASE = "kernel"

_KNOWN_PHASES = frozenset({
    "theory", "experiment", "workflow", "execution", "report",
    "system", _KERNEL_PHASE,
})

_KNOWN_EFFECTS = frozenset({"Measure", "Snapshot", "Inspect", "Host"})


@dataclass(frozen=True, slots=True)
class HirSpan:
    """Decl-level source location."""

    line: int
    col: int


@dataclass(frozen=True, slots=True)
class HirDecl:
    """Top-level declaration with resolved scientific phase, effects, and span."""

    name: str
    phase: str
    effects: frozenset[str] = field(default_factory=frozenset)
    span: HirSpan | None = None


@dataclass(frozen=True, slots=True)
class HirModule:
    """Immutable HIR module snapshot (symbols + typed expression map)."""

    symbols: Mapping[str, Ty]
    typed: Mapping[int, Ty]
    declarations: Mapping[str, HirDecl]


def _span_from(ast_node: Any) -> HirSpan | None:
    s = getattr(ast_node, "span", None)
    if s is None:
        return None
    return HirSpan(line=s.line, col=s.col)


def _build_declarations(
    checker: TypeChecker,
    scope_contracts: Mapping[str, ScientificScopeContract] | None,
    unit: CompilationUnit | None,
) -> Mapping[str, HirDecl]:
    decls: dict[str, HirDecl] = {}

    # Build name→span index from AST decls when unit is available.
    span_index: dict[str, HirSpan | None] = {}
    if unit is not None:
        for d in unit.decls:
            name = getattr(d, "name", None)
            if name:
                span_index[name] = _span_from(d)
        if unit.main is not None:
            span_index["main"] = _span_from(unit.main)

    if scope_contracts:
        for name, contract in scope_contracts.items():
            decls[name] = HirDecl(
                name=name,
                phase=contract.kind,
                effects=frozenset(),
                span=span_index.get(name),
            )

    for name in checker.fun_returns:
        if "." in name or name in decls:
            continue
        effects = checker.fun_effects.get(name, frozenset())
        decls[name] = HirDecl(
            name=name,
            phase=_KERNEL_PHASE,
            effects=frozenset(effects),
            span=span_index.get(name),
        )

    if checker.has_entry_main and "main" not in decls:
        decls["main"] = HirDecl(
            name="main",
            phase=_KERNEL_PHASE,
            effects=frozenset(),
            span=span_index.get("main"),
        )

    return MappingProxyType(decls)


def build_hir(
    checker: TypeChecker,
    *,
    scope_contracts: Mapping[str, ScientificScopeContract] | None = None,
    unit: CompilationUnit | None = None,
) -> HirModule:
    """Build an immutable HIR view from a completed TypeChecker.

    Slice A: symbol table + typed expression map.
    Slice B: declaration phases from sealed scientific-scope contracts.
    Slice C: explicit ``effects {…}`` declarations on each HIR decl.
    Slice D: decl-level source provenance via optional ``unit``.
    """
    return HirModule(
        symbols=MappingProxyType(dict(checker.env)),
        typed=MappingProxyType(dict(checker.typed)),
        declarations=_build_declarations(checker, scope_contracts, unit),
    )


_VERIFIER_DIAGNOSTICS_CODE = "HIR_INVARIANT_ERROR"


def verify_hir(module: HirModule) -> list[dict]:
    """Lightweight HIR invariant checker.

    Returns a list of diagnostic dicts (empty means valid).
    Checks that all declaration phases and effects are known values.
    """
    diags: list[dict] = []
    for name, decl in module.declarations.items():
        if decl.phase not in _KNOWN_PHASES:
            diags.append({
                "code": _VERIFIER_DIAGNOSTICS_CODE,
                "message": (
                    f"HIR decl '{name}' has unknown phase '{decl.phase}'; "
                    f"expected one of {sorted(_KNOWN_PHASES)}"
                ),
            })
        unknown_effects = decl.effects - _KNOWN_EFFECTS
        if unknown_effects:
            diags.append({
                "code": _VERIFIER_DIAGNOSTICS_CODE,
                "message": (
                    f"HIR decl '{name}' has unknown effect(s) "
                    f"{sorted(unknown_effects)}; "
                    f"expected subset of {sorted(_KNOWN_EFFECTS)}"
                ),
            })
    return diags
