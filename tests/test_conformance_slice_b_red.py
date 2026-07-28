"""AT-TDD Phase 1 Red: LISS-0071 Slice B — conformance scenario catalog."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

_CATALOG = _REPO / "docs" / "specs" / "qpex-v1-conformance-scenario-catalog.md"
_ENVELOPES = [f"E-{n:02d}" for n in range(1, 15)]
_TAXONOMY = {"valid", "invalid", "semantic", "numerical", "provenance", "backend"}
_STATUSES = {"covered", "gap", "deferred"}
_SCENARIO_ID = re.compile(r"^E\d{2}-\d{3}$")


def _normative_section(text: str) -> str:
    """Return the ## Catalog (Normative) section body (until next ##)."""
    m = re.search(
        r"^## Catalog \(Normative\)\s*\n(.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert m, "catalog must contain a '## Catalog (Normative)' section"
    return m.group(1)


def _parse_rows(section: str) -> list[dict[str, str]]:
    lines = [ln.strip() for ln in section.splitlines() if ln.strip().startswith("|")]
    assert len(lines) >= 2, "normative catalog table missing"
    header = [c.strip().strip("`") for c in lines[0].strip("|").split("|")]
    required = ["scenario_id", "envelope", "class", "oracle", "status"]
    for col in required:
        assert col in header, f"missing column {col!r} in {header}"
    # skip separator row
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < len(header):
            continue
        row = {header[i]: cells[i] for i in range(len(header))}
        if row.get("scenario_id", "").startswith("scenario_id"):
            continue
        rows.append(row)
    assert rows, "normative catalog has no data rows"
    return rows


def test_catalog_has_normative_section_with_schema() -> None:
    text = _CATALOG.read_text(encoding="utf-8")
    section = _normative_section(text)
    rows = _parse_rows(section)
    for row in rows:
        assert _SCENARIO_ID.match(row["scenario_id"]), row["scenario_id"]
        assert row["envelope"] in _ENVELOPES, row["envelope"]
        assert row["class"] in _TAXONOMY, row["class"]
        assert row["status"] in _STATUSES, row["status"]
        assert row["oracle"], "oracle required"


def test_catalog_covers_every_envelope_e01_through_e14() -> None:
    text = _CATALOG.read_text(encoding="utf-8")
    rows = _parse_rows(_normative_section(text))
    present = {row["envelope"] for row in rows}
    missing = [e for e in _ENVELOPES if e not in present]
    assert not missing, f"envelopes missing from normative catalog: {missing}"


def test_gap_and_deferred_rows_have_notes() -> None:
    text = _CATALOG.read_text(encoding="utf-8")
    section = _normative_section(text)
    lines = [ln.strip() for ln in section.splitlines() if ln.strip().startswith("|")]
    header = [c.strip().strip("`") for c in lines[0].strip("|").split("|")]
    assert "notes" in header, "notes column required for gap/deferred rationale"
    rows = _parse_rows(section)
    for row in rows:
        if row["status"] in {"gap", "deferred"}:
            assert row.get("notes", "").strip(), f"{row['scenario_id']} needs notes"


def test_catalog_status_field_is_published_not_plan_proposed() -> None:
    text = _CATALOG.read_text(encoding="utf-8")
    # Front-matter Status row must not remain plan-proposed after Green.
    m = re.search(r"\|\s*Status\s*\|\s*(.*?)\s*\|", text)
    assert m, "Status field missing"
    status = m.group(1).lower()
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
    print("OK - LISS-0071 Slice B Phase 2 Green")
