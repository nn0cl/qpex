# LISS-0141: Compound binder `where` (`&&`)

## Metadata

- Local issue ID: LISS-0141
- Status: **complete** — 2026-07-31
- Phase: Feature Path Red → Green → Refactor
- Type: Kernel surface
- Priority: P0 (WP-0032)
- Depends on: [LISS-0140](LISS-0140-binder-honesty.md); ADR 0098 D2 extension
- Program: [WP-0032](../work-plans/WP-0032-adr-deferred-finite-slices.md)
- Implementation permission: **yes** (Adjudicator Plan 承認 2026-07-31)
- Branch: `feature/wp-0032-adr-deferred-finite`
- Tests: `tests/test_binder_compound_where_red.py`

## Summary

Static binder guards accept left-associative `&&` chains. Classical
statement-level `&&` remains forbidden (F-01); only `where` predicates
accept `&&`.

## Exit

- [x] Red/Green: `where i < j && j < k` expands and lowers
- [x] Statement `&&` still errors
- [x] ADR 0098 + friction ledger note
