# LISS-0012: `evolve until` repetition semantics

## Metadata

- Local issue ID: LISS-0012
- GitHub issue: none
- Status: **Runtime complete** (grammar, type boundary, and Joint evaluator)
- Phase: Feature Path — Phase 3 reviewed for runtime slice (2026-07-27)
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
- Related: ADR 0037, `staqex-syntax-vocabulary.md`

## Adjudicator Decision Points

- [ ] Predicate may inspect only State values, or also closed classical values?
- [ ] Require an explicit `max` bound, or define a language default?
- [ ] What result represents a predicate that never becomes true?

### Accepted backend boundary (2026-07-27)

The Kernel language lane accepts a syntactically and statically valid bounded
`evolve ... until` expression even when no backend lowering exists yet. The
QPU/OpenQASM emission boundary rejects runtime repetition with
`E_QPU_UNSUPPORTED_CAPABILITY`. It must not reject the source during ordinary
Kernel compilation, silently unroll to a fixed circuit, or fall back to a Host
loop.

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

## Architecture design intake

`evolve ... until` must remain a pure Kernel repetition construct and must not
be confused with the Host workflow `until` declaration from LISS-0035.

### Recommended MVP semantics

- Predicate inputs are `State<T>`/joint-preserving values only; `measure`, RNG,
  `Job`, `Host<T>`, and provider values are not visible.
- The repetition requires an explicit positive `max` bound. No language-wide
  default is inferred.
- The predicate is evaluated after each pure evolution step without sampling.
- If the predicate becomes true, the current `State<T>` result is returned.
- If `max` is reached first, compilation/runtime reports a stable hard
  `EVOLVE_UNTIL_MAX_STEPS_ERROR`; it does not silently return a partial state or
  collapse the state.
- The predicate must be deterministic over the current joint/state and may not
  mutate outer bindings.

### Proposed surface for review

```staqex
state result = evolve psi under H for 1 until converged(psi) max 64
```

The exact grammar and predicate vocabulary remain subject to Phase 1 Red
review. This syntax is not implementation authorization.

### Boundary with workflow `until`

```text
Kernel evolve-until: pure State-preserving repetition, no Job/result access
Host workflow until: completed JobResult projection and Host callback policy
```

Architecture Approval is recorded in [ADR 0079](../architecture/adr/0079-evolve-until-kernel-semantics.md).

Phase 1 Red must lock the exact grammar, predicate vocabulary, effect
rejection, RNG preservation, and max-step diagnostic scenarios.

## Phase 1 Red record

- Added [`test_evolve_until_red.py`](../../tests/test_evolve_until_red.py).
- The Red contract uses the proposed bounded form
  `evolve psi under H until converged(psi) max 64`.
- It covers valid bounded syntax, missing/invalid bounds, and measurement
  inside the predicate as hard diagnostics.
- Runtime RNG preservation and max-step behavior remain represented by the
  semantic acceptance boundary and will be extended once the grammar slice is
  implemented.

## Phase 2 Green record

- Added contextual `until` / `max` tokens and AST fields for the bounded
  `evolve psi under H for t until predicate max N` form.
- Added positive-literal bound validation and hard diagnostics
  `EVOLVE_UNTIL_BOUND_ERROR` and `EVOLVE_UNTIL_EFFECT_ERROR`.
- Measurement expressions inside the predicate are rejected; no runtime
  repetition or QPU lowering is added in this slice.
- Verification: evolve-until tests, all standalone tests, and specification
  verification pass 165/165 (100%). Phase 3 review remains pending.

## Phase 3 review record

- Bound and effect validation is isolated in a dedicated type-checking helper;
  parser and diagnostic behavior remain unchanged.
- The implementation continues to enforce the pure Kernel boundary and does
  not imply runtime looping, RNG consumption, partial-state return, or QPU
  support.
- Reviewer empathy: the source grammar, validation contract, and deferred
  execution work are now distinguishable in both code and documentation.
- Status: **Phase 3 reviewed; grammar/type boundary complete**. Runtime
  repetition and max-step execution remain open follow-up work.

The remaining implementation slice must preserve the accepted backend
boundary above: Kernel compilation stays independent of QPU capability, while
QPU/OpenQASM emission reports the unsupported capability explicitly.

## Runtime follow-up record (LISS-0110 / Wave 1)

- Status: **Phase 3 reviewed; runtime slice complete** (2026-07-27).
- Joint evaluator repeats `evolve psi under H for t until converged(psi) max N`
  with pure predicates (`converged` / literal booleans).
- `converged(state)` is true when the named evolve seed has a single marginal
  support point (delta distribution on that coordinate).
- `EVOLVE_UNTIL_MAX_STEPS_ERROR` is raised via `KernelDiagnosticError` when
  `max` is exhausted; no partial-state return or Host fallback.
- QPU/OpenQASM emission remains `E_QPU_UNSUPPORTED_CAPABILITY`.
- Tests: `tests/test_evolve_until_runtime_red.py`, existing
  `tests/test_evolve_until_red.py`.
