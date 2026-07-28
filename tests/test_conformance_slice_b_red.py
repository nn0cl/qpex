"""AT-TDD Phase 1 Red: LISS-0071 Slice B — conformance scenario catalog."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from tests.spec_verification.harness.scenario_catalog import (
    ENVELOPES,
    SCENARIO_ID,
    STATUSES,
    TAXONOMY,
    catalog_path,
    load_normative_rows,
    normative_section,
    parse_rows,
    status_field,
)


def test_catalog_has_normative_section_with_schema() -> None:
    rows = load_normative_rows()
    for row in rows:
        assert SCENARIO_ID.match(row["scenario_id"]), row["scenario_id"]
        assert row["envelope"] in ENVELOPES, row["envelope"]
        assert row["class"] in TAXONOMY, row["class"]
        assert row["status"] in STATUSES, row["status"]
        assert row["oracle"], "oracle required"


def test_catalog_covers_every_envelope_e01_through_e14() -> None:
    present = {row["envelope"] for row in load_normative_rows()}
    missing = [e for e in ENVELOPES if e not in present]
    assert not missing, f"envelopes missing from normative catalog: {missing}"


def test_gap_and_deferred_rows_have_notes() -> None:
    text = catalog_path().read_text(encoding="utf-8")
    section = normative_section(text)
    lines = [ln.strip() for ln in section.splitlines() if ln.strip().startswith("|")]
    header = [c.strip().strip("`") for c in lines[0].strip("|").split("|")]
    assert "notes" in header, "notes column required for gap/deferred rationale"
    for row in parse_rows(section):
        if row["status"] in {"gap", "deferred"}:
            assert row.get("notes", "").strip(), f"{row['scenario_id']} needs notes"


def test_catalog_status_field_is_published_not_plan_proposed() -> None:
    status = status_field(catalog_path().read_text(encoding="utf-8")).lower()
    assert "plan proposed" not in status
    assert "awaiting" not in status


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
    print("OK - LISS-0071 Slice B Phase 3 Refactor")
