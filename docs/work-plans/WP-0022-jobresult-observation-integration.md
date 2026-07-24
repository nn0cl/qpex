# WP-0022: JobResult observation integration

## Planning record

- Issue: [LISS-0046](../issues/LISS-0046-jobresult-observation-integration.md)
- ADR: [ADR 0091](../architecture/adr/0091-jobresult-observation-integration.md)
- Size: M
- Current phase: Phase 2 Green complete
- Branch scope: additive JobResult observation boundary

## Goal

Connect the explicit LISS-0044 observation reports to the existing Job
completion boundary without changing terminal measurement or exposing Kernel
internals.

## Dependencies

- LISS-0022 Job/JobResult.
- LISS-0035 Workflow/Job DTO boundary.
- LISS-0044 ObservationRequest/ObservationReport.
- ADR 0065 and ADR 0089.

## Proposed sequence

### Phase 0 — Design Intake

Resolve report collection shape, partial failure semantics, ordering, typed
provenance, and WorkflowReport composition.

### Phase 1 — Red

Add failing tests for additive result exposure, measurement/report separation,
happens-before completion, simulator-only honesty, and empty-report behavior.

Authorized and added in
`tests/test_jobresult_observation_integration_red.py`. Production code remains
unchanged.

### Phase 2 — Green

Add the smallest immutable `JobResult` integration and local fake adapter
behavior required by the reviewed tests. No provider SDK or network.

Completed with the additive `JobResult.observations` tuple. Provider adapter,
partial-result policy, and WorkflowReport composition remain deferred.

### Phase 3 — Refactor

Review API readability, compatibility of existing callers, and duplication
between measurements, observations, and workflow projections.

## Non-goals

No provider submission, retry/session policy, persistence, QPex syntax, or
dynamic measurement implementation.
