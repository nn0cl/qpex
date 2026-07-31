# LISS-0148: `Basis<N>` binder expansion

## Metadata

- Local issue ID: LISS-0148
- Status: **complete** — 2026-07-31
- Phase: Feature Path Red → Green
- Depends on: [ADR 0118](../architecture/adr/0118-basis-binder-and-partial-float.md) Accepted
- Program: [WP-0035](../work-plans/WP-0035-basis-and-partial-float.md)
- Branch: `feature/wp-0035-basis-and-partial-float`
- Tests: `tests/test_basis_binder_expansion_red.py`

## Summary

`sum` / `product` over `Basis<N>` enumerates computational-basis labels
`0..N-1` (and `rev(Basis<N>)` descending) per ADR 0118. Not an Index coercion.

## Exit

- [x] Red/Green: `sum (i in Basis<2>) { Z[i] }` lowers
- [x] EnergyLevel (or other deferred carrier) still `BINDER_DOMAIN_ERROR`
- [x] Honesty / ADR 0088 / 0096 docs synced
