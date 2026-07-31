# LISS-0146: Dependent / static Index endpoints

## Metadata

- Local issue ID: LISS-0146
- Status: **complete** — 2026-07-31
- Phase: Feature Path Red → Green
- Depends on: [ADR 0117](../architecture/adr/0117-binder-index-endpoints-and-rev.md) Accepted
- Program: [WP-0034](../work-plans/WP-0034-binder-endpoint-guards.md)
- Branch: `feature/wp-0034-binder-endpoint-guards`
- Tests: `tests/test_dependent_index_endpoints_red.py`

## Summary

`Index<a..b>` endpoints are static additive expressions (literals, outer
binders, register-size names, `+`/`-`) per ADR 0117.

## Exit

- [x] `Index<0..register-1>` and `Index<i+1..register-1>` lower
- [x] Negative endpoint → `BINDER_DOMAIN_ERROR`
