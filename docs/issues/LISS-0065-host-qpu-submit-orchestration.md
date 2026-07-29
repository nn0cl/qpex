# LISS-0065: Host QPU submit orchestration

## Metadata

- Local issue ID: LISS-0065
- GitHub issue: none
- Status: Phase 3 Refactor complete
- Phase: Architecture Path — Phase 0 Design Intake complete; Feature Path Phase 3 Refactor complete
- Type: Host execution orchestration
- Priority: P1
- Initial planning size: L
- Owner/agent: Codex
- Depends on: LISS-0016, LISS-0022, LISS-0041, LISS-0064, ADR 0083, ADR 0103
- Related work plan: WP-0004

## Summary

Connect the provider-neutral OpenQASM artifact produced by the compiler to the
existing Host `Job` boundary without selecting or importing a provider SDK.
The first implementation slice should be a deterministic local fake adapter
and a Python library port, so researchers can exercise submission, lifecycle,
and result handling before any cloud account or device integration exists.

The compiler remains responsible for compilation, provenance, and explicit
capability/resource rejection. The Host orchestration layer owns submission,
job identity, polling, cancellation, retry requests, and conversion to the
existing provider-neutral `JobResult` boundary.

## [DESIGN CHECK]

- Scope and expected behavior: accept a compiled QASM artifact and explicit
  target/job settings, submit through a provider-neutral Host port, return an
  opaque provider job identifier, and expose deterministic status/wait/result
  behavior through the existing Job boundary.
- Specifications and files inspected: ADR 0083, LISS-0016, LISS-0022,
  LISS-0041, LISS-0064, `compiler/staqex/qpu_submit.py`,
  `compiler/staqex/host.py`, `compiler/staqex/codegen_qasm.py`, and the existing
  Job/JobResult tests.
- Component boundaries, ports/adapters, and VO/DTO candidates: the compiler
  produces an immutable `QpuArtifact`; a Host/application use case consumes it
  through `QpuSubmitPort` and `QpuJobPort`. Provider objects, credentials,
  network clients, and SDK exceptions remain in adapters. Candidate DTOs are
  `SubmitJobRequest`, `ProviderJobId`, `ProviderJobState`, and a result/error
  envelope that can map into `JobResult` without exposing provider values.
- Applicable constraints: no provider SDK, credential store, network call,
  automatic retry, or cloud-specific target is introduced in the first slice.
  Retry and cancellation must be explicit operations; no adapter may silently
  resubmit a non-idempotent job. QASM artifacts rejected by resource or
  capability checks must never reach the submit port.
- Decisions, assumptions, and unresolved ambiguities: ADR 0083 already
  selects the Python library port first, fixed lifecycle states, Host-owned
  idempotency keys, opaque provider job IDs, explicit retry, and a local fake
  adapter. The accepted orchestration mapping, lifecycle, partial-result, and
  retry decisions are recorded in ADR 0103. Provider selection remains out of
  scope and requires separate technology approval.
- Included and omitted AI context: included ADR 0083, LISS-0016/0022/0041/0064,
  QASM artifact/IR and Job DTOs, and existing contract tests; omitted provider
  SDK documentation, credentials, cloud account data, and live device APIs.
- Task routing: strong architectural review for lifecycle/idempotency and
  security boundaries; deterministic local fake-adapter contract tests after
  Phase 1 approval.
- Input/output evidence contract: design output is a boundary map with
  explicit DTO fields, lifecycle states, error categories, and fake-adapter
  acceptance scenarios. No AI-derived provider facts are accepted without
  source references and human review.
- Verification plan: inspect existing port and Job DTO compatibility, define
  Gherkin scenarios for fake submit/status/result/cancel/retry, and request
  Phase 1 Red only after the remaining lifecycle decisions are accepted.

## Existing accepted baseline

ADR 0083 and LISS-0016 already establish:

- Python library port first;
- provider-neutral `QpuSubmitPort` and `QpuJobPort`;
- fixed lifecycle state vocabulary;
- Host-owned idempotency keys;
- opaque provider job identifiers;
- explicit retry only;
- local fake adapter before any real provider adapter.

LISS-0064 establishes that an over-budget QASM/QPU request is rejected before
submission. LISS-0065 must consume that rejection result rather than duplicate
resource policy.

## Non-goals

- No Braket, IBM, or other provider selection.
- No authentication, credential storage, network transport, or SDK dependency.
- No automatic retry, polling loop, or background worker hidden inside an
  adapter.
- No changes to Staqex language syntax or Kernel semantics.
- No provider-specific result schema in `compiler/staqex/`.

## Accepted architecture decisions

- QPU submission uses a dedicated Host use case; `submit_source` and
  `submit_path` remain local execution entry points.
- `JobRequest` and `QpuArtifact` remain separate and map explicitly into
  `QpuSubmitRequest`.
- Lifecycle states remain `queued`, `running`, `succeeded`, `failed`, and
  `cancelled`.
- Only successful jobs carry measurements; failed/cancelled jobs do not expose
  partial measurements.
- `QpuSubmitRequest` carries a one-based explicit `attempt`; automatic retry
  is forbidden.
- Provider-neutral error codes are defined in [ADR 0103](../architecture/adr/0103-host-qpu-submit-orchestration.md).

## Phase 1 Red record

`tests/test_host_qpu_submit_orchestration_red.py` defines the accepted contract
using deterministic in-memory fake ports. It covers the dedicated Host use
case, explicit `JobRequest` to `QpuSubmitRequest` mapping, fixed lifecycle
states, rejection of measurements for failed/cancelled jobs, explicit
cancellation, and explicit retry attempts with a stable idempotency key.

The test file was intentionally Red before implementation: the expected
`compiler.staqex.qpu_orchestration` Host use case did not exist. Phase 2 added
the minimal provider-neutral orchestration service and the explicit
`QpuSubmitRequest.attempt` field. The six LISS-0065 tests now pass, as do the
existing QPU submit, Host Job, and Workflow contract tests (19 tests total).
No provider SDK, credential, or network implementation was added.

## Approval gate

Architecture decisions are recorded in ADR 0103. Phase 3 preserves the
provider-neutral boundary while separating unavailable-result construction,
successful-result conversion, and measurement conversion into small private
functions. Provider technology selection and provider integration remain out
of scope.
