# Trace: LISS-0071 Slice A Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0071 |
| Path | Feature Path |
| Phase | Phase 1 Red (Slice A) |
| Branch | `feature/liss-0071-slice-a-red` |
| Production code | **none** (tests + docs only) |

## [DESIGN CHECK]

- Scope: Failing tests for DR-011 protocol index + report-drift API
  (`parse_args` / `emit_reports_if_requested`).
- Specs: approved `staqex-v1-conformance-plan.md` Slice A.
- Boundaries: no Green implementation; no catalog (Slice B).
- Verification: `python3 tests/test_conformance_slice_a_red.py` → 4 failures.

## Red evidence

- Protocol category table missing SV-19…SV-31
- SV-12 not explicitly marked absent
- `run_all.parse_args` / `emit_reports_if_requested` missing

## Next safe action

Adjudicator Red approval → Phase 2 Green.
