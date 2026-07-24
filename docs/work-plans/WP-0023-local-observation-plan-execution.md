# WP-0023: Local observation plan execution

## Planning record

- Issue: [LISS-0047](../issues/LISS-0047-local-observation-plan-execution.md)
- ADR: [ADR 0092](../architecture/adr/0092-local-observation-plan-execution.md)
- Size: M
- Current phase: Phase 3 complete; Adjudicator final review pending
- Branch scope: local observation port and fake/simulator adapter

## Goal

Connect explicit observation plans to completed local JobResults without
introducing provider technology or hidden measurement.

## Dependencies

- LISS-0022 Job/JobResult.
- LISS-0044 ObservationRequest/ObservationPlan.
- LISS-0046 JobResult observations.
- ADR 0065, ADR 0089, and ADR 0091.

## Phase plan

### Phase 0 — Design Intake

Resolved by ADR 0092: opaque HostExecutionContext, injected deterministic fake
value source, hard unsupported-projection diagnostic, and cost-only
separate-job accounting.

Decision memo: [local observation execution decisions](../research/2026-07-25-local-observation-execution-decision-memo.md).
The execution boundary was approved for the dependency-free local adapter.

### Phase 1 — Red

Add failing tests for portable local reports, request ordering, deterministic
seed behavior, explicit resources, unsupported projections, and provider
isolation.

Added in `tests/test_local_observation_plan_execution_red.py`. Green
implementation is complete for the approved local contract.

### Phase 2 — Green

Implement the smallest local fake/simulator adapter and port required by the
reviewed tests. No provider SDK or network. Completed with
`HostExecutionContext`, an injected `ObservationValueSource`, deterministic
fake values, portable `JobResult.observations`, cost-only `separate_job`
metadata, and hard unsupported-projection diagnostics.

### Phase 3 — Refactor

Review adapter thinness, result opacity, deterministic behavior, and
separation from the Kernel evaluator. Completed with explicit boundary type
annotations, removal of an unused import, and clearer acceptance-test
diagnostics. No assertions or behavior changed.

## Non-goals

No QPU submission, provider credentials, network, persistence, dynamic
measurement, automatic tomography, or partial-result policy.
