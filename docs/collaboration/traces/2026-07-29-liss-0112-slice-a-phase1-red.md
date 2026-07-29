# Trace: LISS-0112 Slice A Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0112 |
| Slice | A — D=3 ket + measure |
| Phase | phase-1-red |
| Branch | `feature/liss-0112-slice-a-red` |
| Implementation | **forbidden** until Red approval → Green |

## [DESIGN CHECK]

- Scope: Red for `|0⟩…|2⟩` measure on `State<Qutrit>` / `Qudit<3>` without
  `UNSUPPORTED_LOCAL_DIMENSION`; `|2⟩` proves dim-3; `Qudit<4>` and `|3⟩`
  remain fail-closed; qubit unchanged. Exclude Identity evolve (B), closeout (C).
- Specs: plan approval (“承認”); PR #109 merged.
- Verification: suite must fail before Green on new Red cases.

## Delivered

- `tests/test_qudit_d3_sv_slice_a_red.py`

## Expected Red

`State<Qutrit>` / `Qudit<3>` measure (incl. `|2⟩`) still
`UNSUPPORTED_LOCAL_DIMENSION`.

Regression (already Green): `Qudit<4>` unsupported; `|3⟩` type error; qubit OK.

## Note

LISS-0074 Slice D Red asserts measure-is-unsupported; Green of 0112 Slice A
must update those assertions to match the intentional lift for D=3 measure.

## Next safe action

Adjudicator Red approval → Slice A Phase 2 Green.
