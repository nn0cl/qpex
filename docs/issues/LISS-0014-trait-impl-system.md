# LISS-0014: Trait `impl` and `system` expression model

## Metadata

- Local issue ID: LISS-0014
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

Resolve the remaining abstraction-layer questions in ADR 0019: concrete Trait
`impl` syntax, bounds, and whether `system` is a first-class expression or a
declaration-only package.

## Acceptance Notes

- [ ] `interface` / Trait and `impl` grammar is specified.
- [ ] Coherence, overlap, bounds, and method lookup rules are specified.
- [ ] `system` expression/declaration choice is recorded in an ADR.
- [ ] Pure transformer and `State<T>` preservation rules are testable.
- [ ] No implementation begins before architecture acceptance.

## Dependencies

- Parent: none
- Depends on: ADR 0019, ADR 0024, ADR 0056, LISS-0015
- Blocks: generic trait implementation
- Related: `qpex-abstraction-model.md`

## Adjudicator Decision Points

- [ ] Use explicit `impl Trait for Type`, inherent impls, or both?
- [ ] Is coherence enforced at module link time or typecheck time?
- [ ] Are `system` values constructible expressions?

## Context

- Included: interfaces, generics, immutable classes, pure methods.
- Omitted: inheritance, mutable objects, concurrency, and provider SDKs.
- Assumptions: retired `trait` spelling remains non-normative.

## AI Planning Records

### AIP-0014-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: L
- Intended execution route: Architecture Path only.
- Intended scope: type and declaration contracts.
- Estimation basis: cross-cutting parser/typechecker/linker design.
- Assumptions: no Rust-only semantics.
- Confidence: medium

## Verification

- Future type-system Gherkin/SV cases after ADR acceptance.
