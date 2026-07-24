# QPex density, CPTP, and Lindblad contract

| Field | Value |
|---|---|
| Status | **Phase 2 Green; symbolic Lindblad lowering MVP implemented** |
| Decision | [ADR 0057](../architecture/adr/0057-density-cptp-lindblad.md) |
| Issue | [LISS-0011](../issues/LISS-0011-density-matrix-lindblad.md) |

## Acceptance scenarios

1. Pure `State<T>` programs retain existing unitary and terminal-measure
   behavior.
2. A normalized `DensityState<T>` has a finite Hilbert domain, trace one, and
   positivity metadata/checks.
3. A malformed density value is rejected before channel evolution.
4. A typed CPTP `Channel<A, B>` composes only when domains match.
5. `partial_trace` returns a density state for the retained typed subsystem.
6. Lindblad evolution is available only in an explicitly supported CPU/simulator
   lane and preserves trace within the declared numerical tolerance.
7. Terminal measurement of a density state produces an opaque Job/measurement
   result; no raw density matrix is exposed to the Host by default.
8. Mid-circuit measurement remains a Dynamic QPU capability and is rejected in
   the static Kernel lane.

## Proposed first surface slice

```qpex
State<Qubit> psi = |0>
DensityState<Qubit> rho = pure_to_density(psi)
Channel<Qubit, Qubit> noise = DepolarizingChannel(0.1)
DensityState<Qubit> evolved = apply(noise, rho)
measure evolved
```

## Accepted numeric constructor surface

The numeric slice uses one uniform constructor with explicit input domains:

```qpex
DensityState<Qubit> ensemble = DensityState(
    Ensemble([
        (0.5, |0>),
        (0.5, |1>)
    ])
)

DensityState<Qubit> raw = DensityState(
    RawMatrix([[0.5, 0.0], [0.0, 0.5]])
)
```

`Ensemble` is the physical provenance path. `RawMatrix` is an explicit
low-level simulator/test injection. Representation-specific factory methods
are not part of the surface.

The constructor rejects invalid trace or positivity with
`MALFORMED_DENSITY_STATE`; it does not normalize, clip, or otherwise correct
the input. The default trace and positivity tolerances are `1e-12`.

`KrausChannel([...])` rejects an incomplete operator set with a hard diagnostic
`INCOMPLETE_KRAUS_CHANNEL` when `sum(K_i† K_i) = I` is not satisfied within the
declared tolerance.

Lindblad jump inputs use a separate explicit numeric surface:

```qpex
DensityState<Qubit> evolved = lindblad(
    rho,
    H,
    JumpSet([RawMatrix([[0.0, 1.0], [0.0, 0.0]])]),
    0.1
)
```

`JumpSet` is not a CPTP `Channel`; a `Channel` value is not implicitly accepted
as a jump operator. Non-square or non-numeric entries produce
`INVALID_LINDBLAD_JUMP_SET`; a jump dimension that does not match the source
Hilbert domain produces `LINDBLAD_JUMP_DIMENSION_ERROR`. An empty list remains
the compatibility spelling for no jumps. Bound one-qubit `Operator` entries
are lowered through the existing finite Hamiltonian compiler; general
symbolic jump lowering is deferred.

`DensityState<T>` and `Channel<A, B>` are distinct semantic families. A pure
`State<T>` cannot be passed to a channel that requires `DensityState<T>`
without an explicit `pure_to_density` conversion.

Terminal measurement may name the first typed POVM slice:

```qpex
POVM<Qubit> z_basis = ComputationalBasis()
measure rho with z_basis
```

The same contract is accepted for pure and mixed one-qubit states. The Host
result remains opaque and records `measurement_kind = ComputationalBasis`;
raw density matrices are not exposed. General effect lists and mid-circuit
measurement remain deferred.

## Representation boundary

```text
pure State<T>       -> unitary Kernel path
DensityState<T>     -> finite mixed-state CPU/channel path
Channel<A, B>       -> typed CPTP transformation
terminal measure    -> opaque MeasurementEnvelope / JobResult
```

The representation is finite-dimensional in this LISS. Infinite-dimensional
open systems and provider-specific noise are deferred.

The current implementation validates numeric constructor inputs, lowers
explicit numeric and bound one-qubit symbolic jump inputs, and exposes the
typed contract boundary. General symbolic operator lowering remains deferred.

## Accepted MVP details

- Mixed states use `DensityState<T>` rather than `State<Density<T>>`.
- Structural positivity/trace evidence is checked statically where possible;
  numerical constructors reject invalid values without correction.
- Lindblad first lowers to a finite CPU/simulator superoperator or equivalent
  representation.
- MVP channels are depolarizing, amplitude damping, phase damping, and direct
  Kraus channels with completeness validation.
- Mixed measurement reuses `JobResult` and records density-state and
  basis/POVM metadata without exposing raw matrix storage.

## Deferred questions

- numerical storage format, precision, and dependency policy;
- Lindblad integrator and tolerance contract;
- explicit POVM effect vocabulary, which is tracked by LISS-0037.

The numeric storage format, precision implementation, and dependency policy
remain the entry gate for the next Phase 1 Red slice. The source constructor
surface itself is now accepted by ADR 0057.

## Implementation evidence

- `CompileResult.mixed_state_contracts` records `DensityState<T>` and
  `Channel<A, B>` declarations.
- `RawMatrix` and `Ensemble` constructor inputs receive trace and positivity or
  weight-sum validation without silent correction.
- Explicit numeric Kraus matrices receive a completeness check; symbolic
  Kraus operators remain outside this slice.
- Pure-state/channel mixing is rejected with `MIXED_STATE_TYPE_ERROR` unless
  `pure_to_density` is written explicitly.
- Acceptance coverage is in
  [`test_density_cptp_lindblad_red.py`](../../tests/test_density_cptp_lindblad_red.py).
- Runtime Lindblad acceptance coverage is staged in
  [`test_density_cptp_lindblad_runtime_red.py`](../../tests/test_density_cptp_lindblad_runtime_red.py).
- Runtime implementation is in
  [`runtime/lindblad.py`](../../compiler/qpex/runtime/lindblad.py); it is
  CPU/simulator-only and uses fixed-step RK4 with an explicit trace guard.
- Source-level integration acceptance tests are staged in
  [`test_density_cptp_lindblad_source_red.py`](../../tests/test_density_cptp_lindblad_source_red.py).
- Source-level mixed values use a dedicated evaluator lane and terminal
  measurement returns the existing opaque Host result with `state_type` and
  execution-lane metadata. Symbolic Hamiltonian/jump lowering remains
  deferred; no raw matrix is exposed.
- Symbolic lowering acceptance is staged in
  [`test_density_cptp_lindblad_symbolic_red.py`](../../tests/test_density_cptp_lindblad_symbolic_red.py).
- Explicit one-qubit Hamiltonians and time literals lower to the existing
  fixed-step RK4 runtime. Unresolved symbolic inputs remain contract-only and
  are never assigned hidden numeric defaults.
