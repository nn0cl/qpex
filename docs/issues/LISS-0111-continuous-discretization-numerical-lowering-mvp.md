# LISS-0111: Continuous discretization numerical lowering (MVP)

## Metadata

- Local issue ID: LISS-0111
- GitHub issue: none
- Status: proposed — awaiting plan approval and Phase 1 Red
- Phase: Feature Path (follow-up to LISS-0036)
- Type: Kernel lowering / scientific bridge
- Priority: P1
- Initial planning size: XL (MVP-narrowed)
- Parent batch: [LISS-0110](LISS-0110-pre-north-star-kernel-bump.md)
- Depends on: [LISS-0036](LISS-0036-continuous-operator-and-discretization-boundary.md), [ADR 0074](../architecture/adr/0074-explicit-discretization-contract.md)
- Related spec: [qpex-continuous-discretization.md](../specs/qpex-continuous-discretization.md)

## Summary

Lower a **named Bridge** (`use Grid for Theory.H as H_fd`) to a finite
`Operator` the Joint evaluator can evolve, using only the explicit
`discretization` contract fields. No backend may infer resolution, boundary, or
finite-difference order.

LISS-0036 completed the **honesty layer** (contract + Symbolic IR provenance).
This Issue completes the **execution layer** for one MVP path only.

## Proposed MVP slice (default — reviewable at Phase 1 Red)

- Domain: `Position`
- Basis: `UniformGrid`
- Boundary: `Periodic` (or `Dirichlet` if Red tests need a second case)
- Approximation: `FiniteDifference(order = 2)`
- Theory operator: 1D kinetic + potential form already used in pedagogy (parity
  with `tests/fixtures/qpex/grid_oscillator.qpex` intent, not necessarily the
  legacy `wavepacket` surface)
- Verification: measurement marginals vs hand-built finite matrix equivalent

## Non-goals

- `Momentum` / `PhaseAngle` / `FourierBasis` / `DVR` lowering in v1 of this
  Issue (future Issues).
- Adaptive meshes, implicit PDE solvers, or error-bound algorithms.
- QPU lowering of continuous bridges without an explicit finite register
  relation.
- Replacing existing finite-dimensional operators that do not use a Bridge.

## Acceptance notes (draft)

- [ ] Bridge alias resolves to a finite `Operator` with discretization metadata
      retained in IR or runtime provenance.
- [ ] Missing or incompatible contract fields remain hard diagnostics (reuse
      LISS-0036 codes where applicable).
- [ ] No silent grid creation for `continuous_operator` without a Bridge.
- [ ] Phase 1 Red scenarios approved before lowering code.

## Relationship to LISS-0036

```text
LISS-0036 (done)     : "We declare the grid honestly."
LISS-0111 (this)     : "We compute on that grid."
```

## Verification

- New Red module (name TBD at Phase 1), e.g. `test_continuous_lowering_red.py`.
- Regression: `test_continuous_discretization_red.py` unchanged assertions.
- Full SV after Green.
