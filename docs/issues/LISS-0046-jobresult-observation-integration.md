# LISS-0046: JobResult observation integration

## Metadata

- Local issue ID: LISS-0046
- GitHub issue: none
- Status: **Phase 0 Design Intake**
- Phase: Architecture Path — Phase 0 review
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
- QPex checkpoint syntax or dynamic mid-circuit measurement.
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

[QPex JobResult observation integration](../specs/qpex-jobresult-observation-integration.md)

## Work Plan

[WP-0022](../work-plans/WP-0022-jobresult-observation-integration.md)

## Next gate

Adjudicator review of ADR 0091 and the acceptance specification is required
before Phase 1 Red.
