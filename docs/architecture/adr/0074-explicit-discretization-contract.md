# ADR 0074: Explicit continuous-domain discretization contract

## Status

Accepted (2026-07-24). This ADR accepts the explicit contract boundary only;
numerical lowering and `kernel` syntax remain separate follow-up work.

## Context

QPex currently executes finite-dimensional Hilbert models. Continuous
operators, wavefunctions, and differential equations require a basis and a
finite representation before simulation or QPU lowering. If those choices are
hidden in a backend, source-level physical meaning and approximation error are
lost.

## Decision proposal

Introduce an explicit provider-neutral `discretization` contract for any
continuous-domain lowering. The contract records:

- domain and carrier;
- basis family;
- resolution or finite dimension;
- boundary condition;
- numerical approximation method and order;
- provenance and approximation metadata.

Illustrative shape (not yet accepted syntax):

```qpex
discretization PositionGrid {
    domain = Position
    basis = UniformGrid
    resolution = 64
    boundary = Periodic
    approximation = FiniteDifference(order = 2)
}
```

No continuous expression may be lowered to a finite operator without a
matching explicit contract. The compiler must reject missing or ambiguous
choices rather than silently choose a grid, boundary, or finite-difference
order.

## Reviewed MVP decisions

The architecture review proposes the following constraints for the MVP:

### First-class domains and bases

Domains:

- `Position`
- `Momentum`
- `PhaseAngle`

Basis families:

- `UniformGrid`
- `FourierBasis` / `PlaneWave`
- `DVR`

These are semantic carriers, not aliases for a generic integer or array index.

### Contract fields and static evaluation

`resolution` and approximation order are contract fields. They participate in
static validation and target inspection. A resolution of `2^k` may lower to
`QubitRegister<k>` when the selected representation requires a binary register;
this relation must be recorded rather than assumed for every basis family.
Non-power-of-two resolution is not universally invalid, but it requires an
explicit representation contract or produces a hard target/lowering error.
Target qubit limits and finite dimensions are checked before lowering.

### Error-bound provenance

Approximation metadata must distinguish:

- a declared analytical bound;
- `Empirical(tol = …)` for an empirical target;
- `Unbounded` when no bound is claimed.

`Unbounded` is an explicit provenance value, not a warning suppression or an
implicit absence of metadata.

### Bridge placement

Discretization is an independent top-level Bridge contract between Theory and
the finite Kernel/Execution representation. A Theory may define a continuous
operator, but a finite lowering must explicitly reference a compatible
discretization contract.

An eventual `kernel`/`use … for … as …` surface is a separate syntax decision;
this ADR does not authorize it yet. The first implementation slice should
validate the contract and preserve its provenance in Symbolic IR.

## Non-goals

- infinite-dimensional QPU execution;
- selecting a universal numerical library;
- hiding discretization in a backend adapter;
- asserting that all continuous mathematics belongs in the QPex surface.

## Review questions

- Which domains and basis families are first-class in the MVP?
- Are resolution and approximation order meta values or contract fields only?
- How are error estimates represented when a method cannot provide a bound?
- Does discretization belong in Theory, Experiment, or a separate declaration?
