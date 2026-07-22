# ADR 0021: Normative stdlib names — `map` / `project` / `interfer` and `trait System`

## Status

Accepted (2026-07-22).  
Supersedes naming in ADR 0020 (`given` / `fold` / `QSystem`).

Design notes: `qpex-stdlib-combinators.md`, formal semantics §Project / §Interfer.

## Context

Collection metaphors (`filter`, `fold`) clash with the quantum narrative.
Adjudicator-facing sync chose physics-native names: **`project`** (subspace
projection + renormalize) and **`interfer`** (combine / interfere states).
Domain trait naming unifies on **`System`**, pairing the `system` keyword.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. **`map`**: unchanged — pushforward on supports; no RNG.
2. **`project`**: restrict support by predicate, then renormalize. Primary
   normative name. Former names `given` / `where` / `restrict` / `filter` are
   **retired aliases** (docs may mention migration only).
3. **`project` ≠ `measure`**: no sampling; multi-atom support may remain.
4. **Null event** after projection ($Z=0$): → **`Vacuum`** (ADR 0026);
   not a domain exception.
5. **`interfer`**: pure iterated combine of a list of `State<_>` into one
   `State<_>` (independent product + pushforward of combiner by default).
   Former name `fold` is retired as the normative spelling.
6. **`interfer` signature** threads `State<Acc>` (init lifts to Dirac); do not
   sample carrier `T` out of each element.
7. Domain capability name is **`System`** (`fun step(self) -> Self`;
   surface `interface System` per ADR 0024). `QSystem` /
   `Evolvable` are retired synonyms in normative docs.
8. Still not required for Kernel PoC A/B.

## Consequences

Positive:

- Narrative alignment with projection / interference.
- One trait name matching `system` capsules.

Negative:

- Short migration from ADR 0020 spellings in existing notes.

## Enforcement

Reject normative examples that prefer `filter`/`fold`/`QSystem` over
`project`/`interfer`/`System`, or that equate `project` with `measure`.
