# LISS-0049: QASM function-call lowering boundary

## Metadata

- Local issue ID: LISS-0049
- GitHub issue: none
- Status: proposed
- Phase: phase-0-design
- Type: language architecture / backend boundary
- Priority: P2
- Initial planning size: L
- Current planning size: L
- Reclassification reason: n/a — new issue, split from LISS-0021's Impact
  Inventory ("QASM lowering" row) and Adjudicator Decision Points ("Define
  the QASM boundary for function calls whose bodies can be lowered").
- Owner/agent: TBD
- Related branch: none yet

## Summary

LISS-0021 shipped explicit function signatures and typed returns for the CPU
Kernel (SV evaluator). It deliberately left one question open: when `main`
calls a measure-free `fn`, what happens when that program is lowered to
OpenQASM 3 instead of run on the state-vector evaluator? This issue is the
split-out home for that decision. No implementation is authorized by this
issue; it is Architecture Path design intake only.

## Problem statement (confirmed by direct probe, 2026-07-25)

`compiler/qpex/backend/qasm/lower.py:_from_ast_patterns` only reads
`unit.main.body.stmts` (line 48). It pattern-matches a fixed set of AST
shapes directly inside `main` (`StateBind`, `Measure`, Trotter/`evolve`
forms, etc.) and otherwise falls through to a generic DAG-driven lowering
or, failing that, an "empty program fallback" (`lower.py:264-267`: a single
`h` gate plus a fallback measure).

A user-defined function's body (its own `StateBind`/`return` statements) is
never inspected during QASM lowering — only `main`'s own statements are
walked. Concretely:

```qpex
fn origin() -> State<Int> {
    return dirac(0)
}
pub fn main() -> Unit {
    State<Int> result = origin()
    measure result
}
```

`python3 -m compiler.qpex emit-qasm` on this program emits exactly the same
output as an empty `main` — `h q[0]; measure` — silently discarding the
`origin()` call's actual meaning. There is no diagnostic; the mismatch
between what CPU `run` computes and what `emit-qasm` lowers is currently
invisible to the user.

This is worse than "QASM support is limited" (which is already the accepted
posture for other features, e.g. higher-order Suzuki S4). It is currently
**silent** — a physicist could reasonably run a program with `run` (correct,
uses the function), then lower the same program with `emit-qasm` (silently
wrong, ignores the function), with no warning.

## Proposed acceptance scope (options for Adjudicator decision — none selected)

This issue does not select an option. It records the three candidates
identified during the LISS-0021 review for Architecture Path review:

- [ ] **Option A — Inline at lowering time.** Before pattern-matching,
      substitute each measure-free function call in `main` with its body
      (simple case: no recursion, no branching beyond what `main` already
      supports). Smallest user-visible surprise; requires call-graph
      inlining logic in the QASM backend that does not exist today.
- [ ] **Option B — Explicit CPU-only rejection.** `emit-qasm` detects a call
      to a user-defined function inside `main` and rejects the program with
      a new diagnostic (e.g. `QASM_FUNCTION_CALL_UNSUPPORTED`) rather than
      silently falling back to the empty-program sketch. Smallest
      implementation; turns a silent correctness gap into an honest,
      explicit boundary consistent with the project's "no hidden
      discretization / no hidden collapse" posture elsewhere (ADR 0074,
      ADR 0075).
- [ ] **Option C — Defer, but make the fallback honest.** Keep today's
      CPU-only behavior, but stop silently falling back to a fixed
      empty-program sketch — instead reject with a diagnostic (this is a
      minimal subset of Option B) or explicitly document the fallback's
      current shape as intentional and add a regression test pinning it.

## Impact inventory

| Area | Current behavior | Required decision/change |
|---|---|---|
| QASM lowering (`backend/qasm/lower.py`) | Only walks `main.body.stmts`; ignores called function bodies; falls back silently | Select Option A, B, or C above |
| Diagnostics | No diagnostic exists for a function call inside a QASM-targeted `main` | Define diagnostic code and message if Option B/C chosen |
| Tests | No test pins today's silent-fallback behavior | Add a regression test for whichever option is accepted |
| Documentation | `docs/architecture/qpex-language-spec.md` / normative spec do not mention this boundary | Document the accepted QASM/function boundary once decided |

## Non-goals

- No change to the CPU/SV evaluator's function semantics (LISS-0021's
  shipped behavior is out of scope here and unaffected).
- No general call-graph inlining framework beyond what the accepted option
  requires.
- No QPU provider submission, credentials, or network changes.
- No revisiting of `return`/lexical-scope semantics (ADR 0068, Accepted).

## Dependencies

- Parent: split from [LISS-0021](LISS-0021-function-signatures-and-returns.md)
  (Complete)
- Depends on: ADR 0036 (QASM lowering baseline), ADR 0059 (zero-dependency
  codegen), the accepted function-signature model (ADR 0064/0068)
- Related: LISS-0002 (OpenQASM3 codegen backend), LISS-0008 (Trotter → QASM),
  LISS-0041 (QPU IR lowering), LISS-0048 (unrelated sibling split from
  LISS-0021 — a typecheck bug, not a design question)
- Blocks: nothing known; QASM emission for function-call programs simply
  remains silently incomplete until this is decided

## Adjudicator Decision Points

- [ ] Select Option A, B, or C above (or a different option not yet
      identified).
- [ ] If Option A: approve the call-graph/inlining boundary (recursion
      rejection, argument substitution rules, effect on existing Trotter/
      pattern-match paths).
- [ ] If Option B or C: approve the new diagnostic code and message text.
- [ ] Approve Architecture Path design before any Phase 1 Red tests.

## Context

- Included: `compiler/qpex/backend/qasm/lower.py`, `compiler/qpex/codegen/openqasm.py`,
  `compiler/qpex/backend/qasm/emitter.py`, existing QASM regression tests,
  `docs/architecture/qpex-language-spec.md` QASM section.
- Omitted: CPU/SV evaluator internals (already settled by LISS-0021), QPU
  provider adapters, unrelated LISS-0021 scope.
- Assumption: whichever option is chosen must not weaken the "no hidden
  discretization / no hidden collapse" posture already accepted elsewhere in
  the project (ADR 0074, ADR 0075) — a silent semantic gap is itself a
  violation of that spirit even though it is a QASM-only degradation, not a
  collapse.
- Ambiguity boundary: Option selection (A/B/C) is entirely an Adjudicator
  decision; no option is favored by this issue.

## AI Planning Records

### AIP-0049-001

- Status: proposed
- Created at: 2026-07-25
- Planning size: L
- Intended execution route: Architecture Path design/option selection, then
  Feature Path Phase 1 Red → Phase 2 Green → Phase 3 Refactor once an option
  is chosen.
- Intended scope: QASM backend lowering decision and (if Option A) inlining
  implementation; diagnostic definition (if Option B/C); regression tests;
  documentation.
- Estimated token range: N/A
- Estimated token midpoint: N/A
- Token metric: N/A
- Estimation basis: backend-only change with no CPU evaluator/typechecker
  impact; complexity depends entirely on which option is selected (B/C are
  small; A is larger).
- Assumptions: no external dependency; QASM backend remains zero-dependency
  per ADR 0059.
- Confidence: low on planning size until an option is selected; Option
  B/C would likely be `S`/`M`, Option A likely `L`.
- Revises: none
- Revision reason: n/a
- Superseded by: none

## Verification

- Architecture review and option selection first; no Phase 1 Red before
  that.
- Once selected: a regression test on the reproduction program above must
  demonstrate the accepted behavior (inlined gates, or an explicit
  diagnostic — never a silent empty-program fallback).
- Existing QASM/SV/example regressions must remain green.

## Work Notes

- 2026-07-25: Issue opened from LISS-0021 Architecture Path re-scope review.
  Root cause read (`lower.py:48,264-267`) and reproduction confirmed via
  `emit-qasm` probe. No option selected; no code changed.
