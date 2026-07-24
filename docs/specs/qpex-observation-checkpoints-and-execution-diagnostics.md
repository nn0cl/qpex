# QPex observation checkpoints and execution diagnostics

## Status

Proposed for LISS-0044 Phase 0 review. This is a design contract only; it does
not authorize parser, runtime, provider, or simulator implementation.

## Design boundary

An observation checkpoint is an explicit Host/workflow execution plan. It is
not a classical read of a mid-program `State<T>`, and it does not change the
existing terminal `measure` rule.

The first contract distinguishes two result lanes:

- Portable observations: expectation values, probabilities, counts, and
  uncertainties that can be produced by a simulator or QPU plan.
- Simulator-only diagnostics: state-vector or density-state snapshots, only
  when explicitly requested and capability-checked.

The proposed Host-side value objects are:

- `ObservationRequest`
- `ObservationReport`
- `SnapshotCapability`
- `CheckpointIdentity`

Exact public names remain subject to ADR 0089 review.

## Proposed acceptance scenarios

### Explicit simulator observation

Given a local simulator and an explicit `ObservationRequest`, when the Job
completes, then the `JobResult` contains an `ObservationReport` with observable
identity, checkpoint identity, Job identity, execution lane, and provenance.

If a state-vector or density snapshot is requested, the request must carry an
explicit simulator-only capability. A snapshot must be marked non-portable.

### QPU observation

Given a QPU target and a portable observation request, when an execution plan is
created, then the plan contains an explicit measurable observation circuit or
Job. The result may contain counts, probabilities, expectations, and
uncertainties, but never an internal QPU state snapshot.

### No hidden observation

Given a program without an observation request, when it is compiled or run,
then no additional measurement, tomography, snapshot, or Job is inserted.

### Ordering and completion

Given multiple checkpoints, when their Jobs complete, each report identifies
its source stage and Job. The final report is observable only after the
associated Job reaches a terminal state.

### Resource honesty

Given a checkpoint requiring additional shots or a separate Job, the execution
plan records that resource cost explicitly. The compiler does not silently
merge, add, or retry observations.

## Hard boundaries

- `measure` remains explicit and terminal in the static Kernel lane.
- The Kernel cannot submit, poll, store, print, or inspect provider data.
- A QPU checkpoint is not assumed to continue the original quantum state;
  separate preparation and Job semantics are the default portable model.
- Dynamic mid-circuit measurement belongs to LISS-0028.
- Automatic tomography and unrestricted state inspection are rejected.

## Open decisions

- Host-only plan versus future QPex checkpoint declaration syntax.
- Exact first-class observable schema and uncertainty fields.
- Separate-Job identity and preparation reuse semantics on each target.
- Inline versus referenced simulator snapshot transport.
- Maximum extra shots and checkpoint resource budget representation.
- Composition with `WorkflowReport` and the existing `JobResult.metadata`.
