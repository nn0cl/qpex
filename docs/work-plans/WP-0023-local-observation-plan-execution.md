# WP-0023: Local observation plan execution

## Planning record

- Issue: [LISS-0047](../issues/LISS-0047-local-observation-plan-execution.md)
- ADR: [ADR 0092](../architecture/adr/0092-local-observation-plan-execution.md)
- Size: M
- Current phase: Phase 0 Design Intake
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

Resolve the port input boundary, deterministic value source, unsupported
projection diagnostics, and separate-job accounting.

### Phase 1 — Red

Add failing tests for portable local reports, request ordering, deterministic
seed behavior, explicit resources, unsupported projections, and provider
isolation.

### Phase 2 — Green

Implement the smallest local fake/simulator adapter and port required by the
reviewed tests. No provider SDK or network.

### Phase 3 — Refactor

Review adapter thinness, result opacity, deterministic behavior, and
separation from the Kernel evaluator.

## Non-goals

No QPU submission, provider credentials, network, persistence, dynamic
measurement, automatic tomography, or partial-result policy.
