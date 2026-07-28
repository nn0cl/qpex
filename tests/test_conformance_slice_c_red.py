"""AT-TDD Phase 1 Red: LISS-0071 Slice C — close E-05 catalog gap."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from tests.spec_verification.harness.scenario_catalog import (
    oracle_paths,
    row_by_scenario_id,
    rows_for_envelope,
)


def test_e05_has_no_gap_rows() -> None:
    gaps = [r["scenario_id"] for r in rows_for_envelope("E-05") if r["status"] == "gap"]
    assert not gaps, f"E-05 still has gap rows: {gaps}"


def test_e05_required_scenario_ids_present() -> None:
    ids = {r["scenario_id"] for r in rows_for_envelope("E-05")}
    for required in ("E05-001", "E05-002", "E05-003"):
        assert required in ids, f"missing {required} in E-05 catalog rows"


def test_e05_002_names_foreach_dynamic_bound_diagnostic() -> None:
    row = row_by_scenario_id("E05-002")
    blob = f"{row['oracle']} {row.get('notes', '')}"
    assert "FOR_EACH_DYNAMIC_BOUND_ERROR" in blob


def test_e05_003_names_static_hilbert_resource_diagnostic() -> None:
    row = row_by_scenario_id("E05-003")
    blob = f"{row['oracle']} {row.get('notes', '')}"
    assert "STATIC_HILBERT_RESOURCE_ERROR" in blob


def test_e05_covered_oracle_paths_exist() -> None:
    missing: list[str] = []
    for row in rows_for_envelope("E-05"):
        if row["status"] != "covered":
            continue
        paths = oracle_paths(row["oracle"])
        assert paths, f"{row['scenario_id']} covered but no filesystem oracle path"
        for rel in paths:
            if not (_REPO / rel).exists():
                missing.append(f"{row['scenario_id']}:{rel}")
    assert not missing, f"missing oracle paths: {missing}"


if __name__ == "__main__":
    failures = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except Exception as exc:  # noqa: BLE001 — Red harness
                failures += 1
                print(f"FAIL {name}: {type(exc).__name__}: {exc}")
    if failures:
        raise SystemExit(f"Red confirmed: {failures} failure(s)")
    print("OK - LISS-0071 Slice C Phase 3 Refactor")
