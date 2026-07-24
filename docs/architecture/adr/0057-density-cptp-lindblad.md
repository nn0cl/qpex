# ADR 0057: Mixed-state density and CPTP boundary

## Status

Accepted architecture decision. The numeric constructor surface is accepted
for the next AT-TDD Phase 1 Red slice; implementation still requires the
separate phase gate.

## Context

QPex currently models pure finite-support quantum values with `State<T>` and
preserves terminal `measure` as the observation boundary. Open-system physics
requires mixed states, partial trace, quantum channels, and Lindblad evolution.
Adding these directly to the pure-state representation would make positivity,
trace, and non-unitary evolution implicit and would blur the Kernel / Host
boundary.

## Decision proposal

1. Preserve `State<T>` as the pure-state value and unitary/evolution surface.
2. Introduce a distinct `DensityState<T>` semantic representation for positive
   trace-one operators over a finite Hilbert domain.
3. Introduce typed `Channel<A, B>` values for completely positive maps. A
   channel declaration must carry input/output Hilbert domains and its
   trace-preserving status; invalid maps are hard errors.
4. Treat `partial_trace` as a typed subsystem operation that returns a
   `DensityState` on the retained subsystem.
5. Keep Lindblad evolution in the CPU/simulator lane first. It lowers to a
   finite channel/evolution plan only when a target explicitly supports it;
   there is no implicit QPU emulation.
6. Terminal `measure` remains the only source-language observation boundary.
   Measurement of `DensityState<T>` returns the same opaque host
   `MeasurementEnvelope` / `JobResult` family used by pure states.
7. Mid-circuit measurement and feed-forward remain owned by LISS-0028 and are
   not introduced by this ADR.

## Invariants

- Density values are positive semidefinite and trace one when constructed as a
  normalized state.
- CPTP channels preserve trace and cannot expose raw matrix storage through the
  Host result boundary.
- Pure-state programs remain source-compatible and retain current unitary
  checks.
- Mixed-state semantics do not add implicit classical branching or implicit
  measurement.

## Accepted architecture details

### Surface representation

Use `DensityState<T>` as a distinct top-level semantic type. Do not encode the
mixed-state boundary as `State<Density<T>>`; pure-state and density-state
operator algebras must remain visibly separate.

### Positivity and trace checks

Known constructions such as pure-state projectors, accepted CPTP composition,
and normalized partial trace may carry structural proof metadata through the
type checker. Direct numerical construction and numerical evaluation require a
constructor/runtime guard that rejects non-positive or non-trace-one values.
No silent clipping, renormalization, or correction is permitted.

### Lindblad representation

The MVP Lindblad lane is CPU/simulator only. A finite Liouvillian or equivalent
superoperator representation is the first lowering target; QPU emulation is
not implicit. Numerical storage and integrator selection remain subject to
LISS-0018 and the dependency policy.

### MVP channel constructors

The first constructor set is:

- `DepolarizingChannel(p)`;
- `AmplitudeDampingChannel(gamma)`;
- `PhaseDampingChannel(lambda)`;
- `KrausChannel([K0, K1, …])`, with a hard completeness check
  `sum(Kᵢ† Kᵢ) = I`.

### Numeric slice constructor surface

Use one `DensityState(...)` constructor with explicit typed input domains. Do
not add representation-specific factory methods such as `from_matrix`,
`from_ensemble`, or `from_bloch`.

The accepted inputs for the numeric slice are:

```qpex
DensityState<Qubit> rho = DensityState(
    Ensemble([
        (0.5, |0>),
        (0.5, |1>)
    ])
)

DensityState<Qubit> rho = DensityState(
    RawMatrix([[0.5, 0.0], [0.0, 0.5]])
)
```

`Ensemble` is the primary physical construction path and represents
`rho = sum_i p_i |psi_i><psi_i|`. `RawMatrix` is an explicit low-level
simulator/test injection and must remain visibly distinct from physical
provenance.

Both inputs are rejected with the hard diagnostic
`MALFORMED_DENSITY_STATE` unless trace and positivity satisfy the declared
tolerances. The default trace and positivity tolerances are `1e-12`; no
implicit normalization, clipping, or correction is allowed.

`KrausChannel` is accepted only when
`sum(K_i† K_i) = I` within `epsilon_kraus` and otherwise produces a hard
diagnostic `INCOMPLETE_KRAUS_CHANNEL` before state evolution. The exact numeric
storage implementation and dependency remain separate technology decisions.

Lindblad jump operators are a distinct input concept from CPTP channels. The
MVP source surface is `JumpSet([RawMatrix(...)])`; `Channel` values are not
implicitly converted to jump operators. `INVALID_LINDBLAD_JUMP_SET` identifies
malformed/non-numeric or Channel jump payloads, `LINDBLAD_JUMP_DIMENSION_ERROR`
identifies a Hilbert-domain mismatch, and
`SYMBOLIC_JUMP_LOWERING_REQUIRED` identifies an unresolved symbolic entry. The
Kraus diagnostic remains scoped to Kraus completeness. General symbolic
operator lowering remains deferred.

### Measurement metadata

Pure and mixed results share the existing opaque `JobResult` /
`MeasurementEnvelope` boundary. Mixed-state measurement adds metadata for
`state_type = DensityState`, a basis/POVM specification identity, and
calculated probabilities when available from a simulator. Raw density matrices
remain outside the default Host result.

## Non-goals

- provider SDKs, pulse simulation, or hardware noise APIs;
- infinite-dimensional density operators;
- automatic purification as a hidden implementation trick;
- replacing `State<T>` with a universal dynamic container.

## Review resolution

- `DensityState<T>` is the accepted surface name; `State<Density<T>>` is not
  used.
- Structural evidence may be carried by the type checker, while numeric
  constructors/runtime guards reject invalid trace or positivity without
  correction.
- Lindblad is CPU/simulator-only for the first implementation and lowers to a
  finite superoperator or equivalent representation.
- The MVP channel constructors are depolarizing, amplitude damping, phase
  damping, and `KrausChannel`.
- Mixed measurement metadata uses the existing opaque Job/measurement result
  boundary and records density-state and basis/POVM identity.
- The numeric storage format, precision implementation, and dependency policy
  remain open technology decisions and must not be selected by the Phase 1 Red
  tests.
