# LISS-0045: Scientific input and parameter binding

## Metadata

- Local issue ID: LISS-0045
- GitHub issue: none
- Status: **Phase 3 complete**
- Phase: Feature Path — Phase 3 Refactor reviewed
- Type: Host data contract / language boundary / scientific workflow
- Priority: P0
- Planning size: L
- Depends on: LISS-0027, LISS-0022, LISS-0032, LISS-0033, LISS-0035, ADR 0090
- Related: LISS-0016, LISS-0036, LISS-0044

## Summary

Define how real-world scientific data becomes validated QPex input without
turning file formats, Python objects, or provider SDK types into Kernel
values. The first goal is a local simulator vertical slice with parameter
bindings and a provenance-bearing result.

## Acceptance questions

- What is the smallest typed input set: scalar physical values, geometry,
  coefficient tensors, or all three?
- How do units, dimensions, basis, shape, uncertainty, and quality flags
  cross the Host/Kernel boundary?
- How are one binding and a parameter sweep represented?
- Which values are physical model data and which are execution settings?
- What is the canonical provider-neutral result for counts, expectation,
  probability, variance, and standard error?
- How are source formula, input dataset, mapping/discretization, Job, and
  result connected in provenance?
- Which simulator-only artifacts may be requested without pretending they are
  portable QPU results?

## Representative use cases

1. **H2 / quantum chemistry**: XYZ geometry, charge, spin, basis, electronic
   integrals, second-quantized Hamiltonian, energy expectation.
2. **Ising/material model**: measured coupling and field arrays, finite lattice
   domain, Hamiltonian expectation and uncertainty.
3. **Rabi/parameter sweep**: time or angle values, repeated parameter sets,
   shot-based samples, fitted curve artifact.
4. **Open-system experiment**: measured rates, density/noise parameters,
   expectation values, and simulator-only diagnostic snapshots.

## In scope

- Host-owned typed input and parameter-binding contracts;
- file/library adapter boundary without selecting a provider;
- scalar, tensor, geometry, and sweep requirements;
- result/provenance requirements;
- local fake adapter and simulator acceptance plan.

## Out of scope

- provider SDKs, credentials, network, and cloud persistence;
- choosing JSON, CSV, XYZ, HDF5, or Python as the canonical source format;
- automatic unit/basis/mapping/discretization inference;
- a general classical language in the Kernel;
- optimizer implementation and dynamic QPU feed-forward;
- implementation before the research and ADR are reviewed.

## Dependencies and next phase

1. [Research: scientific input data and SDK execution models](../research/2026-07-24-scientific-input-data-and-sdk-study.md) is reviewed.
2. [ADR 0090](../architecture/adr/0090-scientific-input-and-parameter-binding.md) is accepted for the scalar Host contract.
3. [Acceptance specification](../specs/qpex-scientific-input-and-parameter-binding.md) fixes the scalar first slice.
4. [Work Plan WP-0020](../work-plans/WP-0020-scientific-input-and-parameter-binding.md) records the phase gate and dependencies.
5. Phase 1 Red and Phase 2 Green were reviewed; Phase 3 refactoring is
   complete for the minimum dependency-free Host contract.

## Design intake record

- Included: IBM Runtime PUBs, Braket tasks/result types/Hybrid Jobs, Cirq
  parameter sweeps, Qiskit Experiments, Qiskit Nature electronic structure,
  PennyLane chemistry/dataset inputs, and QPex LISS-0022/0027/0032/0033/0035.
- Omitted: provider credentials, live accounts, private datasets, and SDK
  installation or implementation.
- Candidate value objects: `ScientificInput`, `ParameterBinding`,
  `ParameterSweep`, `CoefficientTensor`, `Geometry`, `ScientificResult`, and
  `ScientificArtifact`.
- Ports/adapters: Host data import port, parameter binding service, and
  provider-neutral Job/result ports; no Kernel provider adapter.
- Current status: Phase 3 complete; provider integration and deferred
  tensor/geometry work have not started.

## Phase 1 Red record

- Added the acceptance specification and WP-0020.
- Added contract tests for scalar input, parameter binding, immutable sweeps,
  validation diagnostics, and provenance.
- Production code unchanged by this phase.
- Exit gate: Adjudicator review of the failing tests before Phase 2 Green.

## Phase 2 Green record

- Added dependency-free immutable Host value objects in
  `compiler/qpex/scientific_input.py`.
- Exported the contract from `compiler.qpex`.
- Reused no provider SDK, filesystem adapter, network, or Kernel value.
- Reviewed acceptance tests pass without changing their assertions.

## Phase 3 Refactor record

- Centralized unit vocabulary and validation helpers.
- Preserved immutable mappings and binding tuples at the public boundary.
- Updated the standalone acceptance runner to report ordinary pass/fail
  results after the contract became implemented.
- No acceptance behavior or assertion was changed.
