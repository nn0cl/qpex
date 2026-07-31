# WP-0059: Bare-block Trace-Out GC

| Field | Value |
|---|---|
| Status | **complete** (2026-07-31) |
| Branch | `feature/wp-0059-bare-block-trace-out` |
| Parent | WP-0048 / ADR 0142 |

## Issue rows

| ID | Topic | Mode | Status |
|---|---|---|---|
| LISS-0185 | Bare `BlockExpr` Trace-Out (ADR 0153) | ship | complete |

## Verification

- `python3 tests/test_bare_block_trace_out_red.py`
- `python3 tests/test_evolve_trace_out_gc_red.py`
