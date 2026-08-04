# LISS-0320: `superpose` formal grammar, AST, and type boundary

## Metadata

- Local issue ID: LISS-0320
- Status: **proposed** (2026-08-04) — awaiting Plan approval before Phase 1 Red
- Phase: phase-0-design
- Type: Feature Path (language surface — grammar/AST/typecheck)
- Priority: P1
- Initial planning size: `M`
- Current planning size: `M`
- Owner / agent: Claude Code
- Program: [WP-0092](../work-plans/WP-0092-quantum-mental-model-follow-up.md)
- Parent: [ADR 0189](../architecture/adr/0189-quantum-mental-model-and-observation-contract.md),
  [ADR 0190](../architecture/adr/0190-s02-selection-boundary-and-mix-control.md)
- Depends on: none (grammar addition only; does not require `controlled`)
- Blocks: coherent amplitude/phase execution semantics; `superpose`
  target/QASM lowering and capability rejection (both separately scoped,
  not this Issue)
- Related: LISS/PR for `controlled` formal grammar (not yet filed — deferred
  to its own Issue so this Issue's scope stays single-lane per Adjudicator
  instruction not to mix `superpose` and `controlled` grammar work)
- Branch: `feature/liss-0320-superpose-formal-grammar`
- GitHub Issue: none yet

## Intent

Give `superpose` a real, first-class place in the primary Staqex grammar/AST/
type-check path, distinct from:

- `mix` / `WhenExpr` (probabilistic mixture — must never be conflated).
- `H1Superposition` (the shallow, line-based lexeme-scan classifier added in
  PR #344's `Parser._parse_h1_experiment_body`, which only tags a source
  line for the H1 authoring/state-transform-plan diagnostic and performs no
  real parsing, typing, or evaluation).

Concretely: `superpose(control) { pat -> expr, ... }` parses to a new
`SuperposeExpr`/`SuperposeArm` AST node (structurally parallel to
`WhenExpr`/`WhenArm`), typechecks to `State<T>` from its arm bodies, and is
never silently accepted as `Mixture`/`mix`. Because a typed node must not
crash the evaluator, attempting to actually evaluate a program containing
`superpose` fails closed with one explicit, documented diagnostic (proposed
code: `COHERENT_EXECUTION_UNSUPPORTED`) rather than an unhandled-node
exception or a silent fallback to mixture semantics.

## Explicitly out of scope

- `controlled` grammar/type boundary (separate future Issue).
- Real coefficient/phase-preserving coherent execution math.
- QASM/QPU target-profile lowering and capability-rejection framework (the
  evaluator guard added here is a baseline safety minimum, not that system).
- Any change to the existing H1 authoring heuristic (`H1Superposition`,
  `_parse_h1_experiment_body`) — it is left as-is.
- Scientific lexicon work (separate WP-0092 work unit).

## Acceptance reference

[`staqex-v1-quantum-mental-model-follow-up.md` §4.5](../specs/staqex-v1-quantum-mental-model-follow-up.md)
("`superpose` formal-grammar acceptance scenarios (Phase 1 target,
LISS-0320)").

## AI planning record (size M)

- Status: proposed, pre-Phase-1
- Authoring environment: Claude Code (Sonnet 5), this session
- Date: 2026-08-04
- Size: `M` — touches `tokens.py`, `ast_nodes.py`, `parser.py`,
  `typecheck.py`, and `runtime/evaluator.py`, but the added surface is one
  new expression form structurally mirroring the existing, well-understood
  `WhenExpr`/`WhenArm` pattern; no new port, adapter, or persistence
  boundary. May reclassify to `L` if arm-pattern exhaustiveness or the
  evaluator guard placement surfaces unexpected interaction with existing
  `WhenExpr` code paths during Phase 1 Red.
- Route: direct implementation by this session (no external AI/model call
  planned beyond normal code generation).
- Estimate: N/A — no token/time budget tracked for this environment.
- Assumptions: `superpose` needs its own `TokenKind` (not reusing
  `TokenKind.WHEN`, unlike how `mix` reuses `WHEN` today) so `SuperposeExpr`
  and `WhenExpr` remain structurally distinguishable at parse time, not just
  by AST class.
- Confidence: medium-high on grammar/AST/typecheck; medium on the exact
  evaluator guard placement without first reading the full `WhenExpr`
  evaluation dispatch in `runtime/evaluator.py`.
- Revision links: none yet.

## Exit criteria

- [ ] Phase 1 Red: acceptance test(s) implementing spec §4.5's four
      scenarios exist and fail for the documented reason (no `SuperposeExpr`
      today; `superpose` lexes as a plain identifier).
- [ ] Phase 2 Green: minimal implementation makes those tests pass without
      editing the tests, without touching `controlled`, and without changing
      existing `mix`/`when` behavior (regression scenario passes unchanged).
- [ ] Phase 3 Refactor: no behavior change; reviewer empathy summary
      produced.
- [ ] Full regression: `pytest tests/ -q`, `python3
      tests/spec_verification/run_all.py` (161/161), `git diff --check`.
- [ ] WP-0092 and open-work-register synchronized with the outcome.

## Non-goals

- Making `superpose` executable with real physics.
- Deciding `controlled`'s grammar.
- Any QASM/backend lowering work.
