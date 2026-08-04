# WP-0021: Observation checkpoints and execution diagnostics

## Planning record

- Issue: [LISS-0044](../issues/LISS-0044-observation-checkpoints-and-execution-diagnostics.md)
- ADR: [ADR 0089](../architecture/decision-themes/dec-0002-state-first-semantics-and-measurement.md)
- Size: L
- Current phase: Phase 3 Refactor complete
- Branch scope: provider-neutral observation plan and result contract

## Goal

Allow a physicist to request explicit evidence during simulator or QPU
execution without making hidden measurements, exposing QPU state, or mixing
provider policy into the Kernel.

## Dependencies

- LISS-0022 Job/JobResult lifecycle.
- LISS-0028 dynamic QPU capability boundary.
- LISS-0033 Symbolic IR and provenance.
- LISS-0035 Workflow/Job composition.
- LISS-0037 measurement/effect identity.
- ADR 0089.

## Phase 0 design decisions proposed for review

1. Start with a Host/workflow observation plan; defer Staqex source syntax.
2. Treat expectation, probability, counts, and uncertainty as portable
   observation results.
3. Treat state-vector and density snapshots as explicit simulator-only
   capabilities, never as QPU results.
4. Make checkpoint identity, source stage, observable identity, execution lane,
   Job identity, shots/seed policy, target, and provenance mandatory metadata.
5. Represent extra Jobs and shots explicitly; never insert them implicitly.
6. Use a separate preparation/Job model as the portable QPU default. Dynamic
   continuation remains LISS-0028.

## Phase plan

### Phase 0 — Design Intake

Current phase. Review the acceptance specification, ADR open decisions, and
the capability matrix before authorizing Red tests.

### Phase 1 — Red

Only after review: add failing contract tests for no-hidden-observation,
portable versus simulator-only result lanes, provenance, Job ordering, and
explicit resource accounting. No provider or network calls.

Authorized and added in `tests/test_observation_checkpoints_red.py`. All five
scenarios are expected to fail until the Host contract is implemented.

### Phase 2 — Green

Add the smallest provider-neutral observation DTO and local fake/simulator
adapter required by the reviewed tests.

The dependency-free observation DTO and explicit plan accounting are now
implemented. Local execution adapters and JobResult integration remain
deferred to a later slice.

### Phase 3 — Refactor

Review result readability, lane honesty, and separation from terminal measure
and dynamic QPU semantics.

Completed: portable/snapshot vocabularies are centralized, report mappings
remain immutable, and explicit resource accounting remains separate from
execution adapters.

## Non-goals

No provider SDK, credentials, persistence, logging backend, automatic
tomography, arbitrary QPU state inspection, or dynamic measurement semantics.
