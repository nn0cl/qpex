# LISS-0016: Host-side QPU submission adapter

## Metadata

- Local issue ID: LISS-0016
- GitHub issue: none
- Status: **Phase 3 reviewed**
- Phase: Feature Path complete for the provider-neutral contract slice
- Type: adapter + integration architecture
- Priority: P2
- Initial planning size: L
- Current planning size: TBD
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

## Summary

Define an optional host-side adapter that submits emitted OpenQASM to Braket
or another provider. Provider SDKs, credentials, retries, polling, and job
identity must remain outside `compiler/staqex/`.

## Acceptance Notes

- [ ] Host adapter port and provider-neutral request/result DTOs are specified.
- [ ] Credential and settings boundaries are specified.
- [ ] Submit idempotency, polling, failure, and resume behavior are specified.
- [ ] No provider SDK enters the Kernel or compiler core.
- [ ] A local fake adapter test path exists before real integration.

## Dependencies

- Parent: none
- Depends on: ADR 0059, ADR 0036, LISS-0019
- Blocks: real cloud/QPU submit workflow
- Related: `staqex-backend-targets.md`, `runner-cli-contract.md`

## Adjudicator Decision Points

- [ ] Select first provider adapter, if any; technology approval is separate.
- [ ] Define whether submission is a CLI adapter or library port first.
- [ ] Define job state and retry semantics.

## Context

- Included: emitted QASM, host ports, credentials, job lifecycle.
- Omitted: changing Staqex language semantics and compiler-core SDK imports.
- Assumptions: OpenQASM emission remains the Kernel boundary.

## AI Planning Records

### AIP-0016-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: L
- Intended execution route: Architecture Path; technology selection later.
- Intended scope: provider-neutral port and fake adapter contract.
- Estimation basis: external boundary, credentials, and recovery behavior.
- Assumptions: no provider is selected by this issue.
- Confidence: medium

## Verification

- Contract tests with a fake adapter; no live provider required for core tests.

## Design Note

- Target behavior: submit emitted OpenQASM through a provider-neutral Host port
  without importing SDKs, credentials, or retry policy into `compiler/staqex/`.
- Phase to execute next: Architecture review; Phase 1 Red is intentionally not
  started because job/retry semantics and the first adapter boundary remain
  open.
- Context included: ADR 0059, ADR 0065, the accepted Job specification,
  `OpenQASM3Generator`, `JobResult`, `JobRequest`, and existing workflow DTOs.
- Context omitted: live provider documentation, credentials, SDK installation,
  cloud account configuration, and changes to Staqex language semantics.
- VO/DTO candidates: immutable `QpuSubmitRequest`, `QpuArtifact`,
  `ProviderJobId`, `ProviderJobState`, `QpuSubmitError`, and opaque
  `QpuResult`; provider names and SDK objects stay in adapters.
- Ports/adapters: `QpuSubmitPort` and `QpuJobPort` in the Host/application
  boundary; Braket/IBM/local fake implementations remain adapters.
- Suggested task routing: strong reasoning for retry/idempotency and security
  policy; deterministic fake-adapter contract tests after acceptance.
- Ambiguities requiring Adjudicator decision: CLI adapter versus library port
  first, lifecycle state vocabulary, idempotency key ownership, retry/resume
  semantics, and whether any provider is selected for the first adapter.

## Proposed architecture direction

1. The compiler emits an immutable `QpuArtifact` containing OpenQASM text,
   target profile, provenance, and a content hash. It never submits directly.
2. `QpuSubmitPort.submit(request) -> ProviderJobId` is the only submission
   operation. `QpuJobPort.status/wait/result/cancel` handles lifecycle through
   provider-neutral DTOs.
3. The first implementation should be a local fake adapter and CLI/library
   boundary contract. No provider SDK or credential implementation is required
   for the Kernel or core tests.
4. Retry, idempotency, cancellation, and resume must be explicit request and
   result fields; no adapter may silently resubmit a non-idempotent job.

## Architecture decision record

Proposed [ADR 0083](../architecture/adr/0083-provider-neutral-qpu-submit-port.md).

Adjudicator decision (2026-07-24): Python library port first; fixed lifecycle
states; Host-owned idempotency keys; explicit retry only; opaque Provider Job
IDs; local fake adapter first. ADR 0083 is Accepted and Phase 1 Red is
authorized.

## Phase 1 Red record

- Added [`test_qpu_submit_red.py`](../../tests/test_qpu_submit_red.py).
- The Red contract covers immutable QPU artifact provenance/hash, Host-owned
  idempotency keys, explicit retry policy, fixed lifecycle states, and opaque
  provider job identifiers/ports.
- The suite is intentionally Red because the Host submission port and DTOs do
  not yet exist. No provider SDK or production adapter was added.

## Phase 2 Green record

- Added dependency-free immutable `QpuArtifact`, `QpuSubmitRequest`, and
  opaque `ProviderJobId` DTOs.
- Added fixed `ProviderJobState` values and `QpuSubmitPort`/`QpuJobPort`
  protocols.
- Exported the contract through the Python package API. No provider SDK,
  credential store, network call, or automatic retry was added.

## Phase 3 Refactor record

- Kept the Host contract in a dedicated `qpu_submit.py` module and exposed only
  the provider-neutral DTOs and ports from the package root.
- Reviewer empathy summary: provider adapters can depend on a small stable
  contract without importing compiler internals or exposing provider objects
  to Staqex code.

Verification: the QPU submit contract, all standalone tests, spec verification
(165/165), bytecode compilation, and `git diff --check` pass.
