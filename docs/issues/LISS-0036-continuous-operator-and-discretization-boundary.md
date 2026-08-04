# LISS-0036: Continuous operators and discretization boundary

- Status: **Phase 3 reviewed** (explicit Theory-to-Kernel Bridge; MVP numerical
  lowering shipped via [LISS-0111](LISS-0111-continuous-discretization-numerical-lowering-mvp.md))
- Depends on: LISS-0018, LISS-0033, ADR 0069
- Blocks: direct source coverage for continuous-space models
- Architecture decision: [ADR 0074](../architecture/decision-themes/dec-0004-type-first-scientific-model.md)
- Acceptance specification: [`staqex-continuous-discretization.md`](../specs/staqex-continuous-discretization.md)
- AT-TDD Phase 1: [`test_continuous_discretization_red.py`](../../tests/test_continuous_discretization_red.py)

## Summary

Investigate integrals, derivatives, wavefunctions, boundary conditions, and
continuous-domain notation. Decide whether these belong to Staqex source,
symbolic front-end ports, or an external preprocessing boundary.

## Acceptance questions

- What finite representation is required before simulator/QPU execution?
- How are basis, resolution, boundary conditions, and approximation error
  represented?
- Can continuous notation coexist with the finite Hilbert type boundary?
- Which exact/numeric choices belong to LISS-0018?

## Non-goals

This LISS does not claim infinite-dimensional QPU execution or silently hide
discretization.

## Phase 1 design record

The proposal introduces an explicit provider-neutral discretization contract
recording domain, basis, resolution, boundary, approximation method, and
provenance. The architecture review selected MVP domains `Position`,
`Momentum`, and `PhaseAngle`; bases `UniformGrid`, `FourierBasis`/`PlaneWave`,
and `DVR`; contract-field static validation; explicit `Unbounded`/
`Empirical` provenance; and an independent Theory-to-Kernel Bridge contract.
Phase 2 implementation is limited to declaration parsing and contract
validation. The continuous-operator bridge and lowering remain deferred.

## Phase 2 implementation record

- Added top-level `discretization` declarations and immutable
  `DiscretizationContract` values.
- MVP domains and bases are validated statically.
- Required fields are `domain`, `basis`, `resolution`, `boundary`, and
  `approximation`; `error_bound` is optional provenance.
- A continuous operator without an explicit contract produces
  `DISCRETIZATION_REQUIRED_ERROR`.
- `kernel` / `use … for … as …` bridge syntax remains deferred.
- Verification: `python3 tests/test_continuous_discretization_red.py` passes.

## Phase 3 implementation record

- Added `use Contract for Theory.Operator as alias` Bridge declarations.
- Bridges require both a known Discretization contract and a known Theory
  operator.
- Symbolic IR preserves bridge alias, source operator, and contract provenance.
- `kernel` declarations and numerical lowering remain deferred.
- Verification: `python3 tests/test_continuous_discretization_red.py` passes.

## Phase 3 review record

- Architecture Approval: granted for ADR 0074's independent discretization
  contract and explicit Theory-to-Kernel Bridge.
- `resolution`, `boundary`, `approximation`, and provenance remain explicit
  contract data; no backend may infer or silently repair them.
- `kernel` syntax and QPU execution remain separate follow-up boundaries.
- Numerical lowering MVP (`Position` + `UniformGrid` + periodic FD order 2) is
  shipped in [LISS-0111](LISS-0111-continuous-discretization-numerical-lowering-mvp.md).
- Status: **Phase 3 reviewed; explicit discretization boundary complete**.
