# LISS-0046: JobResult observation integration

## Metadata

- Local issue ID: LISS-0046
- GitHub issue: none
- Status: **Phase 3 reviewed**
- Phase: Feature Path — Phase 3 Refactor reviewed
- Type: Host result contract / workflow boundary
- Priority: P1
- Planning size: M
- Depends on: LISS-0022, LISS-0035, LISS-0044, ADR 0065, ADR 0089

## Summary

Connect explicit LISS-0044 observation reports to the provider-neutral
`JobResult` boundary while preserving terminal measurement, Job completion
ordering, and simulator/QPU result honesty.

## In scope

- Additive provider-neutral result contract for observation reports.
- Report identity, ordering, completeness, and provenance requirements.
- Separation of terminal measurements and checkpoint observations.
- Local fake adapter acceptance plan without provider SDKs.

## Out of scope

- Provider SDKs, credentials, retries, sessions, persistence, and network.
- Staqex checkpoint syntax or dynamic mid-circuit measurement.
- Automatic tomography or unrestricted state inspection.
- Replacing existing `MeasurementEnvelope` or `WorkflowReport` semantics.

## Design intake record

- Included: LISS-0022 Job lifecycle, LISS-0035 Workflow boundary, LISS-0044
  Observation contracts, ADR 0065, and ADR 0089.
- Omitted: provider SDKs, credentials, persistence, and implementation code.
- Candidate DTO change: additive immutable `JobResult.observations`.
- Candidate policy: source-ordered reports available only after terminal Job
  completion.
- Open decisions: partial failures, ordering/completeness, typed provenance,
  and WorkflowReport composition.

## Acceptance specification

[Staqex JobResult observation integration](../specs/staqex-jobresult-observation-integration.md)

## Work Plan

[WP-0022](../work-plans/WP-0022-jobresult-observation-integration.md)

## Next gate

Adjudicator review of ADR 0091 and the acceptance specification is required
before Phase 1 Red.

## Phase 1 Red record

- Added [`test_jobresult_observation_integration_red.py`](../../tests/test_jobresult_observation_integration_red.py).
- Tests cover additive observation reports, terminal-measurement separation,
  empty observation results, and Job identity/completion boundary.
- Production `JobResult`, `Job`, and Observation contracts are unchanged.
- Expected Red result: current `JobResult` has no `observations` field.

## Phase 2 Green record

- Added an additive immutable `observations` tuple to `JobResult`.
- Existing measurements, diagnostics, metadata, and Job lifecycle behavior are
  unchanged.
- No provider adapter, network call, checkpoint syntax, or Kernel change was
  added.
- Reviewed integration tests pass without changing their assertions.

## Phase 3 review record

- Moved the additive `observations` field to the end of `JobResult` so
  existing positional construction remains compatible.
- Confirmed reports remain separate from terminal measurements and retain
  immutable observation data.
- Confirmed no provider, persistence, WorkflowReport, or Kernel behavior was
  introduced.
- Reviewer empathy: existing Host callers can adopt observations by keyword
  without learning a new lifecycle or measurement model.
