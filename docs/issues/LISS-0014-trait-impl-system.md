# LISS-0014: Trait `impl` and `system` expression model

## Metadata

- Local issue ID: LISS-0014
- GitHub issue: none
- Status: **Phase 3 reviewed**
- Phase: Feature Path complete for the interface-impl/system MVP boundary
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
- Related: `staqex-abstraction-model.md`

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

## Phase 1 Red record

- Added [`test_trait_impl_system_red.py`](../../tests/test_trait_impl_system_red.py).
- The Red contract covers explicit `impl Interface for Type`, inline
  `<T: Interface>` bounds, marker `System`, post-merge duplicate coherence,
  prohibition of `pub` inside `impl`, and rejection of a general `system`
  value constructor.
- The suite is intentionally Red because the parser, AST, and typechecker do
  not yet implement the accepted surface. No production code was changed.

## Phase 2 Green record

- Added `ImplDecl`, interface type parameters, and inline generic bound storage
  to the AST.
- Added parsing for `impl Interface for Type`, interface type parameters, and
  `<T: Interface>` function bounds.
- Added linked-unit duplicate coherence diagnostics,
  `IMPL_COHERENCE_ERROR`, and `IMPL_VISIBILITY_ERROR` for `pub` in impl blocks.
- Registered `System`/interface names as non-constructible type contracts and
  emit `SYSTEM_EXPRESSION_ERROR` for general interface constructors.
- No runtime trait objects, dispatch, specialization, or inherent impl syntax
  were added.

Verification: the trait impl/system contract, all standalone tests, spec
verification (165/165), bytecode compilation, and `git diff --check` pass.

## Phase 3 Refactor record

- Extracted inline generic-bound parsing and impl-contract validation into
  dedicated parser/typechecker helpers.
- Preserved the accepted syntax, marker `System` semantics, linked coherence
  rule, and impl visibility diagnostics.
- Runtime dispatch, specialization, inherent impl blocks, and trait objects
  remain deferred.

Reviewer empathy summary: generic syntax and impl validation now each have one
named responsibility, making the parser and linked-program checks easier to
review without changing the accepted behavior.

Verification: all standalone `tests/test_*.py` scripts, the trait impl/system
contract, spec verification (165/165), bytecode compilation, and
`git diff --check` pass.

## Design Note

- Target behavior: add explicit pure interface implementation and clarify the
  boundary between declaration-level physical systems and runtime values.
- Phase to execute next: Architecture review; Phase 1 Red is intentionally not
  started because the surface and coherence policy are still open.
- Context included: ADR 0019, ADR 0024, ADR 0056, completed LISS-0015/ADR 0081,
  `staqex-abstraction-model.md`, `staqex-language-spec.md`, and existing
  `interface`/`class` parser and typechecker behavior.
- Context omitted: inheritance, mutable objects, concurrency, Provider SDKs,
  and generic trait implementation beyond the first coherence slice.
- VO/DTO candidates: immutable `ImplContract` containing interface, target
  type, bounds, and method signatures; no runtime trait object is introduced.
- Ports/adapters: none; this is a Kernel type/declaration boundary.
- Suggested task routing: strong reasoning review for the architecture
  decision, then deterministic parser/typechecker tests after acceptance.
- Ambiguities requiring Adjudicator decision: explicit `impl Interface for Type`
  versus inherent impls, module-link versus typecheck coherence, and whether a
  `system` can be constructed as an expression.

## Proposed architecture direction

1. Adopt explicit `impl Interface for Type` only for the first slice. Existing
   `class` methods remain the inherent-method mechanism; a second inherent
   `impl Type` form is not needed yet.
2. Check coherence after module graph merge and before type checking/lowering:
   one `(Interface, Type)` implementation per linked program, with duplicate
   and overlapping implementations as hard diagnostics.
3. Keep bounds explicit and pure. The first accepted grammar should support
   interface bounds only; no specialization, negative bounds, or inheritance.
4. Treat `system` as a declaration-level scientific contract, not a
   constructible expression. Runtime values use `class` constructors and
   implement the `System` interface; methods return new immutable values and
   preserve `State<T>` semantics.
5. Keep the existing `system()` spelling only where an already accepted
   static-Hilbert allocation contract requires it; it must not become the
   general abstraction-layer system value constructor.

## Architecture decision record

[ADR 0082](../architecture/adr/0082-interface-impl-and-system-boundary.md) is
Accepted (2026-07-24). The Adjudicator approved inline `<T: Interface>` bounds,
post-merge coherence only, marker `System`, and no `pub` inside `impl` blocks.
Phase 1 Red is authorized.
