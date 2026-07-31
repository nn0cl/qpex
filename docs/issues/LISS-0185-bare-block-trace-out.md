# LISS-0185: Bare-block Trace-Out GC

## Metadata

- Local issue ID: LISS-0185
- Status: **complete**
- ADR: [0153](../architecture/adr/0153-bare-block-trace-out.md)
- Program: [WP-0059](../work-plans/WP-0059-bare-block-trace-out.md)
- Tests: `tests/test_bare_block_trace_out_red.py`

## Exit

- [x] Parse/typecheck/eval `BlockExpr`
- [x] Let temps traced out after block exit
- [x] Unrelated live coords preserved
- [x] Evolve Trace-Out regression green
