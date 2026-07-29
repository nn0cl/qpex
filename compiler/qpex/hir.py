"""Immutable phase-resolved typed HIR view (LISS-0080).

Additive extraction from TypeChecker — no evaluator rewire in Slices A–C.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

from .ast_nodes import ScientificScopeContract
from .typecheck import Ty, TypeChecker

_KERNEL_PHASE = "kernel"


@dataclass(frozen=True, slots=True)
class HirDecl:
    """Top-level declaration with resolved scientific phase and explicit effects."""

    name: str
    phase: str
    effects: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True, slots=True)
class HirModule:
    """Immutable HIR module snapshot (symbols + typed expression map)."""

    symbols: Mapping[str, Ty]
    typed: Mapping[int, Ty]
    declarations: Mapping[str, HirDecl]


def _build_declarations(
    checker: TypeChecker,
    scope_contracts: Mapping[str, ScientificScopeContract] | None,
) -> Mapping[str, HirDecl]:
    decls: dict[str, HirDecl] = {}

    if scope_contracts:
        for name, contract in scope_contracts.items():
            # Scientific-scope decls carry no effects (body-level typing deferred).
            decls[name] = HirDecl(name=name, phase=contract.kind, effects=frozenset())

    for name in checker.fun_returns:
        if "." in name or name in decls:
            continue
        effects = checker.fun_effects.get(name, frozenset())
        decls[name] = HirDecl(name=name, phase=_KERNEL_PHASE, effects=frozenset(effects))

    if checker.has_entry_main and "main" not in decls:
        # main's implicit full-effects permission is an unresolved typecheck rule;
        # recording it as explicit effects is deferred to the execution-phase ADR.
        decls["main"] = HirDecl(name="main", phase=_KERNEL_PHASE, effects=frozenset())

    return MappingProxyType(decls)


def build_hir(
    checker: TypeChecker,
    *,
    scope_contracts: Mapping[str, ScientificScopeContract] | None = None,
) -> HirModule:
    """Build an immutable HIR view from a completed TypeChecker.

    Slice A records symbol table and typed expression map. Slice B adds
    declaration phases from sealed scientific-scope contracts; unscoped
    top-level decls default to ``kernel``. Slice C records explicit
    ``effects {…}`` declarations on each HIR decl.
    """
    return HirModule(
        symbols=MappingProxyType(dict(checker.env)),
        typed=MappingProxyType(dict(checker.typed)),
        declarations=_build_declarations(checker, scope_contracts),
    )
