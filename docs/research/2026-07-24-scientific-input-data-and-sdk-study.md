# Research: scientific input data and SDK execution models

## Status

Proposed research record. This document extracts requirements; it does not
select a provider SDK or authorize implementation.

## Research question

What must QPex accept and return so that a physicist can write a model close
to the mathematical expression, provide real-world data, run a simulator or a
QPU, and obtain an interpretable result without leaking Host concerns into
the Kernel?

## Sources and observed models

### IBM Quantum Runtime and Qiskit

IBM Runtime V2 uses a Primitive Unified Bloc (PUB) as a unit of work. A
Sampler PUB contains a circuit, optional parameter values, and optional
shots. An Estimator PUB adds observables and precision. A single job can
broadcast parameter sets and observables, which is directly relevant to
parameter sweeps and VQE-style workloads.

Sources: [Sampler inputs and outputs](https://quantum.cloud.ibm.com/docs/en/guides/sampler-input-output),
[Runtime V2 primitives](https://quantum.cloud.ibm.com/docs/en/guides/v2-primitives),
[Qiskit Runtime examples](https://github.com/Qiskit/qiskit-ibm-runtime).

Qiskit result data separates the job/backend identity from counts, memory,
statevector, unitary, and optional simulator snapshots. Qiskit Experiments
adds an `ExperimentData` container containing raw measurement data, analysis
results, figures, and metadata.

Sources: [Qiskit Result](https://quantum.cloud.ibm.com/docs/api/qiskit/qiskit.result.Result),
[Qiskit Experiments framework](https://qiskit-community.github.io/qiskit-experiments/apidocs/framework.html),
[experiment artifacts](https://qiskit-community.github.io/qiskit-experiments/howtos/artifacts.html).

### Amazon Braket

Braket treats a circuit plus measurement instructions, device, shots, and
request metadata as a quantum task. Tasks are asynchronous and return a task
identity; the SDK polls and retrieves the result later. Results can include
measurements/counts, probabilities, expectation, variance, samples, and
provider-dependent result types. State vectors and amplitudes are simulator
capabilities rather than portable QPU results.

Sources: [Braket task flow](https://docs.aws.amazon.com/braket/latest/developerguide/braket-how-it-works.html),
[Braket result types](https://docs.aws.amazon.com/braket/latest/developerguide/braket-result-types.html),
[task submission and results](https://docs.aws.amazon.com/braket/latest/developerguide/braket-submit-tasks-to-braket.html).

Braket Hybrid Jobs also distinguish algorithm inputs, hyperparameters,
outputs, and checkpoints. Results and checkpoints are stored outside the
quantum task and copied through an explicit job output contract.

Source: [Hybrid Job inputs and outputs](https://docs.aws.amazon.com/braket/latest/developerguide/braket-jobs-inputs-and-outputs.html).

### Cirq

Cirq represents parameterized circuits separately from parameter assignments.
Parameter sweeps are collections of assignments that can be run on a
simulator or sampler. The same conceptual circuit can therefore be evaluated
for many parameter values without rebuilding its mathematical definition.

Source: [Cirq parameter sweeps](https://quantumai.google/cirq/simulate/params).

For hardware execution, Cirq documents that only sampled end results are
available. This supports a strict distinction between simulator snapshots
and portable experimental observations.

Source: [Cirq basics](https://quantumai.google/cirq/start/basics).

### Quantum chemistry and real scientific inputs

Quantum chemistry SDKs show that real input is richer than a parameter map.
Qiskit Nature accepts molecular structure and classical electronic-structure
data, constructs an `ElectronicStructureProblem`, and returns second-quantized
operators and auxiliary properties. The documented H2 example includes atom
coordinates, charge, spin, basis, and a classical driver.

Sources: [Qiskit Nature electronic structure tutorial](https://qiskit-community.github.io/qiskit-nature/tutorials/01_electronic_structure.html),
[ElectronicStructureProblem](https://qiskit-community.github.io/qiskit-nature/stubs/qiskit_nature.second_q.problems.ElectronicStructureProblem.html),
[Qiskit Nature operators](https://qiskit-community.github.io/qiskit-nature/apidocs/qiskit_nature.second_q.operators.html).

PennyLane's quantum chemistry interface accepts molecular symbols and
coordinates or reads an XYZ structure file, then constructs a molecular
Hamiltonian and observables. It can also import Hamiltonians and states
created by classical chemistry tools.

Sources: [PennyLane quantum chemistry](https://docs.pennylane.ai/en/stable/introduction/chemistry.html),
[PennyLane dataset loading](https://docs.pennylane.ai/en/stable/code/api/pennylane.data.load.html).

## Requirements extracted for QPex

The SDKs and scientific examples converge on five distinct contracts.

### 1. Model data

Data that defines the physical problem:

- scalar quantities with units and dimensions;
- coordinates and geometry;
- sparse/dense coefficient tensors;
- basis and domain declarations;
- charge, particle count, spin, boundary conditions;
- measured or externally computed initial conditions.

### 2. Parameter binding

Values that are supplied after a circuit or experiment is defined:

- one parameter assignment;
- a parameter sweep or broadcast batch;
- parameter shape and ordering;
- allowed range and physical units;
- reproducibility identity for the input set.

### 3. Execution policy

Values controlling execution rather than physics:

- shots or target precision;
- seed policy;
- simulator/QPU target;
- error mitigation and resilience options;
- resource budget and batching policy.

These must not be visible inside a pure theory expression.

### 4. Observation request and result

The output is not one universal state object. It may be:

- counts or bitstrings;
- probabilities;
- expectation or variance of an observable;
- scalar energy and standard error;
- simulator-only state vector, density matrix, or snapshot;
- analysis result and fit artifacts.

Every result needs Job identity, target, shots/precision, observable
identity, parameter binding, and provenance.

### 5. Scientific artifacts

Real experiments also produce data that is neither a final scalar nor a raw
quantum state:

- raw measurements;
- calibration and device metadata;
- fitted curves and uncertainties;
- figures and analysis tables;
- checkpoints and resumable workflow state.

## Design implications for QPex

1. The input boundary should be typed and semantic, not a generic JSON object.
2. File formats such as XYZ, CSV, JSON, and HDF5 should be Host adapters or
   import ports. They should not become Kernel syntax.
3. QPex source should refer to validated physical concepts such as
   `Mass`, `Angle`, `Geometry`, `CoefficientTensor`, and `Param<Angle>`.
4. A parameter sweep should be a Host/workflow value that binds an immutable
   experiment specification, not a classical loop inside a QPU expression.
5. Result types should distinguish portable observations from
   simulator-only snapshots.
6. Raw data and analysis artifacts require an explicit opaque artifact
   boundary; the Kernel should not know about S3, databases, or notebook
   storage.
7. The data contract must preserve the route from source formula and input
   dataset to lowered operator, QPU artifact, Job, and result.

## Recommended first vertical slice

The smallest useful slice is a local, provider-neutral parameter sweep:

```text
validated Host input
  -> Param<T> binding
  -> immutable QPex experiment
  -> local Simulator Job
  -> expectation/count result
  -> provenance and uncertainty report
```

Quantum chemistry should be the first representative domain because its
inputs exercise geometry, units, basis, particle/spin metadata, coefficient
tensors, second quantization, mapping provenance, and energy observables.

## Rejected shortcuts

- Make JSON or Python dictionaries first-class Kernel values.
- Treat simulator statevector output as a portable QPU result.
- Hide parameter sweeps inside `forEach` or ordinary classical loops.
- Infer units, basis, boundary conditions, or mapping choices from raw data.
- Let a provider SDK's request/response model define QPex semantics.

## Proposed follow-up

Record the architecture boundary in [ADR 0090](../architecture/adr/0090-scientific-input-and-parameter-binding.md)
and track implementation planning in [LISS-0045](../issues/LISS-0045-scientific-input-and-parameter-binding.md).
