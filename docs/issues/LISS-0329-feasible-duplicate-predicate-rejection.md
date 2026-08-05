# LISS-0329: reject duplicate predicate names in `feasible(...)`

## Metadata

- Local issue ID: LISS-0329
- Status/phase: **proposed** / `phase-0-design` (2026-08-05) — awaiting
  Plan approval before Phase 1 Red
- Type: Feature Path (Kernel — `compiler/staqex/pipeline.py`'s
  `_collect_feasible_predicates`; no grammar/parser/AST change, no runtime
  change)
- Priority: P2
- Initial planning size: `S`
- Owner / agent: Claude Code
- Program: [WP-0093](../work-plans/WP-0093-s02-language-expressiveness-and-selection.md)
  work unit C/E; found as an open reviewer-empathy question in
  [LISS-0328](LISS-0328-selection-projector-predicate-execution.md)'s
  Completion review
- Depends on: [LISS-0322](LISS-0322-s02-projector-region-semantics.md)
  (`_collect_feasible_predicates`, the function this Issue extends);
  [LISS-0328](LISS-0328-selection-projector-predicate-execution.md)
  (confirmed the concrete silent-misbehavior evidence below)
- Branch: `feature/liss-0329-feasible-duplicate-predicate-rejection`
- GitHub Issue / PR: none yet

## Intent

`feasible(exactly_selected = 2, exactly_selected = 3)` — the same
predicate name repeated with different values — currently compiles clean
and, at runtime, silently resolves to whichever value appears **last**
(`_bind_feasible_predicate` iterates `target.kwargs` and overwrites its
local variable on each match). Verified live:

```python
# compile_source(...).ok == True, only soft QSEM_* diagnostics
# run_source(...) -> status "succeeded", measured pattern (1, 1, 1)
#   (sum == 3, satisfying only the *second*, later `exactly_selected = 3`
#   -- the first `exactly_selected = 2` is silently discarded)
```

This is a fail-closed gap: a source-level contradiction (the same named
constraint asserted twice, with different values) should be rejected
explicitly, not silently resolved by argument order. Fix at the compile-time
layer, `_collect_feasible_predicates`
(`compiler/staqex/pipeline.py:400`), which already walks `target.kwargs`
to validate each name against ADR 0192's closed vocabulary — extend it to
also detect a name appearing more than once, and add a new
`S02_DUPLICATE_CONSTRAINT_PREDICATE` diagnostic (distinct from
`S02_UNKNOWN_CONSTRAINT_PREDICATE`, since a duplicate name is individually
recognized, just repeated).

## Explicitly out of scope

- Any runtime (`evaluator.py`) change. Fixing this at compile time means an
  offending program never reaches `_bind_feasible_predicate` at all —
  consistent with the project's existing pattern of validating malformed
  `feasible(...)` targets once, at the compile-time gate (see
  `S02_UNKNOWN_CONSTRAINT_PREDICATE`'s existing precedent in the same
  function).
- Any change to `_bind_feasible_predicate`'s "last value wins" internals —
  moot once duplicates are rejected before runtime.
- Any change to `exactly_selected`/`pairwise_compatible`/`diversity_at_least`'s
  individual semantics (LISS-0328, unaffected).

## Acceptance reference

New Phase 1 scenarios (no existing spec section covers duplicate-predicate
rejection yet — this Issue's own Red test is the acceptance evidence):

```gherkin
Feature: feasible(...) rejects duplicate predicate names

  Scenario: a repeated predicate name fails closed at compile time
    Given feasible(exactly_selected = 2, exactly_selected = 3)
    When the program is compiled
    Then compilation fails with S02_DUPLICATE_CONSTRAINT_PREDICATE
    And the program never reaches runtime

  Scenario: distinct predicate names are unaffected
    Given feasible(exactly_selected = 2, pairwise_compatible = true)
    When the program is compiled
    Then no S02_DUPLICATE_CONSTRAINT_PREDICATE diagnostic is produced
```

## AI planning record (size S)

- Status: proposed, pre-Phase-1
- Authoring environment: Claude Code (Sonnet 5), this session
- Date: 2026-08-05
- Size: `S` — one function, one file, one new diagnostic code; no new
  AST/grammar surface (`target.kwargs` already carries every occurrence in
  source order).
- Route: direct implementation by this session.
- Confidence: high — the exact silent-misbehavior evidence (compiles
  clean, runs to `(1, 1, 1)`) was reproduced live before drafting this
  Issue.

## Exit criteria

- [ ] Phase 1 Red: acceptance test for both scenarios above exists and
      fails for a documented reason (duplicate names currently compile
      clean).
- [ ] Phase 2 Green: minimal implementation makes those tests pass without
      editing them, without touching `evaluator.py`, and without changing
      `test_s02_selection_surface_red.py`/LISS-0322/LISS-0328's existing
      tests' behavior.
- [ ] Phase 3 Refactor: no behavior change; reviewer empathy summary.
- [ ] Full regression: `pytest tests/ -q`, `python3
      tests/spec_verification/run_all.py`, `git diff --check`.
- [ ] WP-0093 work unit C's row and the diagnostic catalog updated with
      the new code.

## Non-goals

- Runtime changes.
- New predicate names or semantics.
