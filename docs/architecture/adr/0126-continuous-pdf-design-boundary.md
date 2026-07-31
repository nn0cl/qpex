# ADR 0126: Continuous PDF / Monte Carlo — design boundary

## Status

**Accepted as design boundary** (2026-07-31) — LISS-0158 docs.

## Decision

1. Kernel mid-program values remain **finite-support** discrete carriers
   (NLTS / PMF). Continuous PDF is not a Kernel value type in this ADR.
2. Continuous models enter via Host / discretization ports that emit finite
   Kernel domains (existing discretization contracts).
3. Monte Carlo sampling is a Host/workflow concern, not a theory-lane loop.

## Non-goals

`Continuous` Kernel type; silent continuous→discrete truncation in theory.

Next design Issue (no Kernel Red):
[LISS-0195](../../issues/LISS-0195-host-mc-finite-state-design.md)
Host Monte Carlo → finite `State` injection sketch.
