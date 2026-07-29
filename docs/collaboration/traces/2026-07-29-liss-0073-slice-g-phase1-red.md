# Trace: LISS-0073 Slice G Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0073 |
| Slice | G — formula→AST freeze + emit policy |
| Phase | phase-1-red |
| Branch | `feature/liss-0073-slice-g-red` |
| Implementation | **forbidden** until Red approval → Green |

## [DESIGN CHECK]

- Scope: Red proof suite for §4 rows + docs freeze assertions (no new sugar).
- Specs: Slice G plan approval.
- Verification: suite must fail before Green (provisional table / missing
  emit-policy section).

## Delivered

- `tests/test_dirac_slice_g_red.py`
- Issue / plan / open-work-register → Slice G Red

## Expected Red

`(if approved)` still present in §4; no dedicated formatter emit policy
heading.

## Next safe action

Adjudicator Red approval → Slice G Phase 2 Green (freeze docs + Issue complete).
