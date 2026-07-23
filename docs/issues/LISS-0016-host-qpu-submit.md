# LISS-0016: Host-side QPU submission adapter

## Metadata

- Local issue ID: LISS-0016
- GitHub issue: none
- Status: proposed
- Phase: Architecture Path first
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
identity must remain outside `compiler/qpex/`.

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
- Related: `qpex-backend-targets.md`, `runner-cli-contract.md`

## Adjudicator Decision Points

- [ ] Select first provider adapter, if any; technology approval is separate.
- [ ] Define whether submission is a CLI adapter or library port first.
- [ ] Define job state and retry semantics.

## Context

- Included: emitted QASM, host ports, credentials, job lifecycle.
- Omitted: changing QPex language semantics and compiler-core SDK imports.
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
