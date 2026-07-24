# ADR 0092: Local observation plan execution boundary

## Status

Proposed for [LISS-0047](../../issues/LISS-0047-local-observation-plan-execution.md) Phase 0 review.
This ADR does not authorize provider SDK, network, QPU, or Kernel changes.

## Context

LISS-0044 and LISS-0046 define observation requests, reports, and their
`JobResult` collection. They do not yet produce reports from a local run. A
dependency-free local adapter is needed to validate the end-to-end Host path
before any provider technology is selected.

## Decision proposal

1. Add a Host-side `ObservationExecutionPort` implemented first by a local
   fake/simulator adapter. The port receives a completed or locally executable
   Job context and an immutable `ObservationPlan`.
2. The first adapter supports only `expectation`, `probability`, and `counts`.
   It returns `ObservationReport` values in request order and attaches them to
   `JobResult.observations`.
3. Simulator snapshots remain capability-gated and are not required for the
   first portable execution path. If supported in a later slice, the adapter
   must mark them non-portable.
4. Explicit `extra_shots` and `separate_job` values are copied into the
   execution report/metadata. The adapter never invents additional work.
5. Adapter failures become provider-neutral diagnostics and do not expose
   evaluator, AST, or provider objects. Partial-report semantics remain a
   separate decision and are rejected by default in this slice.
6. The adapter is local-only and deterministic under an explicit seed policy.
   No provider SDK, network, persistence, or credential boundary is introduced.

## Non-goals

- Real QPU execution or provider submission.
- Automatic tomography or hidden measurement.
- Dynamic mid-circuit observation.
- Workflow optimizer integration.
- General observable algebra beyond the existing Host request shape.

## Open decisions

- Exact port method and fake adapter name.
- Whether the local adapter consumes source, compiled unit, or a Job request.
- How expectation/probability/counts are calculated from the simulator.
- Whether `separate_job` creates multiple local Job objects or only metadata.
- When partial reports and explicit failure completeness are introduced.
