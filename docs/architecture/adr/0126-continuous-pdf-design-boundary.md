# ADR 0126: Continuous PDF / Monte Carlo — design boundary

## Status

**Accepted as design boundary** (2026-07-31) — LISS-0158 docs.
Strategy lock for how to evolve past this boundary:
[ADR 0162](0162-continuous-host-bridge-first.md) (**Accepted**, Architecture
approval — Host/Bridge first; Kernel `Continuous` deferred).

## Decision

1. Kernel mid-program values remain **finite-support** discrete carriers
   (NLTS / PMF). Continuous PDF is not a Kernel value type in this ADR.
2. Continuous models enter via Host / discretization ports that emit finite
   Kernel domains (existing discretization contracts).
3. Monte Carlo sampling is a Host/workflow concern, not a theory-lane loop.

## Non-goals

`Continuous` Kernel type; silent continuous→discrete truncation in theory.

## Evolution (Adjudicator 2026-07-31)

Prefer **Host / Bridge + programmer-written finiteization** over introducing a
Kernel mid-program `Continuous` value. Continuous and finite stay different
types; execution / QPU paths accept only finite `State`. See ADR 0162.

Next design Issue (no Kernel Red):
[LISS-0195](../../issues/LISS-0195-host-mc-finite-state-design.md)
Host Monte Carlo → finite `State` injection sketch under ADR 0162.

**2026-08-03:** Host inject shipped (0163/0164). Notebook **finiteize**
surface (still no mid-program Continuous type) is [ADR 0185](0185-kernel-continuous-value.md)
**Accepted** Lane A; Feature [LISS-0313](../../issues/LISS-0313-finiteize-surface.md).
