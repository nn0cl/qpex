"""AT-TDD Phase 1 Red: LISS-0082 Slice A — semantic IDs and root verifier.

Slice A deliberately fixes only the immutable identity/provenance root.  It
does not authorize region behavior, Physics lowering, pipeline wiring, target
profiles, or provider adapters.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _load_api():
    """Slice A Green must provide this narrow additive API."""
    from compiler.staqex.quantum_semantic_ir import (
        QuantumSemanticModule,
        SemanticId,
        SemanticOrigin,
        verify_quantum_semantic_ir,
    )

    return QuantumSemanticModule, SemanticId, SemanticOrigin, verify_quantum_semantic_ir


def _origin(SemanticOrigin):
    return SemanticOrigin(
        source_id="slice-a.staqex",
        line=3,
        col=5,
        upstream_ids=(),
        transform_id="test.slice_a.v1",
    )


def test_slice_a_api_is_importable() -> None:
    QuantumSemanticModule, SemanticId, SemanticOrigin, verify = _load_api()

    assert QuantumSemanticModule is not None
    assert SemanticId is not None
    assert SemanticOrigin is not None
    assert callable(verify)


def test_root_and_identity_are_immutable_and_schema_versioned() -> None:
    QuantumSemanticModule, SemanticId, SemanticOrigin, _ = _load_api()
    origin = _origin(SemanticOrigin)
    root = SemanticId(kind="module", scope="root", ordinal=0)
    module = QuantumSemanticModule(
        schema_version=1,
        roots=(root,),
        region_roots=(),
        origins=(origin,),
    )

    assert module.schema_version == 1
    assert module.roots == (root,)
    assert isinstance(module.roots, tuple)
    try:
        module.schema_version = 2  # type: ignore[misc]
        mutated = True
    except (AttributeError, TypeError):
        mutated = False
    assert mutated is False, "Semantic root must be immutable"


def test_identity_is_deterministic_without_object_or_list_identity() -> None:
    _, SemanticId, _, _ = _load_api()

    first = SemanticId(kind="region", scope="module.main", ordinal=1)
    second = SemanticId(kind="region", scope="module.main", ordinal=1)

    assert first == second
    assert hash(first) == hash(second)
    assert "0x" not in repr(first)
    assert "provider" not in repr(first).lower()


def test_root_verifier_rejects_missing_provenance_with_named_diagnostic() -> None:
    QuantumSemanticModule, SemanticId, SemanticOrigin, verify = _load_api()
    module = QuantumSemanticModule(
        schema_version=1,
        roots=(SemanticId(kind="module", scope="root", ordinal=0),),
        region_roots=(),
        origins=(),
    )

    diagnostics = verify(module)

    assert any(
        diagnostic.get("code") == "QSEM_PROVENANCE_INCOMPLETE"
        for diagnostic in diagnostics
    )


def test_root_verifier_rejects_duplicate_ids_and_unknown_schema() -> None:
    QuantumSemanticModule, SemanticId, SemanticOrigin, verify = _load_api()
    origin = _origin(SemanticOrigin)
    duplicate = SemanticId(kind="module", scope="root", ordinal=0)
    module = QuantumSemanticModule(
        schema_version=999,
        roots=(duplicate, duplicate),
        region_roots=(),
        origins=(origin,),
    )

    diagnostics = verify(module)
    codes = {diagnostic.get("code") for diagnostic in diagnostics}

    assert "QSEM_IDENTITY_CONFLICT" in codes
    assert "QSEM_SCHEMA_VERSION_UNSUPPORTED" in codes


if __name__ == "__main__":
    for test in (
        test_slice_a_api_is_importable,
        test_root_and_identity_are_immutable_and_schema_versioned,
        test_identity_is_deterministic_without_object_or_list_identity,
        test_root_verifier_rejects_missing_provenance_with_named_diagnostic,
        test_root_verifier_rejects_duplicate_ids_and_unknown_schema,
    ):
        test()
    print("OK — LISS-0082 Slice A Phase 1 Red")
