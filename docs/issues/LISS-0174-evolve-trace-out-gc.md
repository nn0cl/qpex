# LISS-0174: Trace-Out GC for block `evolve`

## Metadata

- Local issue ID: LISS-0174
- Status: **complete**
- ADR: [0142](../architecture/adr/0142-evolve-trace-out-gc.md)
- Program: [WP-0048](../work-plans/WP-0048-evolve-trace-out-gc.md)
- Tests: `tests/test_evolve_trace_out_gc_red.py`

## Exit

- [x] Evolve `let` temps are absent from the joint after exit
- [x] Caller-live coordinates remain
- [x] Multi-step evolve still drops lets; measure denotation preserved
