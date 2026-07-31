# LISS-0172: Deferred Pushforward MVP

## Metadata

- Local issue ID: LISS-0172
- Status: **complete**
- ADR: [0140](../architecture/adr/0140-deferred-pushforward-mvp.md)
- Program: [WP-0046](../work-plans/WP-0046-deferred-pushforward-mvp.md)
- Tests: `tests/test_deferred_pushforward_mvp_red.py`

## Exit

- [x] Eligible `StateBind* + measure` mains set `deferred_pushforward`
- [x] `inspect` forces eager path
- [x] Same seed → deferred measure matches eager measure
- [x] Dependency cone includes upstream binds
- [x] DAG lowerer still builds a measure node
