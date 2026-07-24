# QPex JobResult observation integration

## Status

Accepted for LISS-0046 Phase 2 Green. The additive dependency-free
`JobResult.observations` contract is authorized; provider integration and QPex
syntax remain out of scope.

## Acceptance scenarios

### Completed Job exposes reports

Given explicit observation requests and a completed Job, when the caller gets
the `JobResult`, then the result exposes the corresponding immutable
`ObservationReport` collection and each report retains its checkpoint, source,
target lane, and Job identity.

### Existing measurement remains distinct

Given a terminal `measure` and one checkpoint, when the Job completes, then the
terminal `MeasurementEnvelope` and checkpoint report remain separate values.
No checkpoint creates an implicit terminal measurement.

### Happens-before ordering

Given a queued or running Job, when the caller requests its result, then the
result is not observable before the Job reaches a terminal state. All attached
reports belong to the completed Job.

### Simulator-only result honesty

Given a simulator-only snapshot report, when it is returned in `JobResult`,
then it is explicitly non-portable. A QPU result cannot contain an internal
state snapshot.

### No observations means no reports

Given a program and Job with no observation requests, when the result is
returned, then the observation collection is empty and no observation Job,
measurement, or tomography is inserted.

## Boundary contract

- `JobResult` remains a Host DTO and never exposes `Joint`, AST, or provider SDK
  objects.
- `ObservationReport` is the only typed carrier for checkpoint results.
- Existing `MeasurementEnvelope` and `WorkflowReport` contracts are preserved.
- Provider adapters and local fake adapters are tested separately from Kernel
  conformance.

## Open design points

Partial failures, report ordering, typed provenance, and WorkflowReport
composition require ADR review before Phase 1 Red.
