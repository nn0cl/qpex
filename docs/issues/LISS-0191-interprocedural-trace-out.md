# LISS-0191: Post-Call caller dead-axis Trace-Out

## Metadata

- Local issue ID: LISS-0191
- Status: **complete**
- ADR: [0158](../architecture/adr/0158-interprocedural-trace-out.md)
- Program: [WP-0064](../work-plans/WP-0064-interprocedural-trace-out.md)
- Tests: `tests/test_interprocedural_trace_out_red.py`
- Extends: LISS-0170 / ADR 0138

## Exit

- [x] After library Call in eligible `main`, dead caller axes are traced out
- [x] Live caller axes used by later stmts / measure are preserved
- [x] Fn-local GC (ADR 0138) regressions remain green
- [x] Deferred Pushforward path also applies post-Call GC
