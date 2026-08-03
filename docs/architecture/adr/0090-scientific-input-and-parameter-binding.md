# ADR 0090: Scientific input and parameter-binding boundary

## Status

Accepted for [LISS-0045](../documentation-compression-map.md) Phase 2 Green.
This acceptance authorizes the dependency-free Host value objects covered by
the reviewed contract tests. It does not authorize provider selection or
external integration.

## Context

Research across IBM Runtime, Amazon Braket, Cirq, Qiskit Experiments,
Qiskit Nature, and PennyLane shows that a useful quantum workload separates
physical input data, parameter assignments, execution policy, observations,
and scientific artifacts. These concerns must connect without allowing file
formats or provider SDKs to define Staqex language semantics.

## Decisions

1. External data enters through Host-owned typed data contracts and ports.
   CSV, JSON, XYZ, HDF5, Python objects, and provider result objects are
   adapters, not Kernel values.
2. The Kernel receives validated semantic values such as physical quantities,
   finite domains, coefficient tensors, geometry, and `Param<T>` bindings.
3. Parameter sweeps are immutable Host/workflow inputs that bind an experiment
   specification. They are not ordinary classical loops in the QPU lane.
4. Execution settings such as shots, target, seed, precision, retry, and
   resilience remain outside theory expressions.
5. Results use a provider-neutral opaque boundary and distinguish portable
   observations (counts, probabilities, expectations, variances, uncertainties)
   from simulator-only snapshots (state vector, density matrix, internal
   diagnostics).
6. Input, lowering, Job, and result provenance are mandatory for a scientific
   run. At minimum, provenance identifies the source formula, input dataset,
   parameter binding, units/basis, mapping/discretization, target, shots or
   precision, and Job identity.
7. The first slice covered scalar physical inputs, `Param<T>` bindings,
   immutable parameter sweeps, and provenance. **In-memory Host
   `CoefficientTensor` inject** is Accepted under
   [ADR 0119](0119-host-coefficient-tensor-inject.md). Geometry Host contracts
   remain deferred until reviewed.
8. The first Host boundary is an in-memory Python API/fake adapter. File
   formats and provider SDK integration remain separate adapter and technology
   decisions under LISS-0016.
9. The existing provider-neutral `JobResult` boundary remains the result
   integration point. Phase 1 defines the provenance and result acceptance
   contract but does not add a production result DTO.
10. Provenance is mandatory for a scientific run and must identify the source
    formula or program, input identity, parameter binding, units/basis,
    lowering or discretization identity when applicable, execution target,
    shots or precision policy, and Job identity.

## Candidate contracts

The Phase 1 acceptance names these Host-side contract candidates:

```text
ScientificInput<T>
ParameterBinding<T>
ParameterSweep<T>
CoefficientTensor<T, Shape, Domain>
Geometry<Frame, Unit>
ObservationRequest<Observable>
ScientificResult<T>
ScientificArtifact
```

The final design must avoid a generic `Data` or `Json` escape hatch in the
Kernel.

## Boundary example

Host input:

```text
geometry = H2.xyz
charge = 0
spin = singlet
basis = sto-3g
bond_length = 0.735 Å
```

Staqex theory:

```staqex
Hamiltonian H = electronic_energy(geometry, basis)
```

Host execution:

```text
bind H.parameters with sweep
run simulator with shots/precision policy
return energy expectation + uncertainty + provenance
```

The exact syntax and chemistry constructors remain open until the research
requirements are reviewed.

## Non-goals

- No file-format syntax in Staqex.
- No provider SDK or credential implementation.
- No automatic unit, basis, mapping, or discretization inference.
- No general classical runtime inside the Kernel.
- No claim that all external datasets share one schema.
- No optimizer implementation in the first slice.

## Open decisions

- How should geometry and coefficient tensors extend the scalar contract?
- Are units represented by existing physical quantity types or a new input
  metadata contract beyond the first scalar slice?
- How are arrays/tensors indexed and shape-checked at the Kernel boundary?
- How are missing values, uncertainty, and quality flags represented?
- Which file adapters, if any, should be added after the in-memory Host API?
- What is the canonical result envelope for counts, expectations, and errors?
- Which optional provenance quality fields should be standardized?

## Verification proposal

- Phase 0: completed by the research note and this ADR decision record.
- Phase 1: contract tests for scalar typed input validation, `Param<T>`
  bindings, immutable parameter sweeps, result opacity, and provenance; no
  external service.
- Phase 2: local fake adapter and simulator integration.
- Phase 3: refactor and reviewer empathy review.
