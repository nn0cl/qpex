# LISS-0018: Numerical and physical representation follow-ups

## Metadata

- Local issue ID: LISS-0018
- GitHub issue: none
- Status: proposed
- Phase: Architecture Path first
- Type: architecture + numerical semantics
- Priority: P2
- Initial planning size: L
- Current planning size: TBD
- Reclassification reason: grouped related technology evaluations before implementation.
- Owner/agent: TBD
- Related branch: none yet

## Summary

Resolve the remaining representation questions: SI dimensions beyond `(L, M,
T)`, continuous PDF/Monte Carlo samples, exact rational versus `f64` masses,
and numeric literal versus `dirac` sugar.

## Acceptance Notes

- [ ] Each representation has an explicit scope or is rejected/deferred.
- [ ] Precision, normalization, sampling, and serialization policies are recorded.
- [ ] Dimension expansion does not change existing accepted programs silently.
- [ ] Numeric literal lifting has a normative rule.
- [ ] Separate follow-on Issues are created if the scope cannot remain unified.

## Dependencies

- Parent: none
- Depends on: ADR 0014, ADR 0018, ADR 0037
- Blocks: continuous-state or exact-probability implementation
- Related: `qpex-dimensional-types.md`, `qpex-type-system.md`

## Adjudicator Decision Points

- [ ] Which item, if any, is prioritized for the next Kernel generation?
- [ ] Is `f64` retained as MVP storage with exact arithmetic only at the boundary?
- [ ] Are continuous distributions a Kernel capability or a separate port?

## Context

- Included: current PMF/amplitude representation and dimensional typing.
- Omitted: density matrices (LISS-0011) and QPU IR (LISS-0019).
- Assumptions: existing examples remain numerically compatible.

## AI Planning Records

### AIP-0018-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: L
- Intended execution route: Architecture Path research and triage only.
- Intended scope: classify and prioritize representation questions.
- Estimation basis: multiple independent numerical decisions.
- Assumptions: no implementation implied by classification.
- Confidence: medium

## Verification

- Decision matrix and representative numerical fixtures after scope acceptance.
