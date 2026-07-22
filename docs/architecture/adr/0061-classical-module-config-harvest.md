# ADR 0061: Classical module config harvest (companion to ADR 0054)

## Status

**Proposed** (2026-07-23). Does **not** authorize implementation until Accepted.

Amends / companions: [ADR 0054](0054-user-module-import.md).  
Follow-up Issue: [LISS-0005](../../issues/LISS-0005-classical-module-config-harvest.md).  
Parent: [LISS-0003](../../issues/LISS-0003-examples-driven-kernel-brush-up.md).

## Context

ADR 0054 Decision §2 exports `Operator` binds from `public fun` bodies and
Type-First `class` fields into entry `main`. Classical `Float` / `Int` binds in
library modules are ignored. Multi-file examples therefore duplicate literals:

- `examples/11_shor_rsa_toy/operators/period_hints.qpex` — `Float r = 4.0`
  with comment “not linker-harvested; keep main in sync”
- `examples/12_…/operators/route_oracle.qpex`, `14_…/motif_oracle.qpex` — same
  pattern for oracle target index

Dream-skinned demos cannot treat `operators/` as real config modules.

## Dependency Adoption Evidence

Not applicable.

## Decision

*(Proposed — pending Adjudicator Accept; pick one surface at Accept)*

**Preferred candidate (A):** Harvest closed Type-First classical binds
(`Float`, `Int`, `Bool`, …) from `public` (and visibility-allowed) `fun`
bodies into the entry environment, same prepend style as `Operator` harvest,
subject to ADR 0058 visibility.

**Alternative (B):** Introduce explicit `pub const Name = …` (or `pub val` at
module scope) as the only harvested classical form — fun-local Floats remain
private implementation.

**Shared rules (either surface):**

1. Name collision with entry `main` binds → hard diagnostic (do not silently
   overwrite), unless Adjudicator prefers entry-wins.
2. Harvested classicals feed evaluator `scalars` and/or Joint const binds so
   `inspect` and `phase`/`times` (ADR 0060) can see them.
3. Operator harvest behavior from ADR 0054 remains unchanged.
4. Namespace-qualified export names are preserved or documented short-alias
   rules (Adjudicator at Accept).

## Consequences

Positive:

- Multi-file oracles/hints stop being comment-synced duplicates.
- Enables later “params → Operator” builders (SSH `SSHParams` → `Hssh`).

Negative:

- Larger merge surface; more collision diagnostics.
- Candidate A may over-harvest scratch Floats inside helper funs — mitigate
  with visibility or prefer B.

## Enforcement

Code review should reject:

- New example comments “Float not harvested; sync with main” after Accept +
  implement, without linking a deferred exception.
- Harvesting `State` / non-closed expressions as “classical config.”
- Bypassing ADR 0058 visibility to pull module-private Floats into another
  module’s main.

## Verification (when Accepted + implemented)

- Extend SV-31 (or sibling): library `pub` Float appears in linked run.
- Update examples 11/12/14 operator modules to consume harvest.
- Full SV suite green.
