"""AT-TDD Phase 1 Red: LISS-0117 Slice A — golden fixture loader."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

_FIXTURES = _REPO / "tests" / "fixtures" / "physics_ir"

_EXPECTED_IDS = (
    "PIR-G-ISING-001",
    "PIR-G-HEISENBERG-001",
    "PIR-G-HUBBARD-001",
    "PIR-G-MOLECULAR-001",
    "PIR-G-OSCILLATOR-001",
    "PIR-G-LINDBLAD-001",
)


def _load_api():
    from compiler.staqex.physics_ir_goldens import (
        load_physics_ir_goldens,
        verify_physics_ir_goldens,
    )

    return load_physics_ir_goldens, verify_physics_ir_goldens


def test_golden_loader_is_importable() -> None:
    load_physics_ir_goldens, verify_physics_ir_goldens = _load_api()
    assert callable(load_physics_ir_goldens)
    assert callable(verify_physics_ir_goldens)


def test_fixture_tree_loads_six_catalog_golden_ids() -> None:
    load_physics_ir_goldens, verify_physics_ir_goldens = _load_api()

    goldens = load_physics_ir_goldens(_FIXTURES)
    by_id = {golden.golden_id: golden for golden in goldens}

    assert set(by_id) == set(_EXPECTED_IDS)
    for golden_id in _EXPECTED_IDS:
        golden = by_id[golden_id]
        assert golden.family
        assert golden.required_structure
        assert golden.provenance_required is True
        assert golden.snapshot is not None
        assert golden.oracle_promoted is False

    assert verify_physics_ir_goldens(goldens) == []


def test_missing_provenance_in_snapshot_is_rejected() -> None:
    load_physics_ir_goldens, verify_physics_ir_goldens = _load_api()

    goldens = list(load_physics_ir_goldens(_FIXTURES))
    broken = goldens[0]
    # Replace with a snapshot that drops provenance for verifier coverage.
    from dataclasses import replace

    broken = replace(
        broken,
        snapshot={
            "family": broken.family,
            "structure": list(broken.required_structure),
            "source_origin": None,
        },
    )
    diagnostics = verify_physics_ir_goldens((broken, *goldens[1:]))
    assert any(
        diagnostic.get("code")
        in {"PHYSICS_IR_PROVENANCE_ERROR", "PHYSICS_IR_GOLDEN_ERROR"}
        for diagnostic in diagnostics
    ), diagnostics


def test_catalog_promotion_remains_gated() -> None:
    load_physics_ir_goldens, _ = _load_api()

    goldens = load_physics_ir_goldens(_FIXTURES)
    assert all(golden.oracle_promoted is False for golden in goldens)
    catalog = (_REPO / "docs" / "specs" / "staqex-v1-physics-ir-golden-catalog.md").read_text()
    assert "not a promoted runtime oracle" in catalog


if __name__ == "__main__":
    try:
        test_golden_loader_is_importable()
        test_fixture_tree_loads_six_catalog_golden_ids()
        test_missing_provenance_in_snapshot_is_rejected()
        test_catalog_promotion_remains_gated()
    except Exception as exc:
        print(f"RED (expected until Green): {type(exc).__name__}: {exc}")
        raise SystemExit(1) from exc
    print("OK — LISS-0117 Slice A")
    raise SystemExit(0)
