# LISS-0321: S02 Host domain records and finite boundary (WP-0093 work unit B)

## Metadata

- Local issue ID: LISS-0321
- Status/phase: **in_progress** / `phase-1-red` (2026-08-04) — Adjudicator
  granted Investigation approval and Plan approval. Decisions: (1) domain
  module lives under `examples/showcase/S02_drug_discovery/domain/` and
  `.../host/`, mirroring S01's layout; (2) greedy/exact classical baselines
  stay out of this Issue, deferred to work unit E; (3) work unit C's
  `Projector<Selection>` ADR is filed separately, right after this Issue
  closes, not in parallel.
- Type: Feature Path (Host-side domain records + boundary validation; no Kernel
  grammar/typecheck/evaluator change)
- Priority: P1
- Initial planning size: `L`
- Current planning size: `L`
- Owner / agent: Claude Code
- Program: [WP-0093](../work-plans/WP-0093-s02-language-expressiveness-and-selection.md)
  work unit B; related [WP-0092](../work-plans/WP-0092-quantum-mental-model-follow-up.md)
- Parent: [ADR 0190](../architecture/adr/0190-s02-selection-boundary-and-mix-control.md)
  (Accepted); [S02 acceptance specification](../specs/staqex-v1-s02-drug-discovery-benchmark.md)
  (Accepted)
- Depends on: none. This Issue is deliberately scoped to be Host-side only
  (Python DTOs + Host input hygiene), so it does not need the
  `Projector<Selection>` semantics ADR that work unit C still requires.
- Blocks: work unit C (constraint/objective/Projector semantics — needs its
  own ADR, not started), work unit D (observation/result contract), work
  unit E (conformance scenarios 3, 8, 9 below — reproducibility and
  capability rejection need the fixture this Issue produces)
- Related: [LISS-0320](LISS-0320-superpose-formal-grammar.md) (unrelated
  language-surface slice, same session)
- Branch: `feature/liss-0321-s02-host-domain-and-finite-boundary` (renamed
  from the investigation branch; investigation commit `b8bd2de` is first)
- GitHub Issue / PR: none yet

## Intent

Implement the classical (Host-side) half of the S02 benchmark shape defined
in the already-**Accepted** [S02 acceptance specification](../specs/staqex-v1-s02-drug-discovery-benchmark.md#value-model)
§"Value model" / §"Fixture limits", without touching the Kernel language
surface (no new grammar, no new typecheck rule, no evaluator change). This
covers WP-0093 work unit B items 1–4:

1. `CandidateId`, `Candidate`, `TargetProfile`, `Constraint`, `Score`, and
   `SelectionProblem` as Host-side Python domain records (dataclasses),
   matching the spec's "Value model" §"Classical records" exactly — stable
   `CandidateId`, descriptor reference, score components, tags, provenance
   for `Candidate`; named rule + domain for `Constraint`; normalized finite
   component + direction + weight + provenance for `Score`; ordered
   candidates + target profile + hard constraints + soft objective terms +
   selection size + seed + encoding profile + resource profile for
   `SelectionProblem`.
2. An explicit finiteization witness for the 8–16 candidate / 2–4 selection
   synthetic fixture (spec §"Fixture limits"). The Kernel's existing
   `finiteize(lo, hi, bins, samples, seed)` op (already shipped, ADR 0185 /
   LISS-0313) is a **general numeric finiteization primitive**, not a
   candidate-manifest witness — this Issue defines the Host-side witness
   that proves a `SelectionProblem`'s candidate set is finite, bounded, and
   ID-unique *before* it reaches the Kernel boundary. It does not reuse or
   modify `finiteize`.
3. Separate Host input hygiene (malformed/duplicate/missing/out-of-domain
   record rejection — ADR 0190 item 5) from quantum selection constraints
   (which stay in the Kernel boundary per work unit C, not this Issue).
4. Reject missing, duplicate, non-finite, oversized, or unproven finite
   input with explicit, distinct failure reasons (not a single generic
   error).

## Scope note: what already exists vs. what this Issue adds

`tests/test_s02_selection_surface_red.py` (already green, part of PR #337)
demonstrates that the **generic** language building blocks tolerate
S02-shaped names — `finiteize(...)`, `prepare_selection(candidates)`,
`project ... onto feasible(...)` — but verified by direct source inspection
that:

- `prepare_selection` is only a name registered in
  `unitarity_check.py`'s `_QUANTUM_OPS` whitelist (marks a call as
  "quantum-lineage", nothing else) — there is no actual selection-state
  preparation implementation.
- `feasible(...)` is not a registered stdlib function anywhere — the
  `project X onto feasible(...)` test passes because the **general**
  `project ... onto <call-expr>` syntax already produces a `ProjectorRegion`
  regardless of what the callee means, not because S02 constraint semantics
  are implemented.
- No `Selection<CandidateId>` type, `Candidate`/`Constraint`/`Score`/
  `SelectionProblem` record, or finite-manifest witness exists anywhere in
  `compiler/staqex/` or `examples/showcase/`.

So the existing green test confirms the *generic* syntax doesn't misfire on
S02-shaped names; it is not evidence that S02's domain model is implemented.
This Issue adds the actual domain model. It does not change or duplicate
`tests/test_s02_selection_surface_red.py`.

## Explicitly out of scope

- `Projector<Selection>` semantics, constraint lowering, objective
  normalization (WP-0093 work unit C) — needs its own ADR per WP-0093's own
  deliverable list; not started, not this Issue.
- `State<Selection<CandidateId>>` Kernel-side carrier, `expect` usage,
  resource/provenance metadata at the Host boundary (work unit D).
- Reproducibility and capability-rejection conformance scenarios (work unit
  E) — depend on this Issue's fixture plus work unit C's Projector, so they
  come after both.
- Classical baselines (greedy / exact small-instance) — WP-0093 requires
  them before quality claims, but they are not required to prove the finite
  boundary itself; deferred to work unit E unless Phase 1 Red review says
  otherwise.
- Any `.sqx`, grammar, typecheck, or evaluator change.
- Real compound data, chemistry graph semantics, or public datasets (spec
  §"Out of scope").

## Acceptance reference

[S02 acceptance specification](../specs/staqex-v1-s02-drug-discovery-benchmark.md#acceptance-scenarios),
scenarios:

- "candidate data stays classical"
- "finite encoding is explicit"

(Scenarios "hard constraints use a projector boundary", "only terminal
measure crosses the classical boundary", "same execution identity
reproduces the result", and "unsupported width fails before execution" stay
with work units C/D/E.)

## AI planning record (size L)

- Status: proposed, pre-Phase-1
- Authoring environment: Claude Code (Sonnet 5), this session
- Date: 2026-08-04
- Size: `L` — multiple new Host-side modules (domain records, finite-witness
  validation, fixture generation) plus their own test suite; no Kernel
  change, but meaningful new surface area and the first real S02
  implementation code, which carries more uncertainty than a single-module
  change.
- Route: direct implementation by this session (no external AI/model call
  planned).
- Estimate: N/A — no token/time budget tracked for this environment.
- Assumptions: this Issue produces Host-side Python only (likely under
  `examples/showcase/S02_.../domain/` and `.../host/`, mirroring S01's
  `domain/`/`host/` layout) plus its own pytest suite; it does not require a
  `.sqx` example file to exist yet, since no Kernel-side selection state is
  being prepared in this slice.
- Confidence: medium — the Host-side record shapes are well-specified in the
  accepted spec, but exact fixture generation (8–16 candidates, deterministic
  seed policy) and the precise set of fail-closed diagnostic codes are not
  yet decided and may need Phase 1 Red iteration.
- Revision links: none yet.

## Exit criteria

- [ ] Phase 1 Red: acceptance tests for "candidate data stays classical" and
      "finite encoding is explicit" (and their fail-closed sub-cases: missing,
      duplicate, non-finite, oversized, unproven-finite input) exist and fail
      for a documented reason (no domain records/witness exist yet).
- [ ] Phase 2 Green: minimal Host-side implementation makes those tests pass.
- [ ] Phase 3 Refactor: no behavior change; reviewer empathy summary.
- [ ] Full regression: `pytest tests/ -q`, `python3
      tests/spec_verification/run_all.py`, `git diff --check`.
- [ ] WP-0093 work unit B marked with implementation evidence; WP-0093
      status field updated if work unit B completion changes it.

## Non-goals

- Projector/constraint semantics (work unit C).
- Kernel-side `State<Selection<CandidateId>>` preparation.
- Classical baselines or resource/provenance reporting.
- Any claim that S02's quantum lane is implemented.
