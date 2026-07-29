"""Immutable phase-resolved typed HIR view (LISS-0080).

Additive extraction from TypeChecker — no evaluator rewire in Slice A/B.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from .ast_nodes import ScientificScopeContract
from .typecheck import Ty, TypeChecker

_KERNEL_PHASE = "kernel"


@dataclass(frozen=True, slots=True)
class HirDecl:
    """Top-level declaration with resolved scientific phase."""

    name: str
    phase: str


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
            decls[name] = HirDecl(name=name, phase=contract.kind)

    for name in checker.fun_returns:
        if "." in name or name in decls:
            continue
        decls[name] = HirDecl(name=name, phase=_KERNEL_PHASE)

    if checker.has_entry_main and "main" not in decls:
        decls["main"] = HirDecl(name="main", phase=_KERNEL_PHASE)

    return MappingProxyType(decls)


def build_hir(
    checker: TypeChecker,
    *,
    scope_contracts: Mapping[str, ScientificScopeContract] | None = None,
) -> HirModule:
    """Build an immutable HIR view from a completed TypeChecker.

    Slice A records symbol table and typed expression map. Slice B adds
    declaration phases from sealed scientific-scope contracts; unscoped
    top-level decls default to ``kernel``.
    """
    return HirModule(
        symbols=MappingProxyType(dict(checker.env)),
        typed=MappingProxyType(dict(checker.typed)),
        declarations=_build_declarations(checker, scope_contracts),
    )
