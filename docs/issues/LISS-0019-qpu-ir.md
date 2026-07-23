# LISS-0019: Concrete QPU IR boundary

## Metadata

- Local issue ID: LISS-0019
- GitHub issue: none
- Status: proposed
- Phase: Architecture Path first
- Type: architecture + backend boundary
- Priority: P2
- Initial planning size: L
- Current planning size: TBD
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

## Summary

Determine whether QPex needs a concrete QPU IR between the Kernel amplitude
model and OpenQASM/host adapters, and define its ownership if it does.

## Acceptance Notes

- [ ] Need for an intermediate QPU IR is demonstrated by a concrete use case.
- [ ] IR ownership, lifecycle, and ports are specified if retained.
- [ ] Relation to DAG IR and OpenQASM emission is explicit.
- [ ] State/measurement semantics cannot be weakened by lowering.
- [ ] No provider-specific IR is adopted without technology approval.

## Dependencies

- Parent: none
- Depends on: ADR 0032, ADR 0059, LISS-0016
- Blocks: multi-backend QPU lowering beyond OpenQASM
- Related: `qpex-backend-targets.md`, LISS-0011

## Adjudicator Decision Points

- [ ] Keep OpenQASM as the only public backend IR or add an internal IR?
- [ ] Which backend requirement justifies the additional layer?
- [ ] Which semantics are forbidden to encode as provider-specific behavior?

## Context

- Included: current DAG IR, OpenQASM 3, future QPU ports.
- Omitted: cloud submission implementation and provider SDK selection.
- Assumptions: CPU Kernel remains authoritative.

## AI Planning Records

### AIP-0019-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: L
- Intended execution route: Architecture Path only.
- Intended scope: boundary decision and non-goals.
- Estimation basis: potential new subsystem and backend consequences.
- Assumptions: no IR code is authorized by this issue.
- Confidence: medium

## Verification

- Architecture dependency review and backend portability examples after acceptance.
