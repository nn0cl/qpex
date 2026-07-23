# LISS-0015: Effect marking for pure and measure-capable functions

## Metadata

- Local issue ID: LISS-0015
- GitHub issue: none
- Status: proposed
- Phase: Architecture Path first
- Type: language architecture + type system
- Priority: P1
- Initial planning size: L
- Current planning size: TBD
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

## Summary

Define effect marking for `measure`-capable and host-effectful functions while
keeping ordinary `fun`, interface defaults, and class methods pure.

## Acceptance Notes

- [ ] Effect vocabulary and annotation syntax are specified.
- [ ] `measure`, `snapshot`, `inspect`, and host ports have explicit rules.
- [ ] Effect propagation through calls, generics, and modules is specified.
- [ ] Pure-function rejection diagnostics are testable.
- [ ] Terminal-collapse and port boundaries remain intact.

## Dependencies

- Parent: none
- Depends on: ADR 0018, ADR 0029, ADR 0030
- Blocks: effect-aware `until` and Trait method implementation
- Related: LISS-0012, LISS-0014, `io-reasoning-contracts.md`

## Adjudicator Decision Points

- [ ] Use a fixed effect set or extensible effect rows?
- [ ] Is `inspect` pure in language terms but host-effectful in delivery?
- [ ] Can effectful functions return State values?

## Context

- Included: purity, measurement, host sinks, module boundaries.
- Omitted: external provider implementation and secret storage.
- Assumptions: RNG remains behind `RngPort`.

## AI Planning Records

### AIP-0015-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: L
- Intended execution route: Architecture Path only.
- Intended scope: effect contract and diagnostics.
- Estimation basis: typechecker, linker, and port boundary impact.
- Assumptions: no implementation until acceptance.
- Confidence: medium

## Verification

- Future purity/effect conformance suite after the design is accepted.
