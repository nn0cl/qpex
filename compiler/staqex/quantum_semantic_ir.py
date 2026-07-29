"""Slice A Quantum Semantic IR identity and root contracts.

This module intentionally owns only immutable semantic identities, provenance,
schema versioning, and deterministic root diagnostics. Region behavior,
finite-space lowering, pipeline wiring, and target adapters belong to later
LISS-0082 slices or other Issues.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

SCHEMA_VERSION = 1
Diagnostic = dict[str, Any]

__all__ = [
    "Diagnostic",
    "QuantumSemanticModule",
    "SCHEMA_VERSION",
    "SemanticId",
    "SemanticOrigin",
    "verify_quantum_semantic_ir",
]


@dataclass(frozen=True, slots=True)
class SemanticId:
    """Stable identity for a semantic object within a named scope."""

    kind: str
    scope: str
    ordinal: int

    def __post_init__(self) -> None:
        if not self.kind:
            raise ValueError("semantic identity kind must not be empty")
        if not self.scope:
            raise ValueError("semantic identity scope must not be empty")
        if self.ordinal < 0:
            raise ValueError("semantic identity ordinal must not be negative")


@dataclass(frozen=True, slots=True)
class SemanticOrigin:
    """Closed source and transformation ancestry for a semantic identity."""

    source_id: str
    line: int
    col: int
    upstream_ids: tuple[str, ...] = field(default_factory=tuple)
    transform_id: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "upstream_ids", tuple(self.upstream_ids))


@dataclass(frozen=True, slots=True)
class QuantumSemanticModule:
    """Schema-versioned immutable root for later Semantic IR slices."""

    schema_version: int
    roots: tuple[SemanticId, ...] = field(default_factory=tuple)
    region_roots: tuple[SemanticId, ...] = field(default_factory=tuple)
    origins: tuple[SemanticOrigin, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "roots", tuple(self.roots))
        object.__setattr__(self, "region_roots", tuple(self.region_roots))
        object.__setattr__(self, "origins", tuple(self.origins))


def _diagnostic(code: str, message: str, **details: Any) -> Diagnostic:
    result: Diagnostic = {"code": code, "message": message}
    result.update(details)
    return result


def _semantic_identities(module: QuantumSemanticModule) -> tuple[SemanticId, ...]:
    return module.roots + module.region_roots


def _origin_is_incomplete(origin: SemanticOrigin) -> bool:
    return (
        not origin.source_id
        or origin.line < 1
        or origin.col < 1
        or not origin.transform_id
    )


def verify_quantum_semantic_ir(module: QuantumSemanticModule) -> list[Diagnostic]:
    """Return deterministic non-mutating diagnostics for the Slice A root."""

    diagnostics: list[Diagnostic] = []
    if module.schema_version != SCHEMA_VERSION:
        diagnostics.append(
            _diagnostic(
                "QSEM_SCHEMA_VERSION_UNSUPPORTED",
                "unsupported Quantum Semantic IR schema version",
                schema_version=module.schema_version,
            )
        )

    identities = _semantic_identities(module)
    seen: set[SemanticId] = set()
    for identity in identities:
        if identity in seen:
            diagnostics.append(
                _diagnostic(
                    "QSEM_IDENTITY_CONFLICT",
                    "duplicate semantic identity in module roots",
                    identity=identity,
                )
            )
        seen.add(identity)

    if identities and not module.origins:
        diagnostics.append(
            _diagnostic(
                "QSEM_PROVENANCE_INCOMPLETE",
                "semantic roots require at least one source origin",
            )
        )

    for origin in module.origins:
        if _origin_is_incomplete(origin):
            diagnostics.append(
                _diagnostic(
                    "QSEM_PROVENANCE_INCOMPLETE",
                    "source origin is missing required ancestry fields",
                    origin=origin,
                )
            )

    return diagnostics
