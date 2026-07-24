# LISS-0047: Local observation plan execution

## Metadata

- Local issue ID: LISS-0047
- GitHub issue: none
- Status: **Phase 0 Design Intake**
- Phase: Architecture Path — Phase 0 review
- Type: Host port / local simulator adapter / JobResult integration
- Priority: P1
- Planning size: M
- Depends on: LISS-0022, LISS-0044, LISS-0046, ADR 0065, ADR 0089, ADR 0091

## Summary

Execute the explicit LISS-0044 observation plan through a local
Simulator/Fake adapter and return portable reports through the existing
`JobResult.observations` boundary.

## In scope

- Local `ObservationExecutionPort` boundary.
- Expectation, probability, and counts projections.
- Request ordering, deterministic seed, Job identity, and explicit resource
  accounting.
- Provider-neutral unsupported-projection diagnostics.

## Out of scope

- Provider SDKs, network, credentials, persistence, and real QPU execution.
- Snapshot execution, dynamic measurement, tomography, and partial reports.
- Workflow optimizer integration or QPex checkpoint syntax.

## Design intake record

- Included: LISS-0044 ObservationPlan, LISS-0046 JobResult integration, and
  LISS-0022 Job lifecycle.
- Omitted: provider adapters, cloud accounts, persistence, and Kernel changes.
- Candidate port: `ObservationExecutionPort`.
- Candidate adapter: `LocalObservationAdapter` or `FakeObservationAdapter`.
- Open decisions: port input shape, deterministic value source, and separate
  Job representation.

## Acceptance specification

[QPex local observation plan execution](../specs/qpex-local-observation-plan-execution.md)

## ADR

[ADR 0092](../architecture/adr/0092-local-observation-plan-execution.md)

## Work Plan

[WP-0023](../work-plans/WP-0023-local-observation-plan-execution.md)

## Next gate

Adjudicator review of ADR 0092 and the acceptance specification is required
before Phase 1 Red.
