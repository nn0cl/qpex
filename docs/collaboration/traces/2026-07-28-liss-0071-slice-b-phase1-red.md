# Trace: LISS-0071 Slice B Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0071 |
| Path | Feature Path |
| Phase | Phase 1 Red (Slice B) |
| Branch | `feature/liss-0071-slice-b-red` |
| Production code | **none** (tests + docs only) |

## [DESIGN CHECK]

- Scope: Failing tests for normative catalog section, schema, E-01…E-14
  presence, gap/deferred notes, published Status field.
- Specs: approved scenario catalog companion.
- Boundaries: no Green catalog publish yet.
- Verification: `python3 tests/test_conformance_slice_b_red.py` → 4 failures.

## Next safe action

Adjudicator Red approval → Phase 2 Green.
