# ADR 0057 density / Lindblad — v1 showcase boundary

| Field | Value |
|---|---|
| Status | **Accepted** (2026-07-31) — Adjudicator Option B §7: **boundary doc only** |
| Issue | [LISS-0131](../issues/LISS-0131-density-lindblad-showcase-boundary.md) |
| ADR | [0057](../architecture/adr/0057-density-cptp-lindblad.md) |
| Program | [open-topics-before-s1-program](staqex-v1-open-topics-before-s1-program.md) |
| Not | Full CPTP completeness claim; new Kernel slices without named Issues |

## Decision

For the locked quantum-matter / Noether Forge showcase (P2):

1. **Do not** require general Lindblad CPTP / adaptive integration / positivity
   projection / QPU open-system execution before S1.
2. **Allowed:** optional toy / partial density use (e.g. A07 lineage) when the
   mission spine needs an honest mixed-state illustration.
3. **Required honesty:** source and docs must not claim general open-system
   completeness.
4. **Kernel gaps** named in open-work (adaptive integration, positivity
   projection, QPU execution, Channel reuse / symbolic jumps beyond shipped
   slices) remain **deferred** — not Option B ship items.

## Coverage ledger

ADR 0057 row stays **partial** / showcase **optional** until a future Issue
explicitly promotes a named slice.
