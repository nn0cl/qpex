# Quantum machine scale and model envelope

## Status and authority

**Draft for Adjudicator architecture review. No implementation permission.**

This contract extends the design horizon in both directions:

```text
Personal / local quantum appliance
            <-> on-premises / laboratory system
            <-> modular utility-scale fault-tolerant system
```

and across explicitly profiled computation families:

```text
digital | analog evolution | measurement-based / photonic
        | qubit / qudit | optimization-specialized | simulator
```

It is governed by the Staqex axioms and ADR 0106. Proposed changes are recorded
in [ADR 0109](decision-themes/dec-0006-host-qpu-and-external-ports.md). External
evidence is recorded in the
[research note](../research/2026-07-30-quantum-machine-scale-and-model-horizon.md).
Optimistic quantitative stress profiles are proposed separately in
[ADR 0110](decision-themes/dec-0006-host-qpu-and-external-ports.md) and the
[capacity horizon](quantum-capacity-horizon-scenarios.md).
Current and 2026–2031 delivery profiles are proposed in
[ADR 0111](decision-themes/dec-0006-host-qpu-and-external-ports.md) and the
[current-hardware delivery envelope](current-hardware-delivery-envelope.md).

## Design check

```markdown
[DESIGN CHECK]
- Scope and expected behavior: keep one Staqex semantics usable from future
  household/local quantum accelerators through modular fault-tolerant facility
  systems, and across explicitly profiled quantum computation families.
- Specifications and files inspected: Staqex axioms; ADR 0106; compiler
  blueprint; proposed Quantum Semantic IR contract/ADR 0108; WP-0025 planning,
  resource, backend, capability, workflow rows; current official hardware
  product and roadmap sources.
- Component boundaries, ports/adapters, and VO/DTO candidates when applicable:
  semantics remain provider-neutral; candidate downstream VOs are
  MachineScaleClass, ComputationModelProfile, DeploymentProfile,
  HierarchicalPlanRef, SymbolicResourceExpr, LogicalResourceBudget,
  PhysicalResourceEstimate, and CapabilitySnapshot. Concrete hardware,
  firmware, cloud, and local-device access remain adapters.
- Applicable constraints: Never Leave the State; no provider types in semantic
  IR; no cloud assumption; no silent fallback; finite Quantum Semantic IR v1;
  target constraints cannot change source meaning.
- Decisions, assumptions, and unresolved ambiguities: Personal Quantum
  Appliance is a design horizon, not current product availability; exact
  capability schema belongs to LISS-0099; continuous-native semantics need a
  separate future decision; ADR 0109 remains Proposed.
- Included and omitted AI context: include public primary hardware roadmaps and
  directly affected architecture contracts; omit provider SDKs, credentials,
  pricing, private roadmaps, and speculative performance claims.
- Task routing (model/assistant/tool): architecture synthesis by capable
  coding agent; public primary-source research by web tools; later profile and
  resource validation by deterministic tests and target fakes.
- Input/output evidence contract when AI output is involved: dated public
  roadmap/product claims and repository contracts in; scale/model-neutral
  design constraints and explicit uncertainty out; no hidden reasoning.
- Verification plan: terminology/dependency/link sync and architecture review;
  no implementation or target adoption in this design batch.
```

## 1. Core decision boundary

The language does not target a number of qubits. It targets **state-transform
meaning** and declares semantic requirements. Planning and target layers decide
whether a particular machine can realize them.

The same source program may be:

- simulated locally;
- executed on a Personal Quantum Appliance;
- submitted to an on-premises laboratory system;
- planned for a modular fault-tolerant facility;
- rejected because the selected target lacks the required computation model,
  scale, fidelity, control, or carrier support.

Target rejection is valid. Silent semantic substitution, remote execution, or
simulator fallback is not.

## 2. Two scale horizons

### 2.1 Utility-scale fault-tolerant horizon

The compiler must tolerate:

- logical rather than source-visible physical carriers;
- millions to hundreds of millions of logical operations;
- modular processors and non-local operations;
- sustained error correction and decoding;
- logical memory, communication, and magic-state resources;
- long-running, partially materialized execution plans.

Therefore no normative IR after Physics IR may require eager expansion to one
flat instruction list. Hierarchical regions, callable subplans, symbolic
repetition, and symbolic resource expressions must survive until the target
requires materialization.

### 2.2 Personal Quantum Appliance horizon

This horizon means a locally owned quantum co-processor with a conventional
host, not necessarily a standalone replacement for a CPU.

The architecture must permit:

- offline source compilation and local execution;
- direct local capability discovery through a port;
- interactive compile/inspect/run latency;
- no cloud account, network, queue, or credential requirement;
- local-only scientific inputs and results by default;
- explicit power, thermal, memory, and execution budgets;
- specialized or small devices that honestly reject unsupported programs;
- firmware/calibration/capability snapshots that can change independently of
  language semantics.

Remote fallback requires an explicit host-workflow decision and user
permission. A local target adapter may not contact a remote service merely
because the local device is insufficient.

## 3. Generalized computation-model horizon

Staqex remains one language, not one surface syntax per hardware modality.

`ComputationModelProfile` is a downstream capability classification, with
candidate families:

- `UniversalDigital`
- `NativeHamiltonianEvolution`
- `MeasurementBased`
- `PhotonicFock`
- `OptimizationSpecialized`
- `Simulator`

These names are candidates, not implementation authorization or a claim that
all profiles are equivalent.

The rules are:

1. Source and Physics IR express physical/state intent.
2. Quantum Semantic IR v1 expresses finite state-transform meaning.
3. Algorithm Plan chooses an accepted realization family.
4. Logical/Target IR records model-specific operations and requirements.
5. A target adapter proves profile compatibility or rejects.

An optimization-specialized or analog target cannot claim to execute arbitrary
digital semantics. A digital gate backend cannot silently discretize a
continuous model. A photonic target cannot reinterpret a qubit register as a
Fock space without an explicit accepted mapping.

## 4. Scale-free semantic constraints

Quantum Semantic IR must:

- use acting-space and Joint-state identities, never device locations;
- permit nested region/call relationships without mandatory inlining;
- keep symbolic parameter and repetition identities;
- avoid fixed carrier-count, depth, or operation-count limits;
- preserve exactness and realization obligations;
- declare required semantic capabilities without provider names;
- remain serializable/versioned for local and remote use;
- reject unknown semantic schema versions.

It must not contain:

- QEC code distance or physical-qubit allocation;
- modular-link routing;
- decoder, calibration, magic-state, or native-gate details;
- household/cloud deployment choice;
- power, price, queue, or credential data.

## 5. Hierarchical planning contract

Algorithm and Logical plans need structure:

```text
PlanModule
  declarations[]
  callable_regions[]
  symbolic_loops[]
  specialization_points[]
  logical_resource_exprs[]
  approximation_and_failure_budgets[]
  target_requirements[]
```

`repeat 10_000_000` remains a symbolic count until a target or exporter
requires expansion. Cost and failure calculations operate on symbolic resource
expressions where possible.

The verifier rejects:

- expansion whose predicted artifact exceeds an approved materialization
  budget;
- recursive or unbounded plan structure without accepted termination
  semantics;
- target-specific data entering Semantic IR;
- loss of source/provenance through plan calls or specialization;
- resource estimates that mix semantic, logical, and physical quantities.

## 6. Three resource levels

Resource reporting distinguishes:

| Level | Examples |
|---|---|
| Semantic | acting-space dimension, state resources, measurements, required transformation kinds |
| Logical | logical qubits/qudits, logical operations, logical depth, logical failure budget, ancillas |
| Physical | physical carriers, code distance, cycles, factories, links, decoder load, power, time, cost |

The levels may be related by an explicit plan, but never collapsed into one
unqualified `qubits` or `gates` field.

## 7. Capability profile

LISS-0099 should define a versioned capability snapshot containing, when
applicable:

- deployment: local, on-premises, remote, modular facility;
- computation-model profile and supported carrier families;
- logical and physical capacity ranges;
- local dimension/qudit support;
- structured control, measurement, reset, feed-forward;
- maximum supported symbolic/materialized plan forms;
- parallelism and module/link topology;
- logical operation/error envelope;
- loss/reload and decoder characteristics;
- timing, power, thermal, memory, cost, and session limits;
- firmware/calibration timestamp and freshness;
- privacy/network behavior.

Unknown and not-applicable are distinct. Provider-specific payloads stay in the
adapter and map into this core-owned snapshot.

## 8. Local execution and privacy

Personal-machine support uses the same core-owned ports as remote/facility
execution:

```text
TargetCapabilityPort
ExecutionPort
CalibrationPort
MeasureSinkPort
```

Names remain candidates for their owning Issues. Local-device, simulator,
on-premises, and remote adapters implement the applicable common port; core
interfaces are not forked merely by deployment. Existing source, RNG, sink,
settings, and job contracts should be reused where their semantics match.

Core compilation and deterministic verification must remain usable without a
network. Local scientific data is not uploaded by default. Any remote
transition is a Host Workflow operation with destination, payload, policy,
cost, and consent evidence.

## 9. Implementation impact by Issue

| Issue | Required design impact |
|---|---|
| LISS-0082 | scale-free Joint identities; nested/callable region capability; no eager flattening; no deployment/model/vendor fields |
| LISS-0083 | hierarchical Algorithm Plan; symbolic repetition/resources; realization-family decision with provenance |
| LISS-0087 | pass contracts preserve hierarchy or justify bounded materialization |
| LISS-0091 | semantic/logical/physical resource separation; failure, power, time, and materialization budgets |
| LISS-0094 | local simulator and accelerator ports share explicit capability/rejection behavior |
| LISS-0097/0098 | exporters preserve structure where the chosen target profile permits and report bounded expansion |
| LISS-0099 | versioned scale/model/deployment capability snapshot |
| LISS-0102 | local/on-premises/remote orchestration; no implicit remote fallback |
| LISS-0120 | Noether Forge reviews local simulation/appliance and future utility planning from one source meaning |

## 10. Review decisions

Adjudicator architecture approval is required for:

1. bidirectional scale horizon;
2. Personal Quantum Appliance as a local co-processor profile;
3. no-eager-flattening rule and hierarchical plan requirement;
4. semantic/logical/physical resource separation;
5. computation-model profiles as downstream capabilities;
6. local-first/no-implicit-remote-fallback policy;
7. proposed ADR 0109;
8. proposed ADR 0110 as a non-normative quantitative stress envelope.

No hardware, SDK, provider, or dependency is selected by approving this
contract.
