# LISS-0250: Kernel `measure … tracing_out …` — Red (ADR 0173)

## Metadata

- Local issue ID: LISS-0250
- Status: **in progress** — Phase 1 Red complete (awaiting Phase 2 Green)
- Phase: phase-1-red
- Type: Feature Path
- Priority: P1
- Planning size: M
- Design ADR: [0173](../architecture/adr/0173-measure-tracing-out-leftover-policy.md)
  (**Accepted**)
- Depends on: [LISS-0249](LISS-0249-adr-0173-measure-tracing-out.md) (**complete**)
- Branch: `feature/liss-0250-measure-tracing-out`
- Approval: Adjudicator「承認」(2026-08-02) — Phase 1 Red

## Intent

Ship ADR 0173 in the Shipping Kernel:

1. Grammar / AST: `measure <primary> tracing_out <name> [, <name> …]`
2. HIR LINEAR: listed leftovers consumed; unnamed live leftovers still
   `LINEAR_IMPLICIT_DISCARD`
3. Evaluator: Born `Joint.trace_out` of leftovers (source order), then existing
   primary measure (RngPort / MeasureSinkPort unchanged)
4. Companion: builtin `trace_out` Call always consumes its State argument for
   LINEAR (even Classical / placeholder bind)
5. Tests assert dialect ideal path and reject silent leftover discard /
   uncompute conflation

## Exit

- [x] Phase 1 Red: failing tests only (grammar + LINEAR + evaluator contract)
  — `tests/test_liss0250_measure_tracing_out_red.py` (7 failed, expected)
- [ ] Phase 2 Green: minimal implementation; no test edits to force pass
- [ ] Phase 3 Refactor + reviewer empathy
- [ ] SV / seed-0 regression green where applicable
- [ ] Follow-on or same Issue: S01 spine ritual `|0>` → `tracing_out` (may split)

## Non-goals

- Rest-sugar `tracing_out others` / `*`
- QPU / OpenQASM emitter behavior beyond fail-closed / deferred obligation
- Density-matrix CPTP Trace-Out (ADR 0057)
- Type-First fields ADR; failure glossary ADR
- Weakening terminal-measure / early-collapse rules

## Notes

Phase 1 Red evidence (`.venv/bin/pytest tests/test_liss0250_measure_tracing_out_red.py -q`):
all seven scenarios fail — parse gap for `tracing_out` clause; Classical-bound
`trace_out` still reports `LINEAR_IMPLICIT_DISCARD` on the State argument.
