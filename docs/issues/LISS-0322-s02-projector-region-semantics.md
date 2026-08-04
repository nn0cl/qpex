# LISS-0322: `Projector<Selection>` region semantics (ADR 0192 Kernel slice)

## Metadata

- Local issue ID: LISS-0322
- Status/phase: **proposed** / `phase-0-design` (2026-08-05) — awaiting Plan approval before Phase 1 Red
- Type: Feature Path (Kernel — `compiler/staqex/pipeline.py` semantic-IR
  lowering; no grammar/parser change)
- Priority: P1
- Initial planning size: `M`
- Current planning size: `M`
- Owner / agent: Claude Code
- Program: [WP-0093](../work-plans/WP-0093-s02-language-expressiveness-and-selection.md)
  work unit C (Kernel slice)
- Parent: [ADR 0192](../architecture/adr/0192-s02-projector-selection-semantics.md)
  (Accepted 2026-08-05)
- Depends on: [ADR 0192](../architecture/adr/0192-s02-projector-selection-semantics.md)
  (Accepted — this Issue implements its Decisions 1–2 only)
- Blocks: work unit C's Host-side `ConstraintDisposition`/`objective_profile`
  slice (ADR 0192 Follow-up item 2, likely folded into work unit E); work
  unit D (observation/result contract)
- Related: [LISS-0321](LISS-0321-s02-host-domain-and-finite-boundary.md)
  (Host-side domain records this Issue's constraint names conceptually
  align with, though this Issue does not import from it)
- Branch: `feature/liss-0322-s02-projector-region-semantics`
- GitHub Issue / PR: none yet

## Intent

Implement ADR 0192 Decisions 1–2 in
`compiler/staqex/pipeline.py::_append_selection_projector_region`:

1. **Structured, source-derived `constraint_ref`** (Decision 1): replace the
   hardcoded `constraint_ref="S02.feasible"` literal with a value derived
   from the actual `project X onto feasible(...)` call site's recognized
   predicate names, so two programs with different constraints produce
   distinguishable `ProjectorRegion`s, and a program with no `project ...
   onto ...` produces no `ProjectorRegion` at all (tightening today's
   whole-body `has_projector` scan, which does not inspect the target).
2. **Fixed, closed predicate vocabulary** (Decision 2): only
   `exactly_selected`, `pairwise_compatible`, and `diversity_at_least` are
   recognized. Any other name inside `feasible(...)` — or a `project ...
   onto` target that is not a call to `feasible` at all — fails with a new
   `S02_UNKNOWN_CONSTRAINT_PREDICATE` diagnostic (added to `HARD_CODES`)
   instead of being silently accepted into a generic region.

## Scope clarification found during design intake

ADR 0192's Decision 2 table describes the predicates as if they were called
directly (`exactly_selected(n)`, `diversity_at_least(k)`), matching the S02
design draft's §10.3 aspirational sketch. The actual shipped syntax, used by
the existing regression test
(`tests/test_s02_selection_surface_red.py::test_projector_is_explicitly_lowered_from_selection_constraints`),
passes them as **keyword arguments to `feasible(...)`**:
`feasible(exactly_selected = 2, pairwise_compatible = true)`. This Issue
implements the kwarg-name form to stay regression-safe and match what
already ships; the ADR's substance (fixed three-name vocabulary, capability
rejection for anything else, structured `constraint_ref`) is unaffected by
this calling-convention detail. Treated as an implementation clarification,
not a scope change requiring ADR amendment — flagged here for visibility.

## Explicitly out of scope

- Changing `ProjectorRegion`'s dataclass shape (`constraint_ref` stays
  `str`; this Issue makes its *value* meaningful, not its type).
- `ConstraintDisposition` / `objective_profile` / `BenchmarkResult` (ADR
  0192 Follow-up item 2 — Host-side, separate Issue).
- Any change to `prepare_selection` (still a `unitarity_check.py` whitelist
  name only) or to what `feasible`/`project` mean outside this one
  region-construction function.
- Real Projector *execution* semantics (actual quantum projection math) —
  the Static Kernel does not execute S02 programs end-to-end yet; this
  Issue is IR-lowering only, same boundary as the existing shipped test.
- `controlled`'s formal grammar, `superpose` execution, or any WP-0092 work.

## Acceptance reference

[S02 acceptance specification § "Acceptance scenarios — `Projector<Selection>`
semantics (ADR 0192, Phase 1 target, LISS-0322)"](../specs/staqex-v1-s02-drug-discovery-benchmark.md),
four scenarios: recognized predicates produce a source-derived
`constraint_ref`; different predicate sets produce different `constraint_ref`
values; an unrecognized predicate fails closed; a penalty-only program (no
`project ... onto`) produces no `ProjectorRegion`.

## AI planning record (size M)

- Status: proposed, pre-Phase-1
- Authoring environment: Claude Code (Sonnet 5), this session
- Date: 2026-08-05
- Size: `M` — one function in one file
  (`_append_selection_projector_region`) plus one new diagnostic code
  added to `HARD_CODES`; no new AST/type/grammar surface. Bounded by the
  existing regression test's exact call shape, which reduces uncertainty
  versus LISS-0320/0321.
- Route: direct implementation by this session (no external AI/model call
  planned).
- Estimate: N/A — no token/time budget tracked for this environment.
- Assumptions: `constraint_ref`'s new value only needs to be *distinct and
  inspectable* per source predicate set (per the spec scenarios), not a
  fully structured object — a deterministic string built from the sorted
  recognized predicate names satisfies this with the smallest change.
- Confidence: high — the exact AST shape (`Call(callee=Var("project"),
  args=[source, target])`, `target` itself a `Call` with `.kwargs`) was
  confirmed by direct source reading in `parser.py` before drafting this
  Issue.
- Revision links: none yet.

## Exit criteria

- [ ] Phase 1 Red: acceptance tests for the four spec scenarios exist and
      fail for a documented reason (today's stub ignores predicate content
      and never rejects an unknown name).
- [ ] Phase 2 Green: minimal implementation makes those tests pass without
      editing tests, without touching `ProjectorRegion`'s dataclass shape,
      and without changing the existing
      `test_projector_is_explicitly_lowered_from_selection_constraints`
      regression test's behavior (still passes unchanged).
- [ ] Phase 3 Refactor: no behavior change; reviewer empathy summary.
- [ ] Full regression: `pytest tests/ -q`, `python3
      tests/spec_verification/run_all.py`, `git diff --check`.
- [ ] WP-0093 work unit C's Kernel-slice row and open-work-register
      synchronized with the outcome.

## Non-goals

- Real coherent Projector execution math.
- `ConstraintDisposition`/`BenchmarkResult` (separate Host-side Issue).
- Extending the predicate vocabulary beyond the fixed three names.
