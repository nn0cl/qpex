# Quantum machine scale and model horizon research (2026-07-30)

## Purpose

This note supports a bidirectional hardware horizon for Staqex:

1. scale **up** to planned modular, fault-tolerant facility machines; and
2. scale **down** to a future local or household-sized quantum appliance.

It also asks whether the language can generalize across quantum computation
models without adopting a circuit language as its semantics.

This is research evidence, not an accepted product forecast. Vendor roadmap
figures are current intentions and may change.

The separate
[optimistic capacity horizon](../architecture/quantum-capacity-horizon-scenarios.md)
turns selected historical reference points into non-normative compiler stress
profiles.

## Current and planned evidence

### Facility-scale fault-tolerant direction

- IBM's March 2026 roadmap describes Starling for 2029 as a modular,
  error-corrected system with 200 logical qubits and 100 million gates.
- QuEra's July 2026 roadmap describes Libra for 2028 with 256 logical qubits,
  more than 10,000 physical qubits, logical error rate `10^-6`, real-time QEC,
  qubit-loss detection, and active reloading.
- Quantinuum describes an end-of-decade universal fault-tolerant system with
  hundreds of logical qubits and millions of operations.
- PsiQuantum frames its utility-scale photonic architecture around roughly one
  million physical qubits and modular deployment.

These roadmaps indicate more than scalar growth. They introduce logical versus
physical resources, sustained QEC, modular communication, decoder/control
latency, and programs too large to treat as eagerly expanded instruction
lists.

### Local and compact direction

- IQM Spark is an on-premises five-qubit superconducting system for
  universities and research centers.
- SpinQ offers desktop and portable NMR systems for education; these are small
  demonstrators, not evidence of a scalable household universal computer.
- Quantum Brilliance has sold a second-generation 19-inch rack-mountable,
  room-temperature diamond quantum accelerator.
- Quandela offers modular on-premises photonic systems from 6 to 24 qubits,
  described as datacenter-ready and upgradable.

These systems do not yet establish a general-purpose household quantum PC.
They do establish relevant deployment patterns: local ownership, on-premises
operation, accelerator integration, compact/rack form factors, offline or
low-latency access, and hardware models unlike a conventional superconducting
cloud QPU.

## Design inferences for Staqex

### 1. Scale is a vector, not a qubit count

Relevant dimensions include:

- logical and physical carriers;
- local dimension and carrier family;
- logical operation budget and logical failure probability;
- parallelism and structured-control support;
- measurement/reset/feed-forward latency;
- modular links and non-local operation support;
- loss detection/reload;
- decoder throughput;
- power, thermal, memory, wall-clock, and monetary budgets;
- local, on-premises, or remote deployment.

No one number defines a "larger" quantum computer.

### 2. Large machines require hierarchical plans

Millions or hundreds of millions of operations should not be represented by
eagerly materializing one flat tuple. Compiler artifacts need structured
regions, callable subplans, symbolic repetition, resource expressions, and
late target expansion.

### 3. Personal machines are accelerators, not isolated replacements for CPUs

A plausible Personal Quantum Appliance is a local quantum co-processor
attached to ordinary CPU/GPU/storage and used through a hybrid workflow. The
language must not require cloud queues, credentials, or network access for
core compilation and execution.

### 4. Generalization is broader than the gate model

Potential target families include:

- universal digital gate machines;
- native Hamiltonian/analog evolution;
- measurement-based or photonic/Fock-state systems;
- qubit and qudit machines;
- optimization/annealing-oriented systems;
- simulators and emulators.

Staqex should preserve physics and state-transform semantics above those
families. Each target family receives a capability profile and an explicit
lowering. Unsupported semantics fail; no target silently reinterprets source.

Continuous-variable source meaning remains in Physics IR. Quantum Semantic IR
v1 is finite. A future native continuous-variable target needs its own reviewed
semantic profile or an explicit finite contract; it must not bypass this
boundary.

### 5. Locality changes operational policy, not quantum meaning

A local appliance needs:

- offline compilation and execution;
- local capability discovery;
- explicit permission before remote fallback;
- local source/result handling and privacy-preserving defaults;
- incremental compile/run suitable for interactive applications;
- versioned firmware/calibration/capability snapshots;
- power and thermal budgets;
- honest rejection when the local device is too small or lacks an operation.

These belong to workflow, ports, target capability, and resource policy—not to
`State<T>` semantics.

## Adopt, adapt, reject

| Direction | Staqex treatment |
|---|---|
| Fixed vendor roadmap numbers as language limits | **Reject** |
| Logical/physical resource distinction | **Adopt downstream of semantics** |
| Flat expansion of very large programs | **Reject** |
| Hierarchical and symbolic plans | **Adopt** |
| Cloud as required execution model | **Reject** |
| Local/on-premises/remote as deployment profiles | **Adopt** |
| Local quantum accelerator beside CPU/GPU | **Adopt as a host-workflow target** |
| Gate model as universal source semantics | **Reject** |
| Multiple target computation families | **Adapt through explicit capability profiles and lowerings** |
| Silent simulator or remote fallback | **Reject** |

## Primary sources

- IBM, [Quantum 2030 roadmap](https://www.ibm.com/roadmaps/quantum/2030/).
- QuEra, [Quantum roadmap](https://www.quera.com/our-quantum-roadmap).
- Quantinuum, [Technical roadmap to universal fault-tolerant quantum
  computing](https://www.quantinuum.com/blog/technical-perspective-by-the-end-of-the-decade-we-will-deliver-universal-fault-tolerant-quantum-computing).
- PsiQuantum, [Company and architecture mission](https://www.psiquantum.com/about).
- IQM, [IQM Spark](https://iqm.tech/products/iqm-spark/).
- Quantum Brilliance, [Room-temperature rack-mountable accelerator
  deployment](https://quantumbrilliance.com/news/quantum-brilliance-announces-first-purchase-of-a-room-temperature-quantum-accelerator-in-europe-powered-by-nvidia-cuda-q/).
- Quandela, [MosaiQ modular photonic quantum
  computer](https://www.quandela.com/products-and-services/mosaiq/).
- SpinQ, [Desktop and portable NMR systems](https://www.spinq.com/).

## Limits

- "Personal Quantum Appliance" is a Staqex design horizon, not a claim that a
  useful general-purpose household device currently exists.
- Vendor product and roadmap pages are primary claims from their publishers,
  not independent validation of delivery dates or performance.
- This note does not select a provider, hardware modality, QEC code, runtime,
  SDK, or target format.
