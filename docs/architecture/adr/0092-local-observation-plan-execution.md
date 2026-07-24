# ADR 0092: Local observation plan execution boundary

## Status

Accepted for [LISS-0047](../../issues/LISS-0047-local-observation-plan-execution.md) Phase 1 Red.
This acceptance authorizes contract tests only. It does not authorize
provider SDK, network, QPU, or Kernel changes.

## Context

LISS-0044 and LISS-0046 define observation requests, reports, and their
`JobResult` collection. They do not yet produce reports from a local run. A
dependency-free local adapter is needed to validate the end-to-end Host path
before any provider technology is selected.

## Decisions

1. Add a Host-side `ObservationExecutionPort` with
   `execute(plan: ObservationPlan, execution: HostExecutionContext)`. The
   first implementation is a local fake adapter. `HostExecutionContext` is a
   Host-owned opaque context and does not expose source, AST, evaluator, or
   provider objects.
2. The first adapter is represented by `LocalObservationAdapter` and supports
   only `expectation`, `probability`, and `counts`.
   It returns `ObservationReport` values in request order and attaches them to
   `JobResult.observations`.
3. Simulator snapshots remain capability-gated and are not required for the
   first portable execution path. If supported in a later slice, the adapter
   must mark them non-portable.
4. `ObservationValueSource` is an injected port. Phase 1/2 use a deterministic
   `FakeObservationValueSource` with an explicit seed policy. Explicit
   `extra_shots` and `separate_job` values are copied into execution metadata;
   the adapter never creates child Jobs in this slice.
5. Adapter failures become provider-neutral diagnostics and do not expose
   evaluator, AST, or provider objects. Partial-report semantics remain a
   separate decision and are rejected by default in this slice.
6. Unsupported projections produce the hard diagnostic
   `OBSERVATION_PROJECTION_UNSUPPORTED` with projection, target lane, and
   checkpoint context.
7. The adapter is local-only and deterministic under an explicit seed policy.
   No provider SDK, network, persistence, or credential boundary is introduced.

## Non-goals

- Real QPU execution or provider submission.
- Automatic tomography or hidden measurement.
- Dynamic mid-circuit observation.
- Workflow optimizer integration.
- General observable algebra beyond the existing Host request shape.

## Open decisions

- When partial reports and explicit failure completeness are introduced.
- How a future evaluator-backed value source calculates observations from an
  intermediate state without violating terminal measurement semantics.
