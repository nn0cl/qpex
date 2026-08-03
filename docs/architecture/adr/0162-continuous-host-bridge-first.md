# ADR 0162: Continuous → finite via Host/Bridge (Kernel Continuous deferred)

## Status

**Accepted** (2026-07-31) — Architecture approval
([review](../../collaboration/reviews/2026-07-31-adr-0162-architecture-approval.md)).
Extends [ADR 0126](0126-continuous-pdf-design-boundary.md);
companions [ADR 0074](0074-explicit-discretization-contract.md),
[LISS-0195](../../issues/LISS-0195-host-mc-finite-state-design.md).

This ADR does **not** authorize Feature Path Red, Host adapter
implementation, or a Kernel `Continuous` value type.

## Context

Adjudicator discussion (2026-07-31): continuous distributions cannot ride a
gate-model QPU (or the NLTS Kernel joint) without an explicit finite
approximation. The preferred language stance is that **continuous and finite
are different types**, and the programmer must write the finiteization step
before Kernel execution / measurement / QPU lowering. Putting a mid-program
`Continuous` Kernel value first would be hard to narrow later; Host/Bridge
first stays reversible.

## Decisions

1. **Two type worlds.** Continuous carriers (PDF, continuous operators,
   continuous equations, Host Monte Carlo bags) are not Kernel mid-program
   values. Finite carriers (`State` / finite-support Joint) are the only
   values that enter measure, Joint eval, and QPU-bound paths.
2. **Programmer-written finiteization.** Continuous → finite must be an
   explicit step the programmer (or Host adapter they invoke) writes —
   discretization contract ([ADR 0074](0074-explicit-discretization-contract.md)),
   Host Monte Carlo → finite `State` inject, or an accepted Bridge form.
   Silent backend grids / silent theory-lane truncation remain forbidden.
3. **Host / Bridge first.** The authorized evolution path is:
   continuous (Host or Theory notation) → explicit finiteization → finite
   Kernel `State`. Prefer ports and Bridge over new Kernel syntax until the
   inject surface is concrete (LISS-0195).
4. **Kernel `Continuous` deferred; finiteize surface unsealed separately.**
   A mid-program `Continuous` type still requires a **future** ship ADR after
   Host/Bridge is specified (and now after Lane A proves demand). Notebook
   **finiteize** Call (finite State result only) is unsealed by
   [ADR 0185](0185-kernel-continuous-value.md) **Accepted** Lane A — not a
   Continuous type world. Type gate remains: no measure / no QPU on continuous
   description without explicit finiteization.
5. **Reversibility.** Host/Bridge choices may be refined cheaply. Narrowing
   or removing a shipped Kernel `Continuous` mid-program meaning is treated
   as breaking and is out of scope for opportunistic sugar.

## Non-goals

- Implementing Host Monte Carlo adapters or Kernel Red in this ADR
- Selecting a cloud / HPC Monte Carlo SDK (technology selection separate)
- Replacing ADR 0074 discretization fields
- Authorizing Joint rational masses or CUDA (unrelated)

## Consequences

- ADR 0126 remains the design boundary against Kernel `Continuous` values;
  this ADR records the **preferred unseal path** (Host/Bridge) when continuous
  workflows are ready.
- LISS-0195 proceeds as design of Host MC → finite `State` injection under
  these constraints; a later ship ADR is still required before Red.
- Agents must not invent Kernel continuous syntax or silent finiteization.
