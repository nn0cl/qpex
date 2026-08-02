# LISS-0277: S01 domain struct-first demotion

## Metadata

- Local issue ID: LISS-0277
- GitHub issue: _(none yet)_
- Status: **proposed**
- Phase: Feature examples
- Type: Feature Path
- Priority: P0
- Program: [WP-0089](../work-plans/WP-0089-surface-adoption-and-sugar.md)
- Depends: [LISS-0274](LISS-0274-wp-0089-program-lock.md); coordinate with [LISS-0276](LISS-0276-s01-import-use-lane-adoption.md)
- Paths: `examples/showcase/S01_quantum_disaster_response/domain/**`, consumers in mains/physics/protocol

## Summary

Apply Accepted struct-first teaching (LISS-0268 / harmony): pure parameter packs
and score bags become `struct`/`enum`; retain `class` only where the type is a
**physical or evolving system** (setup + Hamiltonian / multi-step board with
true system reading). Cut DTO `fn init` / `this` forests that read as Java beans.

## Problem

S01 domain is dominated by `pub class` + `fn init` (~25 inits) for tickets,
reports, observations — contradicts “class = physical system.”

## Exit

- [ ] Inventory: each domain type labeled **struct candidate** vs **keep class**
- [ ] Convert pure DTO/score packs to `struct` (or free data + pure fns)
- [ ] Keep class only with documented physics/system reading
- [ ] Call sites updated; seed-0 / S01 tests green
- [ ] No behavior change to Joint spine outcomes (same physics schedule)

## Non-goals

- Named struct sugar `{ field: … }` (LISS-0283) — positional struct OK until then
- Deleting domain coverage seats
- Host Python DTO redesign (LISS-0280 docs only)

## Adjudicator Decision Points

- Borderline types (e.g. boards with many pure methods): prefer struct + free fns
  unless ownership of evolving state is real

## Verification

- Before/after type table in Issue notes or short design comment
- S01 regression suite / seed-0
