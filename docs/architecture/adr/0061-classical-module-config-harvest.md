# ADR 0061: Classical module config harvest (companion to ADR 0054)

## Status

**Superseded** (2026-07-23) by ADR 0068. Adjudicator authorized Feature Path via
“ISSUE を消化して進めて” on the LISS-0003 ledger.

Amends / companions: [ADR 0054](0054-user-module-import.md).  
Follow-up Issue: [LISS-0005](../documentation-compression-map.md).
Parent: [LISS-0003](../documentation-compression-map.md).

## Context

ADR 0054 Decision §2 exported `Operator` binds from `pub fn` bodies and
Type-First `class` fields into entry `main`. Classical `Float` / `Int` binds in
library modules were ignored (11/12/14 sync comments).

## Dependency Adoption Evidence

Not applicable.

## Decision

**Historical decision:** candidate A harvested closed Type-First classical binds
(`Float`, `Int`, `Bool`) from `pub` `fn` bodies into the entry environment,
same prepend style as `Operator` harvest, subject to ADR 0058 visibility.

(`pub const` / candidate B deferred.)

1. Name collision with entry `main` binds → **hard diagnostic**
   `CONFIG_HARVEST_COLLISION_ERROR`.
2. Harvested classicals feed Joint const binds (and evaluator `scalars` via
   normal Type-First capture).
3. Operator and classical function-local harvest is removed by ADR 0068.
4. Short bind names from the library fn body are used (same as Operator).

## Consequences

Historical positive:

- Multi-file oracles/hints stop being comment-synced duplicates.

Historical negative:

- Candidate A may harvest scratch Floats inside helper `pub fn`s — prefer
  non-`pub` for scratch, or narrow later with candidate B.

## Historical enforcement

Code review should reject:

- New “Float not harvested; sync with main” comments without a deferred note.
- Harvesting `State` / non-closed expressions as classical config.
- Bypassing ADR 0058 visibility for module-private Floats.

## Historical verification

- Library `pub` Float appears in linked run; examples 11/12/14 updated.
- Full SV suite green.
