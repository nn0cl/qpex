# LISS-0013: Pipeline and currying surface

## Metadata

- Local issue ID: LISS-0013
- GitHub issue: none
- Status: proposed
- Phase: Architecture Path first
- Type: language architecture
- Priority: P2
- Initial planning size: L
- Current planning size: TBD
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

## Summary

Specify the reserved `|>` pipeline and currying/partial-application surface
for composable state transformers and future Operator Fusion.

## Acceptance Notes

- [ ] Pipeline direction and associativity are normative.
- [ ] Call-chain and partial-application grammar is normative.
- [ ] State/classical type lifting and error cases are specified.
- [ ] Purity, joint preservation, and Operator Fusion boundaries are specified.
- [ ] Phase 1 Red cases are approved before implementation.

## Dependencies

- Parent: none
- Depends on: ADR 0018, ADR 0021, ADR 0032
- Blocks: pipeline/currying implementation and fusion work
- Related: `qpex-ast-design.md`, `qpex-syntax-vocabulary.md`

## Adjudicator Decision Points

- [ ] Choose `lhs |> f` expansion and composition order.
- [ ] Decide whether currying is function-only or supports Operators.
- [ ] Decide whether partial application creates a first-class value.

## Context

- Included: `Pipe` AST placeholder, call chains, pure state transformers.
- Omitted: optimizer implementation and external provider IR.
- Assumptions: no classical escape from State values.

## AI Planning Records

### AIP-0013-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: L
- Intended execution route: Architecture Path only until syntax is accepted.
- Intended scope: syntax and semantics specification.
- Estimation basis: grammar, type system, and optimizer boundary.
- Assumptions: existing `Pipe` node is provisional.
- Confidence: medium

## Verification

- Architecture examples first; parser/typechecker tests only after acceptance.
