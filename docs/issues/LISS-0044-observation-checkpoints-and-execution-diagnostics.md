# LISS-0044: Observation checkpoints and execution diagnostics

## Metadata

- Local issue ID: LISS-0044
- GitHub issue: none
- Status: **Phase 3 reviewed**
- Phase: Feature Path — Phase 3 Refactor reviewed
- Type: language/execution boundary and Host result contract
- Priority: P1
- Planning size: L
- Depends on: LISS-0022, LISS-0028, LISS-0033, LISS-0035, LISS-0037, ADR 0089
- Related: LISS-0011, LISS-0016, LISS-0027

## Motivation

Physicists need evidence that a model, discretization, circuit, and execution
are behaving as intended before trusting the final result. The evidence must
work honestly across two different lanes:

- a simulator may expose explicitly requested internal snapshots;
- a QPU exposes only measured observables, counts, probabilities, and metadata.

This issue defines that difference without weakening QPex's explicit terminal
measurement rule or exposing Kernel internals through the Host API.

## Proposed acceptance scenarios

### Scenario A: simulator diagnostic observation

Given a simulator execution and an explicit checkpoint request, the runtime
returns the requested observable and provenance. A state-vector or density
snapshot is returned only when the simulator-only capability is explicitly
requested.

### Scenario B: QPU observation

Given a QPU target and an explicit checkpoint request, the execution plan
contains a measurable observation circuit/Job. The result contains counts,
probabilities, or expectation values, never an unobservable internal state.

### Scenario C: no hidden observation

Given a program without checkpoints, compilation and execution do not insert
additional measurements, tomography, Jobs, or state dumps.

### Scenario D: result ordering

Given multiple checkpoints, each report is associated with a source stage and
Job identity. The final result is available only after its Job completes, in
accordance with the Job happens-before contract.

### Scenario E: resource honesty

Given a checkpoint that requires extra shots or a separate Job, the plan
records that cost explicitly. The compiler does not silently add or merge
observations.

## Boundaries

In scope:

- observation/checkpoint vocabulary and capability matrix;
- simulator-only versus QPU-portable result distinction;
- provider-neutral ObservationReport / JobResult integration;
- provenance, resource accounting, and negative contracts.

Out of scope:

- provider SDKs and credentials;
- automatic tomography;
- arbitrary QPU state inspection;
- dynamic mid-circuit measurement semantics;
- persistence or a logging backend;
- changing terminal `measure` semantics.

## Dependencies and sequencing

1. Resolve the result/provenance relationship with LISS-0022 and LISS-0033.
2. Resolve dynamic-target differences with LISS-0028.
3. Resolve observable/effect identity with LISS-0037.
4. Define the Host/workflow composition with LISS-0035.
5. Only then authorize Phase 1 Red.

## Design intake record

- Context included: ADR 0027 terminal measurement, ADR 0065 Job lifecycle,
  ADR 0071 Dynamic QPU lane, ADR 0075 POVM boundary, and the QPU execution
  research note.
- Context omitted: provider SDK documentation, credentials, persistence
  products, and implementation changes.
- Candidate value objects: `ObservationRequest`, `ObservationReport`,
  `SnapshotCapability`, and `CheckpointIdentity`.
- Ports/adapters: future Host observation/job ports; no Kernel provider
  adapter.
- Ambiguities: surface syntax versus Host-only plan, first-class observables,
  separate-Job semantics, snapshot transport, and resource budgets.
- Acceptance specification: [`qpex-observation-checkpoints-and-execution-diagnostics.md`](../specs/qpex-observation-checkpoints-and-execution-diagnostics.md)
- Work Plan: [`WP-0021`](../work-plans/WP-0021-observation-checkpoints-and-execution-diagnostics.md)
- Implementation status: Phase 1 Red contract tests are authorized; no
  production implementation is authorized.

## Phase 1 Red record

- Added [`test_observation_checkpoints_red.py`](../../tests/test_observation_checkpoints_red.py).
- Tests cover portable report provenance, simulator-only snapshots, QPU
  snapshot rejection, no hidden observations, and explicit resource costs.
- Production code and existing `JobResult` remain unchanged.
- Expected Red result: `compiler.qpex.observation` does not yet exist.

## Phase 2 Green record

- Added dependency-free Host value objects and explicit resource accounting in
  `compiler/qpex/observation.py`.
- Exported the contract from `compiler.qpex`.
- Kept terminal `measure`, `JobResult`, provider adapters, and simulator
  execution unchanged.
- Reviewed observation contract tests pass without changing their behavior.

## Phase 3 review record

- Centralized lane and projection vocabularies to keep portable and
  simulator-only result policies readable and consistent.
- Confirmed immutable report mappings and explicit plan resource accounting.
- Confirmed no hidden measurement, state inspection, provider call, or
  `JobResult` mutation was introduced.
- Reviewer empathy: a QPU reader can distinguish measurable reports from
  simulator-only snapshots directly from `ObservationRequest.portable`.
