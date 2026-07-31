# LISS-0147: `rev` binder domains

## Metadata

- Local issue ID: LISS-0147
- Status: **complete** — 2026-07-31
- Phase: Feature Path Red → Green
- Depends on: [ADR 0117](../architecture/adr/0117-binder-index-endpoints-and-rev.md); LISS-0146
- Program: [WP-0034](../work-plans/WP-0034-binder-endpoint-guards.md)
- Branch: `feature/wp-0034-binder-endpoint-guards`
- Tests: `tests/test_rev_binder_domain_red.py`

## Summary

`rev(Index<a..b>)` enumerates the inclusive domain in descending order when
non-empty (ADR 0117 D5).

## Exit

- [x] Red/Green: descending expansion for `rev(Index<0..2>)`
- [x] Empty ascending domain stays empty under `rev`
