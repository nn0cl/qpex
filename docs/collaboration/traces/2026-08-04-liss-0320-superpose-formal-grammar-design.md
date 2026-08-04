# LISS-0320 `superpose` formal grammar — design intake

## Current State

- Current phase: phase-0-design (pre-Phase-1; awaiting Plan approval).
- User request: continue Staqex WP-0092 work; pick a minimal, non-mixed
  scope (`superpose` grammar OR `controlled` grammar, not both) and follow
  Feature Path DESIGN CHECK → spec update → Phase 1 approval gate.
- Canonical issue: [LISS-0320](../../issues/LISS-0320-superpose-formal-grammar.md).
- Work plan: [WP-0092](../../work-plans/WP-0092-quantum-mental-model-follow-up.md).

## Included context

- AGENTS.md, `docs/architecture/agent-quickstart.md`,
  `docs/architecture/open-work-register.md`, ADR 0189, ADR 0190, WP-0092,
  `staqex-v1-quantum-mental-model-follow-up.md` §4.
- Current shipped code: `compiler/staqex/tokens.py` (ACTIVE/RETIRED tables),
  `parser.py` (`_when_expr`, `_parse_h1_experiment_body`), `ast_nodes.py`
  (`WhenExpr`/`WhenArm`, `H1Superposition`), `typecheck.py` (WhenExpr typing),
  `runtime/evaluator.py` (`_bind_when` and other `WhenExpr` dispatch sites).
- `tests/test_quantum_composition_surface_red.py` (PR #344, already green —
  tests only the shallow H1 heuristic, not the formal grammar this Issue
  targets).

## Omitted context

- `controlled` grammar (deliberately deferred to its own Issue).
- QASM/QPU target lowering internals.
- S02 domain-specific code (unrelated benchmark).
- Rust VM (future generation, same semantics, not started).

## Model / tool routing

- Design and spec authoring: this session (Claude Sonnet 5), no external AI
  call.
- Verification: deterministic — `pytest`, `tests/spec_verification/run_all.py`,
  `git diff --check`.

## Execution record — attempt 1 (design only)

- Re-verified `main` at `c4a9756` (PR #344 merged): `pytest tests/ -q` →
  `1205 passed`; `tests/spec_verification/run_all.py` → `161/161`; `git diff
  --check` clean.
- Read PR #344's diff directly (`ast_nodes.py`, `h1_authoring.py`,
  `parser.py`) to confirm the shipped `superpose` recognition is the shallow
  `_parse_h1_experiment_body` line-lexeme scanner, not a real grammar rule —
  this determined the Issue's actual remaining scope.
- Created branch `feature/liss-0320-superpose-formal-grammar` (not on
  `main`, per AGENTS.md).
- Added spec §4.5 (Gherkin acceptance scenarios for the formal-grammar
  slice) to `docs/specs/staqex-v1-quantum-mental-model-follow-up.md`.
- Filed `docs/issues/LISS-0320-superpose-formal-grammar.md`.
- No test or implementation code written yet — stopped for Plan approval per
  CLAUDE.md "Claude Code Issue-Level and Work-Plan Autonomy."

## Adjudicator decisions

- Pending: Plan approval for LISS-0320 (before Phase 1 Red).

## Assumptions

- `superpose` needs its own `TokenKind`, not a reuse of `TokenKind.WHEN`
  (unlike `mix`), so `SuperposeExpr` is structurally distinguishable from
  `WhenExpr` at parse time.
- The evaluator guard (fail-closed diagnostic on attempted evaluation) is a
  baseline safety inclusion in this slice, not the separately-scoped
  target-lowering/capability-rejection work item.

## Open decisions

- Exact diagnostic code name for the evaluator guard (proposed
  `COHERENT_EXECUTION_UNSUPPORTED`) — open for Adjudicator preference.
- Whether arm-pattern exhaustiveness rules should mirror `WhenExpr`'s
  `_check_when_enum_exhaustive` exactly or take a narrower first pass.

## Verification run (this attempt)

```text
.venv/bin/python3 -m pytest tests/ -q            → 1205 passed
.venv/bin/python3 tests/spec_verification/run_all.py → 161/161, 100%
git diff --check                                  → clean
```

## Changed files (this attempt)

- `docs/specs/staqex-v1-quantum-mental-model-follow-up.md` (new §4.5)
- `docs/issues/LISS-0320-superpose-formal-grammar.md` (new)
- `docs/collaboration/traces/2026-08-04-liss-0320-superpose-formal-grammar-design.md` (this file)
- `docs/work-plans/WP-0092-quantum-mental-model-follow-up.md` (reference update)

## Next safe action

Await Plan approval for LISS-0320. On approval, proceed directly to Phase 1
Red (failing acceptance tests only, per spec §4.5) without a further
per-phase check-in, per CLAUDE.md Issue-Level Autonomy — then report before
Phase 2.
