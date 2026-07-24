# LISS-0047: Local observation plan execution

## Metadata

- Local issue ID: LISS-0047
- GitHub issue: none
- Status: **Phase 3 reviewed**
- Phase: Feature Path — Phase 3 reviewed
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

## Decision record

- `HostExecutionContext` is the opaque Host input.
- `ObservationValueSource` and `FakeObservationValueSource` provide
  deterministic values.
- `LocalObservationAdapter` executes only portable projections.
- `separate_job` records cost without creating child Jobs.
- Unsupported projections use `OBSERVATION_PROJECTION_UNSUPPORTED`.

## Next gate

Adjudicator review of ADR 0092 and the acceptance specification is required
before Phase 1 Red.

## Phase 1 Red record

- Added [`test_local_observation_plan_execution_red.py`](../../tests/test_local_observation_plan_execution_red.py).
- Tests cover the opaque Host context, deterministic fake source, portable
  report execution, explicit resource accounting, and unsupported projections.
- Production code and existing Job/JobResult implementations are unchanged.

## Phase 2 Green record

- Added `HostExecutionContext`, `ObservationValueSource`,
  `FakeObservationValueSource`, and `LocalObservationAdapter`.
- Portable report execution is deterministic and attaches reports to
  `JobResult.observations`.
- Unsupported projections fail with `OBSERVATION_PROJECTION_UNSUPPORTED`.
- `separate_job` records requested cost without creating child Jobs.
- No provider SDK, network, QPU, or Kernel implementation was added.

## Phase 3 Refactor record

- Added explicit type annotations at the adapter/report boundary.
- Removed an unused import and clarified the acceptance-test module label.
- Preserved all acceptance assertions and the provider-neutral result shape.
- Deterministic verification remained green after the refactor.

Adjudicator final review approved the Phase 3 result.

## Decision memo

[Local observation execution decision memo](../research/2026-07-25-local-observation-execution-decision-memo.md)

Phase 1 Red is intentionally paused until the execution-port input boundary,
deterministic value source, separate-Job semantics, and unsupported-projection
diagnostic are adjudicated.
