"""AT-TDD Phase 1 Red: LISS-0071 Slice C — close E-05 catalog gap."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from tests.spec_verification.harness.scenario_catalog import load_normative_rows

_PATH_TOKEN = re.compile(
    r"(?:docs|tests|examples)/[A-Za-z0-9_./\-]+\.(?:py|md|qpex)|"
    r"(?:docs|tests|examples)/[A-Za-z0-9_./\-]+"
)


def _e05_rows() -> list[dict[str, str]]:
    return [r for r in load_normative_rows() if r["envelope"] == "E-05"]


def _oracle_paths(oracle: str) -> list[str]:
    # Split on ';' then pull path-like tokens (ignore SV-NN labels).
    found: list[str] = []
    for part in oracle.split(";"):
        part = part.strip().strip("`")
        for m in _PATH_TOKEN.finditer(part):
            found.append(m.group(0).rstrip("/"))
    return found


def test_e05_has_no_gap_rows() -> None:
    gaps = [r["scenario_id"] for r in _e05_rows() if r["status"] == "gap"]
    assert not gaps, f"E-05 still has gap rows: {gaps}"


def test_e05_required_scenario_ids_present() -> None:
    ids = {r["scenario_id"] for r in _e05_rows()}
    for required in ("E05-001", "E05-002", "E05-003"):
        assert required in ids, f"missing {required} in E-05 catalog rows"


def test_e05_002_names_foreach_dynamic_bound_diagnostic() -> None:
    row = next(r for r in _e05_rows() if r["scenario_id"] == "E05-002")
    blob = f"{row['oracle']} {row.get('notes', '')}"
    assert "FOR_EACH_DYNAMIC_BOUND_ERROR" in blob


def test_e05_003_names_static_hilbert_resource_diagnostic() -> None:
    row = next(r for r in _e05_rows() if r["scenario_id"] == "E05-003")
    blob = f"{row['oracle']} {row.get('notes', '')}"
    assert "STATIC_HILBERT_RESOURCE_ERROR" in blob


def test_e05_covered_oracle_paths_exist() -> None:
    missing: list[str] = []
    for row in _e05_rows():
        if row["status"] != "covered":
            continue
        paths = _oracle_paths(row["oracle"])
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
    print("OK - LISS-0071 Slice C Phase 2 Green")
