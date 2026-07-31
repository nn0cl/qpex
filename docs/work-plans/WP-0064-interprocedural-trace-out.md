# WP-0064: Interprocedural Trace-Out GC

| Field | Value |
|---|---|
| Status | **complete** (2026-07-31) |
| Branch | `feature/wp-0064-interprocedural-trace-out` |
| Parent | WP-0044 / ADR 0138 |

## Issue rows

| ID | Topic | Mode | Status |
|---|---|---|---|
| LISS-0191 | Post-Call caller dead-axis GC (ADR 0158) | ship | complete |

## Verification

- `python3 tests/test_interprocedural_trace_out_red.py`
- `python3 tests/test_trace_out_gc_fn_scope_red.py`
- `python3 tests/test_bare_block_trace_out_red.py`
- `python3 tests/test_evolve_trace_out_gc_red.py`
