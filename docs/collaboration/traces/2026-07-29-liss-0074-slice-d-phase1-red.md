# Trace: LISS-0074 Slice D Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0074 |
| Slice | D — hard unsupported qudit runtime |
| Phase | phase-1-red |
| Branch | `feature/liss-0074-slice-d-red` |
| Implementation | **forbidden** until Red approval → Green |

## [DESIGN CHECK]

- Scope: Red for `UNSUPPORTED_LOCAL_DIMENSION` on Qutrit/Qudit measure,
  QutritRegister evolve, apply on Qutrit; qubit carriers unchanged; no D=3 SV;
  exclude E.
- Specs: Slice D plan approval; probes show silent success today.
- Verification: suite must fail before Green on the new Red cases.

## Delivered

- `tests/test_qudit_slice_d_red.py`

## Expected Red

`State<Qutrit>` / `State<Qudit<3>>` measure, QutritRegister evolve, and apply
on Qutrit currently succeed without `UNSUPPORTED_LOCAL_DIMENSION`.

Regression (already Green): `State<Qubit>` measure unchanged.

## Next safe action

Adjudicator Red approval → Slice D Phase 2 Green.
