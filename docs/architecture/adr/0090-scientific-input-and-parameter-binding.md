# ADR 0090: Scientific input and parameter-binding boundary

## Status

Proposed. Architecture Path design for [LISS-0045](../../issues/LISS-0045-scientific-input-and-parameter-binding.md).
This ADR does not authorize implementation or provider selection.

## Context

Research across IBM Runtime, Amazon Braket, Cirq, Qiskit Experiments,
Qiskit Nature, and PennyLane shows that a useful quantum workload separates
physical input data, parameter assignments, execution policy, observations,
and scientific artifacts. These concerns must connect without allowing file
formats or provider SDKs to define QPex language semantics.

## Decision proposal

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
7. The first implementation slice should be a dependency-free local
   simulator path with a fake Host data adapter. Provider SDK integration is a
   separate technology decision under LISS-0016.

## Candidate contracts

These are design candidates, not accepted surface names:

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

QPex theory:

```qpex
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

- No file-format syntax in QPex.
- No provider SDK or credential implementation.
- No automatic unit, basis, mapping, or discretization inference.
- No general classical runtime inside the Kernel.
- No claim that all external datasets share one schema.
- No optimizer implementation in the first slice.

## Open decisions

- Which Host data contract is the minimum: scalar bindings, tensors, geometry,
  or all three together?
- Are units represented by existing physical quantity types or a new input
  metadata contract?
- How are arrays/tensors indexed and shape-checked at the Kernel boundary?
- How are missing values, uncertainty, and quality flags represented?
- Is the first external adapter file-based, Python-library-based, or both?
- What is the canonical result envelope for counts, expectations, and errors?
- Which provenance fields are mandatory versus optional?

## Verification proposal

- Phase 0: validate requirements against representative H2/Ising/parameter
  sweep inputs and the SDK models documented in the research note.
- Phase 1: contract tests for typed input validation, parameter sweeps,
  result opacity, and provenance; no external service.
- Phase 2: local fake adapter and simulator integration.
- Phase 3: refactor and reviewer empathy review.
