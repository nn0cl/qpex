# LISS-0163: Stepwise Partial fill

## Metadata

- Local issue ID: LISS-0163
- Status: **complete**
- ADR: [0131](../architecture/adr/0131-stepwise-partial-fill.md)
- Program: [WP-0040](../work-plans/WP-0040-stepwise-partial-ev.md)
- Tests: `tests/test_stepwise_partial_fill_red.py`

## Exit

- [x] `p2(b)` with two holes remaining yields Partial `#1`
- [x] Over-arity Call on Partial diagnoses `FUNCTION_ARITY_ERROR`
