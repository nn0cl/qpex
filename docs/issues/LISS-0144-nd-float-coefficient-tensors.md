# LISS-0144: ND `Float[N][M]…` coefficient tensors

## Metadata

- Local issue ID: LISS-0144
- Status: **complete** — 2026-07-31
- Phase: Feature Path Red → Green → Refactor
- Type: Kernel surface
- Priority: P0 (WP-0033)
- Depends on: [LISS-0143](LISS-0143-indexed-coefficient-family.md); ADR 0096 ND Accepted
- Program: [WP-0033](../work-plans/WP-0033-nd-float-coefficient-tensors.md)
- Implementation permission: **yes** (Adjudicator Plan 承認 2026-07-31)
- Branch: `feature/liss-0144-nd-float-coeffs`
- Tests: `tests/test_nd_float_coefficient_tensors_red.py`

## Summary

Extend 1D `Float[N]` to Kernel-literal ND tensors with full-rank chained
indexing in binders. Host tensors remain deferred.

## Exit

- [x] Red/Green: 2D + 4D smoke; shape/arity mismatch; 1D regression
- [x] ADR 0096 + register/friction updated
- [ ] PR merge review
