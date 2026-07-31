# LISS-0170: Trace-Out GC MVP for library `fn` scopes

## Metadata

- Local issue ID: LISS-0170
- Status: **complete**
- ADR: [0138](../architecture/adr/0138-trace-out-gc-fn-scope.md)
- Program: [WP-0044](../work-plans/WP-0044-trace-out-gc-mvp.md)
- Tests: `tests/test_trace_out_gc_fn_scope_red.py`

## Exit

- [x] After `r = f(x)` with param `y`, joint keeps `x`/`r` and drops `y`
- [x] Caller-live coordinates are never traced out by the Call
