# LISS-0066: QPU observation/result integration

## Metadata

- Local issue ID: LISS-0066
- GitHub issue: none
- Status: Phase 3 Refactor complete
- Phase: Architecture Path — Phase 0 Design Intake complete; Feature Path Phase 3 Refactor
- Type: Host execution / observation result boundary
- Priority: P1
- Initial planning size: L
- Owner/agent: Codex
- Depends on: LISS-0044, LISS-0046, LISS-0047, LISS-0065, ADR 0091,
  ADR 0092, ADR 0103
- Related work plan: WP-0004

## Summary

Connect completed provider-neutral QPU jobs to the existing observation and
`JobResult` contracts. A QPU adapter may return portable observation reports
and terminal measurements, but it must not expose provider SDK objects,
internal simulator snapshots, or partial measurements through the Kernel.

The first slice remains provider-neutral and dependency-free. It should use a
deterministic fake QPU job adapter and existing Host ports before any provider
SDK, credential, network, or live-device decision is made.

## [DESIGN CHECK]

- Scope and expected behavior: accept an explicit `ObservationPlan` together
  with a submitted QPU job, wait for a terminal provider-neutral lifecycle
  state, and project successful portable observations into immutable
  `JobResult.observations`. Failed, cancelled, queued, and running jobs must
  not expose measurements or observation values.
- Specifications and files inspected: LISS-0044, LISS-0046, LISS-0047,
  LISS-0065, ADR 0091, ADR 0092, ADR 0103, `compiler/staqex/observation.py`,
  `compiler/staqex/host.py`, `compiler/staqex/qpu_submit.py`, and
  `compiler/staqex/qpu_orchestration.py`.
- Component boundaries, ports/adapters, and VO/DTO candidates: the Host use
  case owns plan validation, lifecycle gating, report projection, and
  provider-neutral diagnostics. `QpuJobPort` remains the lifecycle/result
  port. Candidate DTOs are `QpuObservationRequest`, `QpuObservationResult`,
  and a terminal-result projection carrying `JobResult` plus immutable
  `ObservationReport` values. Provider adapters own provider result mapping;
  no provider type crosses the port.
- Applicable constraints: no provider SDK, credentials, network transport,
  simulator snapshot on the QPU lane, hidden measurement, implicit extra Job,
  silent retry, or partial-result publication. Existing terminal `measure`
  remains distinct from checkpoint observations.
- Decisions, assumptions, and unresolved ambiguities: ADR 0104 accepts a
  structured `QpuJobPort.result()` payload, source-plan ordering, fail-closed
  incomplete-result handling, stable logical identity across explicit attempts,
  and metadata-only `separate_job`. Provider selection and live transport
  remain outside this issue.
- Included and omitted AI context: included the provider-neutral Host DTOs,
  QPU orchestration, observation contracts, and related ADR/LISS documents;
  omitted provider SDK documentation, credentials, cloud account data, and
  live QPU APIs.
- Task routing: strong architectural review for result/lifecycle boundaries;
  deterministic fake-port contract tests after Phase 1 approval.
- Input/output evidence contract: design output is a boundary map with
  explicit DTO fields, lifecycle rules, diagnostics, and acceptance scenarios.
  No provider-specific fact is accepted without a source reference and human
  review.
- Verification plan: cross-check DTO compatibility and existing observation
  invariants, then request Phase 1 Red only after the open decisions below are
  adjudicated.

## Proposed acceptance scenarios

1. A succeeded QPU job with a portable observation plan returns immutable
   `JobResult.observations` with checkpoint, source, target lane, and Job
   identity preserved.
2. A failed or cancelled QPU job returns a terminal diagnostic and no
   measurements or observation values.
3. A queued or running job cannot be projected as a completed result.
4. A QPU observation requesting a simulator-only snapshot is rejected with a
   hard provider-neutral diagnostic.
5. The terminal `measure` result and checkpoint observations remain separate.
6. An explicit retry creates a new attempt while preserving the logical
   idempotency key and does not merge results from different attempts.

## Resolved decisions

See [ADR 0104](../architecture/adr/0104-qpu-observation-result-integration.md):
structured result payload, source-plan ordering, fail-closed incomplete
results, stable logical identity with explicit attempt metadata, and
metadata-only `separate_job`.

## Non-goals

- No provider SDK or credential/authentication implementation.
- No live QPU or cloud integration.
- No new Staqex language syntax.
- No dynamic measurement, POVM expansion, tomography, or simulator snapshot
  on a QPU lane.
- No automatic retry or partial-result recovery.

## Approval gate

ADR 0104 authorizes the provider-neutral result projection contract. Phase 1
Red, Phase 2 Green, and Phase 3 Refactor are complete. Provider selection and
live QPU integration remain out of scope.

## Phase 2 Green record

`compiler/staqex/qpu_observation.py` adds the Host-side
`QpuObservationProjector`. It consumes the existing `QpuJobHandle` and
structured `QpuJobPort.result()` payload, emits reports in source-plan order,
fails closed on incomplete payloads, preserves terminal measurements
separately, and records logical Job/provider Job/attempt metadata. Failed and
cancelled jobs expose no partial values. `QpuJobHandle.result_payload()` is a
small provider-neutral access point for the Host projector; no provider SDK or
network code was added.

Verification: LISS-0066 tests 6 passed; related QPU submit, JobResult
observation, and local observation tests 20 passed.

## Phase 3 Refactor record

The projector now separates execution metadata, incomplete-result creation,
and successful projection into small helpers. The tests use one shared
projection helper while preserving all assertions. No provider policy,
language syntax, or result semantics changed.

### Reviewer empathy summary

- The Host boundary is visible in one projector class and does not require
  knowledge of provider SDK objects.
- Fail-closed behavior is concentrated in one diagnostic helper, making the
  no-fabricated-values rule easy to audit.
- The test fixture deliberately returns observations out of order, so the
  source-plan ordering rule is visible in the acceptance test.

### Verification gap

- Live provider behavior, authentication, network failures, and provider
  payload adapters remain untested by design.
- The repository-wide spec suite still has five pre-existing unrelated example
  failures (160/165); targeted LISS-0066 and related Host tests pass.
