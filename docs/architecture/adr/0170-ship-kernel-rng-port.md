# ADR 0170: Ship Kernel `RngPort` (first slice of ADR 0166)

## Status

**Accepted** (2026-08-02) — WP-0081 intake / [LISS-0235](../documentation-compression-map.md)
Adjudicator lock (Accept 0170). Shipped on [WP-0082](../../work-plans/WP-0082-kernel-rng-port.md)
(`RngPort` + `StdlibRngAdapter`; evaluator no longer constructs `random.Random`).

## Context

[ADR 0166](0166-kernel-external-resource-ports.md) (**Accepted**) requires
Kernel entropy behind `RngPort`, with bit-identical seeded outputs, separate
from `HostRngPort`, and slice order `RngPort` → `MeasureSinkPort` →
`SourcePort`. Design ADR forbids Red without a separate ship authorization.

## Dependency Adoption Evidence

Not applicable. Default adapter wraps stdlib `random.Random`.

## Decision

1. Authorize Feature Path AT-TDD for [LISS-0235](../documentation-compression-map.md)
   to introduce `RngPort` + default adapter and inject it into the Joint
   evaluator `measure` path.
2. **Determinism is binding:** seeded outputs (`--seed 0`, SV, published
   examples) must be **bit-identical** before/after; prove by output diff, not
   assertion alone.
3. Do **not** unify with `HostRngPort` in this ship.
4. Do **not** construct `random.Random` inside the evaluator after this ship
   lands (adapter owns construction).
5. `MeasureSinkPort` / `SourcePort` remain out of scope (follow-on Issues).

## Consequences

Positive: closes the first External-Resources contract gap with a pinned seed
contract.

Negative: evaluator construction sites change; determinism regressions are
expensive.

## Enforcement

Code review should reject seed-changing refactors, Host/Kernel RNG unification,
and sneaking sink/source ports into this Issue.
