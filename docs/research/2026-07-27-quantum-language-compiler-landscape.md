# Quantum language and compiler landscape for the QPex north star

- Date: 2026-07-27
- Scope: language semantics, hybrid execution, intermediate representations,
  simulation, transpilation, and real-hardware workflow
- Evidence policy: primary specifications, official documentation, and
  peer-reviewed/project papers; no provider selection is made
- Related: ADR 0106, WP-0025, LISS-0068

## 1. Research question

What should QPex adopt, avoid, or place behind a port if its primary user is a
physicist who wants to move from a formula and real-world data to a simulator
and then a QPU without rewriting the scientific model?

## 2. Findings

### 2.1 OpenQASM is a target language, not the QPex source model

The [OpenQASM 3.1 specification](https://openqasm.com/versions/3.1/) includes
quantum and classical types, gates, measurement, subroutines, branching,
loops, timing, calibration, pulse constructs, and input/output. Its
[introduction](https://openqasm.com/versions/3.1/intro.html) explicitly
positions OpenQASM as an intermediate representation for higher-level
compilers to communicate with hardware and permits hardware implementations
to support only executable subsets.

QPex implication:

- OpenQASM 3.1 is an important backend artifact and dynamic-control target;
- its imperative gate/timing model must not replace Theory/Physics IR;
- successful OpenQASM emission does not imply that a selected device supports
  every emitted capability;
- target-subset validation and capability provenance are mandatory.

### 2.2 QIR is the portable low-level hybrid boundary

Microsoft's [QIR overview](https://learn.microsoft.com/en-us/azure/quantum/concepts-qir)
describes QIR as language- and hardware-agnostic rules over LLVM IR and as a
common interface between languages/frameworks and quantum platforms. LLVM
control flow naturally represents hybrid classical/quantum programs.

QPex implication:

- QIR is a second portable backend beside OpenQASM, not the Physics IR;
- QPex needs explicit profile selection because static/base and adaptive
  execution capabilities differ;
- lowering must preserve QPex measurement, acting-space, parameter, and result
  contracts rather than inheriting LLVM's general classical semantics at the
  source level.

### 2.3 Modern hybrid compilers use multiple IR levels

The [Catalyst compiler architecture](https://docs.pennylane.ai/projects/catalyst/en/stable/dev/architecture.html)
uses a frontend, an MLIR-based compiler core with multiple dialects and
transformations, LLVM/QIR lowering, and a runtime that connects to devices.
Its goal is a unified representation for hybrid programs, optimization,
automatic differentiation, and dynamic features.

QPex implication:

- a single AST-to-QASM traversal is not a sufficient long-term architecture;
- high-level physics and lower-level hybrid/circuit transformations need
  distinct IR invariants;
- MLIR is credible infrastructure for lower compiler layers, but QPex's
  source-faithful Physics IR should not be defined by MLIR adoption.

### 2.4 One backend does not fit every simulation problem

[CUDA-Q's backend inventory](https://nvidia.github.io/cuda-quantum/latest/using/backends/backends.html)
includes CPU/GPU state-vector, tensor-network, MPS, stabilizer, density-matrix,
trajectory, photonic, multi-QPU, hardware, and dynamics backends. Its
[dynamics documentation](https://nvidia.github.io/cuda-quantum/latest/examples/python/dynamics/dynamics_intro_1.html)
distinguishes circuit simulation from Schrödinger/Lindblad dynamics, including
collapse operators and numerical integration.

QPex implication:

- simulation must be a capability port over a semantic plan;
- simulator selection belongs to Execution, not to state type spelling;
- `State<T>` and `DensityState<T>` must stay representation-independent;
- simulator limitations require explicit resource diagnostics, never state
  truncation or automatic method substitution.

### 2.5 Real hardware compilation has distinct target stages

IBM's current [transpiler-stage guide](https://quantum.cloud.ibm.com/docs/en/guides/transpiler-stages)
separates decomposition/translation, initial layout, routing, optimization,
and scheduling concerns. Physical qubit assignment and connectivity are target
problems rather than source-level logical identities.

QPex implication:

- logical register identity and acting space must survive until target planning;
- layout, routing, native-gate translation, and timing belong after logical QPU
  IR;
- pre-routing and post-routing resource estimates are both needed;
- a provider router is not permitted to redefine a Theory operator.

### 2.6 Mid-circuit measurement is necessary and capability-sensitive

IBM describes dynamic circuits as circuits with
[mid-circuit measurement and feed-forward](https://quantum.cloud.ibm.com/docs/en/tutorials/long-range-entanglement).
Its hardware guidance also documents controller and buffering constraints for
classical feed-forward.

OpenQASM likewise supports measurement-based classical control, while warning
that real-time support is implementation-specific.

QPex implication:

- permanent rejection of dynamic measurement would exclude error correction
  and important protocols;
- adding ordinary classical values to the Static Kernel would be equally
  wrong;
- an explicit `dynamic qpu` lane with phase-local controller values and target
  capability requirements is the correct boundary.

### 2.7 Hardware execution is Job/Session/Batch orchestration

IBM's current [execution-mode guide](https://quantum.cloud.ibm.com/docs/en/guides/choose-execution-mode)
distinguishes independent Jobs, Batches, and iterative Sessions. Amazon
Braket's [task API](https://docs.aws.amazon.com/braket/latest/APIReference/API_CreateQuantumTask.html)
submits artifacts to devices, while the task lifecycle exposes states such as
created, queued, running, completed, failed, cancelling, and cancelled.

QPex implication:

- `main` is not the operating-system/cloud entry point that polls a QPU;
- QPex compilation produces an artifact and measurement contract;
- Host use cases own submission, lifecycle, retry, cancellation, session,
  batch, and completed result retrieval through provider-neutral ports;
- provider IDs, credentials, and SDK types do not belong in source or compiler
  Domain modules.

### 2.8 Existing languages validate stronger static abstractions

[Q#](https://learn.microsoft.com/en-us/azure/quantum/qsharp-overview)
distinguishes quantum operations from classical functions, treats qubits as
opaque target objects, supports measurement results, simulation, resource
estimation, and hardware jobs.

[Silq](https://www.sri.inf.ethz.ch/publications/bichsel2020silq) demonstrates
that safe automatic uncomputation can be a high-level language responsibility.
[Qunity](https://popl23.sigplan.org/details/POPL-2023-popl-research-papers/32/Qunity-A-Unified-Language-for-Quantum-and-Classical-Computing)
explores compositional quantum/classical control and uncomputation.

QPex implication:

- no-cloning, no-implicit-discard, and uncomputation should be type/effect
  obligations rather than programmer-managed memory;
- QPex should preserve its distinctive physicist-facing state/operator model
  rather than copy Q#'s allocation-centered surface;
- automatic uncomputation must be proof-driven and must fail explicitly when
  proof is unavailable.

### 2.9 Quantum chemistry already has mature transformations

PennyLane's
[molecular Hamiltonian API](https://docs.pennylane.ai/en/stable/code/api/pennylane.qchem.molecular_hamiltonian.html)
constructs electronic Hamiltonians and maps fermionic forms to qubit
Hamiltonians, with basis, active-space, charge, spin, and mapping options.

QPex implication:

- QPex should not re-invent every electronic-structure solver or mapping;
- it should own typed physical input, operator/statistics semantics, mapping
  selection, provenance, and compiler diagnostics;
- mature numerical/chemistry engines may be adapters after dependency and
  licensing review.

## 3. Comparative architecture

| Concern | Existing ecosystem tendency | QPex north-star position |
|---|---|---|
| Human authoring | Python/C++ object construction or operation language | paper-shaped typed scientific source |
| Circuit exchange | OpenQASM | backend artifact |
| Low-level hybrid IR | LLVM/QIR | backend/profile artifact |
| High-level compiler | MLIR/dialect stacks increasingly common | typed QPex Physics/Quantum IR; MLIR optional below |
| Quantum safety | opaque qubits, operation/function split, linear types, uncomputation research | `State<T>` plus linear/effect/phase checking |
| Dynamic control | supported on selected devices | explicit capability-checked lane |
| Simulation | many specialized engines | simulator capability ports |
| Hardware mapping | layout/routing/native translation/scheduling | target planning after logical QPU IR |
| Execution | Job/Session/Batch and provider SDKs | Host ports and immutable DTOs |
| Chemistry/many-body | mature domain libraries | typed frontend plus adapter reuse |
| Approximation | often dispersed across API calls | first-class provenance/error ledger |

## 4. Recommended differentiator

QPex should not compete by exposing more gates than SDKs. Its defensible
position is:

> The compiler that accepts a physicist's theory and experimental intent,
> proves phase/type/acting-space consistency, records every approximation, and
> produces simulator and QPU artifacts without losing the meaning of the
> original formula.

That implies four non-negotiable capabilities:

1. source-level mathematical locality;
2. semantic and phase isolation;
3. provenance-complete multi-level lowering;
4. provider-neutral execution and result contracts.

## 5. Decisions still requiring dedicated technology Issues

The research supports boundaries but does not select:

- custom Rust IR only versus selective MLIR dialect adoption;
- concrete simulator libraries and their dependency/licensing posture;
- QIR profiles and validator/toolchain versions;
- first live QPU provider adapter;
- scientific data container adapters such as HDF5;
- exact/symbolic algebra engine integration;
- formatter/LSP Unicode input technology.

These are placed as `[要決定]` Issues in WP-0025. They are not reasons to
weaken the source-language target.
