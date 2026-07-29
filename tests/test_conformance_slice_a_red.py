"""AT-TDD Phase 1 Red: LISS-0071 Slice A — SV index sync + report drift."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

_PROTOCOL = _REPO / "docs" / "testing" / "staqex-spec-verification-protocol.md"
_SUITES_DIR = _REPO / "tests" / "spec_verification" / "suites"


def _shipped_sv_ids_from_harness() -> set[str]:
    ids: set[str] = set()
    for path in _SUITES_DIR.glob("sv*_*.py"):
        m = re.match(r"sv(\d+)_", path.name)
        assert m, path.name
        ids.add(f"SV-{int(m.group(1)):02d}")
    return ids


def test_protocol_category_table_lists_every_shipped_sv_suite() -> None:
    """DR-011: protocol category table must list every harness suite module."""
    text = _PROTOCOL.read_text(encoding="utf-8")
    listed = set(re.findall(r"\|\s*\*\*(SV-\d+)\*\*", text))
    shipped = _shipped_sv_ids_from_harness()
    missing = sorted(shipped - listed)
    assert not missing, f"protocol category table missing shipped suites: {missing}"


def test_protocol_explicitly_marks_sv12_absent() -> None:
    """SV-12 has no harness module; protocol must say so explicitly."""
    text = _PROTOCOL.read_text(encoding="utf-8").lower()
    assert "sv-12" in text
    assert any(
        marker in text
        for marker in (
            "sv-12 is absent",
            "sv-12 absent",
            "no sv-12",
            "sv-12 skipped",
            "sv-12 not shipped",
            "sv-12 gap",
        )
    ), "protocol must explicitly mark SV-12 as absent/skipped/gap"


def test_run_all_parse_args_default_write_report_false() -> None:
    """Local default: write_report=False; --write-report enables CI artifact write."""
    from tests.spec_verification import run_all

    parse = getattr(run_all, "parse_args", None)
    assert callable(parse), "run_all.parse_args(argv) must exist"
    assert parse([]).write_report is False
    assert parse(["--write-report"]).write_report is True


def test_emit_reports_if_requested_gates_write_reports() -> None:
    """emit_reports_if_requested must call write_reports only when write=True."""
    from tests.spec_verification import run_all
    from tests.spec_verification.harness.report import SuiteReport, write_reports

    gate = getattr(run_all, "emit_reports_if_requested", None)
    assert callable(gate), "run_all.emit_reports_if_requested(...) must exist"

    calls: list[object] = []
    original = write_reports

    def _fake_write(rep, out_dir):  # noqa: ANN001
        calls.append((rep, out_dir))
        return out_dir / "latest.json", out_dir / "latest.md"

    import tests.spec_verification.harness.report as report_mod

    report_mod.write_reports = _fake_write  # type: ignore[assignment]
    try:
        empty = SuiteReport(results=[])
        gate(empty, run_all.ROOT, write=False)
        assert calls == []
        gate(empty, run_all.ROOT, write=True)
        assert len(calls) == 1
    finally:
        report_mod.write_reports = original  # type: ignore[assignment]


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
    print("OK - LISS-0071 Slice A Phase 3 Refactor")
