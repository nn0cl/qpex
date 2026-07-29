# ADR 0020: `map` / `given` / `fold` — pure stdlib; conditioning ≠ measure

## Status

**Superseded by ADR 0021** (normative names `project` / `interfer` / `System`).

Historical design baseline 2026-07-22. Semantic *laws* (pushforward;
restrict+renormalize ≠ measure; pure fold/combine; measure-free domain traits)
remain in force under the new spellings.

## Context

(See ADR 0021.)

## Decision

Historical:

1. `map` = pushforward.
2. Pure conditioning = restrict + renormalize (then named `given`).
3. Null event = domain error.
4. Conditioning ≠ `measure`.
5. `fold` = pure iterated `State` combine.
6. Domain traits measure-free.

## Consequences

Superseded for naming; see ADR 0021 and `staqex-stdlib-combinators.md`.
