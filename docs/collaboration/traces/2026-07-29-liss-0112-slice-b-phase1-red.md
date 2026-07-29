# Trace: LISS-0112 Slice B Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0112 |
| Slice | B — Identity evolve / apply(I) on D=3 |
| Phase | phase-1-red |
| Branch | `feature/liss-0112-slice-b-red` |
| Implementation | **forbidden** until Red approval → Green |

## [DESIGN CHECK]

- Scope: Red for Identity `apply(I)` / `evolve … under I` on
  `State<Qutrit>` / `State<Qudit<3>>` without `UNSUPPORTED_LOCAL_DIMENSION`;
  measure after Identity preserves `|2⟩` / `|1⟩` (dim-3). Non-Identity (`H`)
  and `Qudit<4>` remain fail-closed; qubit Identity unchanged. Exclude
  clock/shift, registers, Slice C.
- Specs: Slice B plan approval (“承認”); Slice A on `main` via PR #110.
- Verification: suite must fail before Green on new Identity cases.

## Delivered

- `tests/test_qudit_d3_sv_slice_b_red.py`

## Expected Red

`apply(I)` / `evolve under I` on `Qutrit` / `Qudit<3>` still
`UNSUPPORTED_LOCAL_DIMENSION`.

Regression (already Green): `apply(H)` unsupported; `Qudit<4>` unsupported;
qubit `apply(I)` OK.

## Next safe action

Adjudicator Red approval → Slice B Phase 2 Green.
