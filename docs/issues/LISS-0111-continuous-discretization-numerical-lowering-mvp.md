# LISS-0111: Continuous discretization numerical lowering (MVP)

## Metadata

- Local issue ID: LISS-0111
- GitHub issue: none
- Status: **Phase 3 reviewed** (2026-07-27) — MVP lowering shipped
- Phase: Feature Path (follow-up to LISS-0036)
- Type: Kernel lowering / scientific bridge
- Priority: P1
- Initial planning size: XL (MVP-narrowed)
- Parent batch: [LISS-0110](../architecture/documentation-compression-map.md)
- Depends on: [LISS-0036](LISS-0036-continuous-operator-and-discretization-boundary.md), [ADR 0074](../architecture/adr/0074-explicit-discretization-contract.md)
- Related spec: [staqex-continuous-discretization.md](../specs/staqex-continuous-discretization.md)

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
  with `tests/fixtures/staqex/grid_oscillator.staqex` intent, not necessarily the
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

- [x] Bridge alias resolves to a finite `Operator` with discretization metadata
      retained in IR or runtime provenance.
- [x] Missing or incompatible contract fields remain hard diagnostics (reuse
      LISS-0036 codes where applicable).
- [x] No silent grid creation for `continuous_operator` without a Bridge.
- [x] Phase 1 Red scenarios approved before lowering code.

## Relationship to LISS-0036

```text
LISS-0036 (done)     : "We declare the grid honestly."
LISS-0111 (this)     : "We compute on that grid."
```

## Verification

- New Red module `tests/test_continuous_lowering_red.py`.
- Regression: `test_continuous_discretization_red.py` unchanged assertions.
- Full SV after Green: **160/160** (2026-07-27).

## Implementation record

- `compiler/staqex/continuous_lowering.py` — `lower_discretization_bridges()` produces
  sealed `GridHamiltonian` values on `[-π, π)` uniform periodic grids.
- `compiler/staqex/pipeline.py` — `CompileResult.grid_hamiltonians` populated at
  analysis time; non-MVP contracts emit `DISCRETIZATION_LOWERING_ERROR`.
- `compiler/staqex/runtime/evaluator.py` — `GridHamiltonianRef` bridge aliases
  evolve via precomputed matrices when state abscissae match the lowered grid.
- `wavepacket(-pi, pi, N, …)` must align abscissae with the lowered grid.
- Tests: `tests/test_continuous_lowering_red.py`.
