# LISS-0328: real `project ... onto feasible(...)` Projector execution (ADR 0194, Follow-up item 2)

## Metadata

- Local issue ID: LISS-0328
- Status/phase: **proposed** / `phase-0-design` (2026-08-05) — design
  intake only, awaiting Plan approval.
  [LISS-0327](LISS-0327-host-input-port-foundation.md) is now **complete**
  (PR #366 merged), so this Issue's dependency is satisfied
- Type: Feature Path (Kernel — `compiler/staqex/runtime/evaluator.py`'s
  `project` op dispatch; no grammar/parser/AST change; no change to
  LISS-0322's IR-lowering layer)
- Priority: P2
- Initial planning size: `M`
- Owner / agent: Claude Code
- Program: [ADR 0194](../architecture/adr/0194-host-input-port-and-selection-predicate-semantics.md)
  Follow-up item 2; [WP-0093](../work-plans/WP-0093-s02-language-expressiveness-and-selection.md)
  work unit E
- Depends on: [LISS-0327](LISS-0327-host-input-port-foundation.md) (the
  `HostInputPort`/`host_input_binding.py` this Issue's `pairwise_compatible`/
  `diversity_at_least` handling calls); [LISS-0324](LISS-0324-s02-prepare-selection.md)
  (`prepare_selection`, the only known way to produce a selection-pattern
  Joint coordinate this Issue's `project` handling operates on)
- Blocks: none currently known
- Branch: `feature/liss-0328-selection-projector-predicate-execution`
  (not created yet)
- GitHub Issue / PR: none yet

## Intent

Implement ADR 0194 Decisions 3–5: replace `project`'s current
unconditional crash on a `feasible(...)` target
(`compiler/staqex/runtime/evaluator.py:3797`, `_eval_value` raising `call
cannot be classical value in Phase 2.2 value context`) with real execution
for all three ADR 0192 predicates:

1. **`exactly_selected(n)`**: `sum(pattern) == n` — a pure function of the
   pattern itself, no Host input needed.
2. **`pairwise_compatible = true`**: look up
   `self.host_input.get("pairwise_compatible")` (via LISS-0327's port);
   validate as an `n×n` symmetric `Bool` matrix via
   `host_input_binding.validate_matrix_binding(..., dtype=bool)`; satisfied
   iff every pair of selected slots `i < j` has `M[i][j] is True`.
3. **`diversity_at_least = k`**: look up
   `self.host_input.get("diversity_at_least")`; validate as an `n×n`
   symmetric non-negative `Float` matrix; satisfied iff the **minimum**
   `M[i][j]` over every pair of selected slots is `>= k`.

All predicates present in one `feasible(...)` call combine with logical
AND into one predicate function, applied via the existing
`joint.project_coord(name, predicate)` — the same Hilbert-projector-plus-
renormalize mechanism `project(psi, k)` already uses (line ~3827). `n` (the
pattern width) is read from the actual bound pattern's tuple length at
runtime, not tracked separately.

## Explicitly out of scope

- Any change to `_append_selection_projector_region`'s IR-lowering
  (LISS-0322) — that layer already produces a correct `ProjectorRegion`
  witness; this Issue only makes the *runtime* execution real.
- Any change to `feasible(...)`'s compile-time predicate-name recognition
  or `S02_UNKNOWN_CONSTRAINT_PREDICATE` (unchanged, LISS-0322's scope).
- Any change to `prepare_selection` (LISS-0324, already real).
- A general symbolic/predicate-lambda `project` form — the existing
  `PREDICATE_PROJECTOR_ERROR` guard against a literal `Lambda` target stays
  exactly as-is; this Issue only special-cases the closed-vocabulary
  `feasible(...)` `Call` form, matching how `KetLit` targets are already
  special-cased in the same dispatch.
- Live QPU execution or any target-adapter concern.

## Acceptance reference

New Phase 1 scenarios (extends the existing shipped
[S02 spec's Projector scenarios](../specs/staqex-v1-s02-drug-discovery-benchmark.md#acceptance-scenarios--projectorselection-semantics-adr-0192-phase-1-target-liss-0322),
which are IR-lowering-only today):

```gherkin
Feature: real Projector execution for feasible(...) predicates

  Scenario: exactly_selected filters to only matching patterns
    Given prepare_selection(3) projected onto feasible(exactly_selected = 2)
    When the state reaches terminal measure
    Then the result always has exactly 2 of 3 slots selected

  Scenario: pairwise_compatible rejects an incompatible pair
    Given prepare_selection(3), a bound pairwise_compatible matrix marking
      slots 0 and 1 incompatible, and feasible(exactly_selected = 2,
      pairwise_compatible = true)
    When the state reaches terminal measure
    Then the result never selects both slot 0 and slot 1 together

  Scenario: diversity_at_least rejects a below-threshold pair
    Given prepare_selection(3), a bound diversity_at_least matrix, and
      feasible(exactly_selected = 2, diversity_at_least = k)
    When the state reaches terminal measure
    Then the result's selected pair's diversity is always >= k

  Scenario: a missing required Host input fails closed at runtime
    Given feasible(pairwise_compatible = true) with no bound
      "pairwise_compatible" host input
    When the program runs
    Then it fails with HOST_INPUT_BINDING_MISSING, not a fabricated result

  Scenario: an infeasible constraint set produces vacuum, not a silent pass
    Given constraints that no pattern can satisfy
    When the state reaches terminal measure
    Then the terminal measurement is vacuum/empty, matching the existing
      empty-projector contract project(psi, k) already has
```

## AI planning record (size M)

- Status: proposed, pre-Phase-1
- Authoring environment: Claude Code (Sonnet 5), this session
- Date: 2026-08-05
- Size: `M` — one new `target`-handling branch in the existing `project`
  dispatch (mirrors the existing `KetLit` special-case exactly), plus
  predicate-combination logic and Host-input lookups via LISS-0327's port.
  No new AST, no new Joint method (`project_coord` already supports an
  arbitrary label predicate — confirmed by the existing `KetLit` case's own
  use of it).
- Route: direct implementation by this session.
- Assumptions: `feasible(...)`'s `target` AST shape (a `Call` with
  `.kwargs: list[tuple[str, Expr]]`) matches what LISS-0322 already reads
  in `_append_selection_projector_region` — confirmed by that Issue's own
  documented AST-shape verification, not re-verified independently in this
  design intake (re-verification planned before Phase 1 Red).
- Confidence: medium — the Hilbert-projector mechanism and Host-input
  lookup are both individually verified/shipped; their combination
  (reading `feasible(...)`'s kwargs at the runtime layer, which currently
  never inspects them at all) has not yet been directly probed and may
  surface a smaller implementation-detail surprise during Red, per this
  session's established pattern.
- Revision links: none yet.

## Exit criteria

- [ ] Phase 1 Red: acceptance tests for the five scenarios above exist and
      fail for a documented reason.
- [ ] Phase 2 Green: minimal implementation makes those tests pass without
      editing them, without touching LISS-0322's IR-lowering layer, and
      without changing `test_s02_selection_surface_red.py`'s existing
      compile-only structural test.
- [ ] Phase 3 Refactor: no behavior change; reviewer empathy summary.
- [ ] Full regression: `pytest tests/ -q`, `python3
      tests/spec_verification/run_all.py`, `git diff --check`.
- [ ] ADR 0194's Follow-up item 2 checked off; WP-0093 work unit E updated.

## Non-goals

- `HostInputPort` foundation itself (LISS-0327).
- Symbolic/general predicate `project`.
- Live QPU execution.
