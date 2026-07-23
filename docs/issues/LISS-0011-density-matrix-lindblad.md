# LISS-0011: Density matrix and Lindblad CPTP semantics

## Metadata

- Local issue ID: LISS-0011
- GitHub issue: none
- Status: proposed
- Phase: Architecture Path first
- Type: architecture + language semantics
- Priority: P1
- Initial planning size: XL
- Current planning size: TBD
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

## Summary

Specify the mixed-state extension covered by ADR 0057: density matrices,
partial trace, and completely positive trace-preserving Lindblad evolution.
This issue is design-only until the representation and `State<T>` boundary are
accepted.

## Acceptance Notes

- [ ] ADR 0057 is updated or superseded with an accepted representation.
- [ ] Pure-state compatibility and `measure` collapse semantics are specified.
- [ ] CPTP/Lindblad time evolution and trace preservation have observable cases.
- [ ] Partial trace and subsystem composition have typed boundaries.
- [ ] Kernel/SV scope and non-goals are recorded before implementation.

## Dependencies

- Parent: none
- Depends on: ADR 0018, ADR 0016, LISS-0019 if concrete QPU IR is needed
- Blocks: mixed-state Kernel implementation
- Related: ADR 0057, `docs/architecture/qpex-stdlib-combinators.md`

## Adjudicator Decision Points

- [ ] Choose density matrix representation and ownership of trace/positivity checks.
- [ ] Decide whether Lindblad is Kernel CPU-only MVP or a later port.
- [ ] Define terminal measurement and host-sink behavior for mixed states.

## Context

- Included: density matrices, CPTP maps, Lindblad evolution, partial trace.
- Omitted: vendor QPU APIs, quantum chemistry, and pulse-level simulation.
- Assumptions: Never Leave the State remains the language law.

## AI Planning Records

### AIP-0011-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: XL
- Intended execution route: Architecture Path; no implementation.
- Intended scope: accepted representation and observable semantics only.
- Estimation basis: new state model and multiple architecture boundaries.
- Assumptions: no third-party dependency is selected.
- Confidence: medium

## Verification

- Architecture review checklist and future Gherkin/SV plan; no code verification until acceptance.
