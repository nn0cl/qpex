# Trace: LISS-0073 Slice E Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0073 |
| Slice | E — expression-side postfix `†` |
| Phase | phase-1-red |
| Branch | `feature/liss-0073-slice-e-red` |
| Implementation | **forbidden** until Red approval → Green |

## [DESIGN CHECK]

- Scope: Red assertions for `X†` → `Call(adjoint, [Var("X")])` on expression
  path; OpDSL dagger regression; EBNF note.
- Specs: Slice E plan approval; probe `PARSE_ERROR` on `state a = X†`.
- Verification: suite must fail before Green.

## Delivered

- `tests/test_dirac_slice_e_red.py`
- Issue / plan / open-work-register status → Slice E Red

## Expected Red

`PARSE_ERROR: unexpected token in expression: †` on expression-side `X†`.

## Next safe action

Adjudicator Red approval → Slice E Phase 2 Green.
