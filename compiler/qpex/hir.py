"""Immutable phase-resolved typed HIR view (LISS-0080 Slice A).

Additive extraction from TypeChecker — no evaluator rewire in Slice A.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from .typecheck import Ty, TypeChecker


@dataclass(frozen=True, slots=True)
class HirModule:
    """Immutable HIR module snapshot (symbols + typed expression map)."""

    symbols: Mapping[str, Ty]
    typed: Mapping[int, Ty]


def build_hir(checker: TypeChecker) -> HirModule:
    """Build an immutable HIR view from a completed TypeChecker.

    Slice A records only the symbol table and typed expression map.
    Declaration phase, effects, and provenance land in later slices.
    """
    return HirModule(
        symbols=MappingProxyType(dict(checker.env)),
        typed=MappingProxyType(dict(checker.typed)),
    )
