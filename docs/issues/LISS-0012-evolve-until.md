# LISS-0012: `evolve until` repetition semantics

## Metadata

- Local issue ID: LISS-0012
- GitHub issue: none
- Status: proposed
- Phase: Architecture Path → Feature Path
- Type: language feature
- Priority: P1
- Initial planning size: L
- Current planning size: TBD
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

## Summary

Define bounded, state-preserving repetition for `evolve ... until`. The feature
must not introduce classical early collapse or an unbounded host loop.

## Acceptance Notes

- [ ] Grammar and AST shape are specified.
- [ ] Predicate domain and evaluation timing are specified without measurement.
- [ ] Maximum-step / nontermination behavior and diagnostics are specified.
- [ ] Deferred RNG law and joint-coordinate preservation are covered by tests.
- [ ] Phase 1 Red scenarios are approved before parser/evaluator changes.

## Dependencies

- Parent: none
- Depends on: ADR 0018, ADR 0028, LISS-0015 effect marking
- Blocks: implementation of `until`
- Related: ADR 0037, `qpex-syntax-vocabulary.md`

## Adjudicator Decision Points

- [ ] Predicate may inspect only State values, or also closed classical values?
- [ ] Require an explicit `max` bound, or define a language default?
- [ ] What result represents a predicate that never becomes true?

## Context

- Included: `evolve`, Joint semantics, termination and diagnostics.
- Omitted: classical `while`, `for`, `break`, and mid-program `measure`.
- Assumptions: `times` and `for` existing behavior remains compatible.

## AI Planning Records

### AIP-0012-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: L
- Intended execution route: Architecture Path, then Feature Path AT-TDD.
- Intended scope: grammar, semantics, tests, and minimal runtime support.
- Estimation basis: parser, typecheck, evaluator, and SV coordination.
- Assumptions: no new dependency.
- Confidence: medium

## Verification

- Future Gherkin scenarios plus full SV suite after implementation approval.
