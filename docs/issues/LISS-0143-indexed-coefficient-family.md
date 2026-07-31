# LISS-0143: 1D `Float[N]` indexed coefficients (`J[i]`)

## Metadata

- Local issue ID: LISS-0143
- Status: **complete** — 2026-07-31
- Phase: Feature Path Red → Green → Refactor
- Type: Kernel surface
- Priority: P0 (WP-0032)
- Depends on: [LISS-0140](LISS-0140-binder-honesty.md); ADR 0096 1D coeff promotion
- Program: [WP-0032](../work-plans/WP-0032-adr-deferred-finite-slices.md)
- Implementation permission: **yes** (Adjudicator Plan 承認 2026-07-31)
- Branch: `feature/wp-0032-adr-deferred-finite`
- Tests: `tests/test_indexed_coefficient_family_red.py`

## Summary

1D classical coefficient families:

```staqex
Float[N] J = [a0, a1, /* … */, a_{N-1}];
Operator H = sum (i in Index<0..N-2>) { J[i] * Z[i] * Z[next(i)] }
```

Binder lowering substitutes literal coefficients. 2D tensors and Host arrays
remain deferred.

## Exit

- [x] Red/Green: TFIM-like indexed `J[i]` lowers; shape mismatch diagnosed
- [x] ADR 0096 Deferred list updated
