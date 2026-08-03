# LISS-0311: B06 Type-First leftover pedagogy (`tracing_out`)

## Metadata

- Local issue ID: LISS-0311
- Status: **complete** (2026-08-03)
- Type: Feature examples + docs (no Kernel change)
- Priority: P2 residual (follow-on to LISS-0310)
- Depends: ADR 0173; LISS-0310 LINEAR leftover pedagogy
- Branch: `feature/liss-0311-b06-type-first-tracing-out`
- Authority: Adjudicator「1」(B06 classical vacuum residual)

## Problem

B06 discharged Type-First `State<Time|Mass|Stiffness|Momentum>` leftovers with
ritual `state … = vacuum` before `measure viewed`. Those are still-live
**linear State** carriers with dimensions — not classical Floats — so the
correct dialect story is the same as LISS-0310:

```text
measure viewed tracing_out dt, m, k, p
```

## Scope

- Convert B06 main to `tracing_out`
- README / catalog honesty if the vacuum story is still taught
- Trace

Out: Kernel changes; B06 feature expansion (classical Type-First heads in
State arithmetic remain a language follow-up note in the source comment).

## Exit

- [x] B06 seed-0 green
- [x] No vacuum hand-kill before measure in B06
- [x] Issue + trace
