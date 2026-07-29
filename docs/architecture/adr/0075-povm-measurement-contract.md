# ADR 0075: Terminal POVM and measurement contract

## Status

Proposed. Architecture Path design for LISS-0037. This ADR does not authorize
implementation or provider selection.

## Context

Staqex currently has terminal `measure` for pure states and a mixed-state result
boundary for `DensityState<T>`. LISS-0037 must define how explicit measurement
effects and outcome spaces relate to those paths without introducing an
implicit classical collapse or leaking density matrices to the Host.

The language also has a separate Dynamic QPU lane for mid-circuit measurement
and feed-forward. Static Kernel measurement must not silently acquire those
semantics.

## Decision proposal

1. `measure` is terminal-only in the static Kernel lane.
2. The default terminal measurement is the computational basis of the source
   finite Hilbert domain.
3. An explicit measurement is represented by a typed `POVM<T>` contract whose
   effects form a finite outcome-indexed family:

   ```staqex
   POVM<Qubit> z_basis = ComputationalBasis()
   measure rho with z_basis
   ```

4. Each effect is a typed positive operator on the same Hilbert domain, and a
   POVM is valid only when the effects are complete within the declared
   tolerance: `sum(E_i) = I`. No implicit normalization or completion is
   inserted.
5. `State<T>` and `DensityState<T>` may use the same POVM contract. Probabilities
   are computed as the pure-state equivalent or `Tr(E_i rho)` respectively.
6. The source result is an opaque terminal measurement value. The Host receives
   outcome labels/probabilities and measurement identity metadata, not the raw
   effects or density matrix by default.
7. Mid-circuit measurement, classical feed-forward, and dynamic capability
   checks remain owned by LISS-0028 and are not enabled by this contract.

## MVP boundary

The first implementation slice accepts `ComputationalBasis()` for the existing
finite one-qubit domain:

```staqex
POVM<Qubit> z_basis = ComputationalBasis()
measure rho with z_basis
```

General explicit effect lists are specified by this ADR but remain a follow-up
slice after the boundary is validated. This keeps the terminal result contract
independent from a new matrix-construction surface.

## Diagnostics proposal

- `POVM_DOMAIN_MISMATCH`: effects/POVM domain differs from the measured state.
- `INVALID_POVM_EFFECT`: effect is not a finite square positive operator.
- `INCOMPLETE_POVM`: effects do not sum to identity within tolerance.
- `MID_CIRCUIT_MEASUREMENT_REQUIRES_DYNAMIC_LANE`: measurement occurs before
  the terminal source boundary.

These diagnostics are distinct from `INCOMPLETE_KRAUS_CHANNEL` and the
Lindblad jump diagnostics.

## Consequences

Positive:

- Pure and mixed states share one measurement vocabulary without sharing their
  internal representation.
- The terminal observation boundary and opaque JobResult contract remain clear.
- POVM completeness and channel completeness are not conflated.

Negative:

- Outcome labels need a stable host representation.
- Explicit effect constructors and positivity checks require a later numeric
  slice.
- Dynamic QPU measurement still needs a separate workflow and capability
  contract.

## Open questions

- Whether outcome labels are `Basis`, user-defined symbols, or a dedicated
  `Outcome<N>` carrier.
- Whether the first explicit effect list accepts only `RawMatrix` or a typed
  effect constructor.
- Whether probabilities are always returned or only counts when shots are
  configured.
- How measurement identity is represented in `MeasurementEnvelope`.

## Verification proposal

- Phase 1: terminal computational-basis contract tests, domain/phase negative
  tests, and opaque result metadata tests.
- Phase 2: minimum one-qubit measurement contract implementation.
- Phase 3: refactor and review without changing result assertions.
