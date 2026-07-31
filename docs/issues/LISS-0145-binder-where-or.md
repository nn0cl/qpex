# LISS-0145: Binder `where ||`

## Metadata

- Local issue ID: LISS-0145
- Status: **complete** — 2026-07-31
- Phase: Feature Path Red → Green
- Depends on: ADR 0098 D2 extension; LISS-0141 `&&`
- Program: [WP-0034](../work-plans/WP-0034-binder-endpoint-guards.md)
- Branch: `feature/wp-0034-binder-endpoint-guards`
- Tests: `tests/test_binder_where_or_red.py`

## Summary

Binder `where` accepts `||` with lower precedence than `&&`. Statement-level
`||` remains forbidden.

## Exit

- [x] Red/Green: `where i < j || j == 0` lowers; statement `||` still errors
- [x] ADR 0098 updated
