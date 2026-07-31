# LISS-0149: Partial Float classical indexing

## Metadata

- Local issue ID: LISS-0149
- Status: **complete** — 2026-07-31
- Phase: Feature Path Red → Green
- Depends on: [ADR 0118](../architecture/adr/0118-basis-binder-and-partial-float.md); LISS-0144
- Program: [WP-0035](../work-plans/WP-0035-basis-and-partial-float.md)
- Branch: `feature/wp-0035-basis-and-partial-float`
- Tests: `tests/test_partial_float_indexing_red.py`

## Summary

`Float[M…] row = h[i]` with static literal indices binds a remaining-shape
Kernel float tensor alias. Scalar binder coefficients still need full rank.

## Exit

- [x] Red/Green: classical partial bind + `row[q]` in binder
- [x] Binder `h[p] * Z[p]` remains unsupported
