# LISS-0310: LINEAR uncompute pedagogy (`tracing_out`)

## Metadata

- Local issue ID: LISS-0310
- Status: **complete** (2026-08-03)
- Type: Feature examples + docs (no Kernel change)
- Priority: P2 residual (language re-review §5.4)
- Depends: ADR 0173 / LISS-0250–0252 (`measure … tracing_out …` shipped)
- Branch: `feature/liss-0310-linear-uncompute-pedagogy`
- Authority: Adjudicator residual continue after LISS-0309

## Problem

Official applied / basics / QMD samples still taught LINEAR discharge as ritual
`state sibling = |0>` (or vacuum) before a singular `measure`. That contradicts
the accepted minimal dialect and ADR 0173 pedagogy: leftovers leave via
explicit partial trace on the terminal measure.

## Scope

Convert legal hand-kill sites to:

```text
measure <primary> tracing_out <leftover> [, <leftover> ...]
```

Touched mains (incremental pass):

- Showcase: QMD, S01 `main_comms_channel`
- Applied: A01–A05, A07–A10
- Basics: B09, B11, B12, B15
- Docs: `surface-style-guide.md` §6a; re-review residual mark

Out of scope:

- Kernel / HIR / evaluator changes
- True ADR 0107 computational-basis uncompute witnesses (none in this pass)
- Bulk rewrite of fixture tests that intentionally demonstrate `|0>` rebind
- P3 Open Topics (Continuous / display-unit / QPU / trait)

## Exit

- [x] All listed mains seed-0 green
- [x] A08 QASM smoke still valid
- [x] Style guide + re-review residual updated
- [x] Trace under `docs/collaboration/traces/`

## Notes

Several former hand-kills were **ritual re-introductions** of `|0>` after the
root was already moved by `cnot` / `capply` / walk / `lindblad`. Those become
plain `measure primary` (no `tracing_out`). Only still-live leftovers go in
the `tracing_out` list.
