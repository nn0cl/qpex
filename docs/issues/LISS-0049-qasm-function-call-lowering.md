# LISS-0049: QASM function-call lowering boundary

## Metadata

- Local issue ID: LISS-0049
- GitHub issue: none
- Status: Architecture Path decision recorded (Option B); Feature Path Phase 1
  Red not yet approved
- Phase: phase-0-design → option selected 2026-07-25; diagnostic code/message
  text and Phase 1 Red still need explicit Adjudicator phase approval
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

## Proposed acceptance scope

**Decided 2026-07-25 (Architecture Path): Option B — Explicit CPU-only
rejection.** See Adjudicator Decision Points and Work Notes below. Option A
is not rejected outright; it is split out as a possible future follow-up
(see Dependencies) if precise QASM output for function-call programs later
becomes required, since Option B only makes the gap honest — it does not
make `emit-qasm` produce a correct circuit for these programs.

The three candidates considered:

- [x] **Option B — Explicit CPU-only rejection (selected).** `emit-qasm`
      detects a call to a user-defined function inside `main` and rejects
      the program with a new diagnostic (`QASM_FUNCTION_CALL_UNSUPPORTED`)
      rather than silently falling back to the empty-program sketch.
      Smallest implementation; turns a silent correctness gap into an
      honest, explicit boundary consistent with the project's "no hidden
      discretization / no hidden collapse" posture elsewhere (ADR 0074,
      ADR 0075). Selected because it is the fastest path to eliminating the
      silent-misrepresentation failure mode the Adjudicator flagged as the
      controlling constraint (see Work Notes).
- [ ] **Option A — Inline at lowering time (deferred, not selected).**
      Before pattern-matching, substitute each measure-free function call in
      `main` with its body (simple case: no recursion, no branching beyond
      what `main` already supports). Smallest user-visible surprise once
      built; requires call-graph inlining logic in the QASM backend that
      does not exist today. Deferred rather than rejected — may be revisited
      as a follow-up issue if correct QASM output (not just an honest
      rejection) for function-call programs becomes a requirement.
- [ ] **Option C — Defer, but make the fallback honest (not selected as a
      separate path).** Its diagnostic-reject sub-choice is subsumed by
      Option B above; its "document the fallback as intentional" sub-choice
      is explicitly ruled out — it would still ship an incorrect circuit
      silently to the user, which is the exact failure mode this decision
      rejects.

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

- [x] Select Option A, B, or C above (or a different option not yet
      identified). — **Option B selected, 2026-07-25.** Rationale: the
      Adjudicator identified the silent empty-program fallback as an
      anti-pattern to reject outright (a user cannot tell their circuit was
      mishandled), which rules out Option C's "document as intentional"
      sub-choice and makes Option B the smallest change that satisfies the
      constraint. Option A remains open as a possible future upgrade from
      "honest rejection" to "correct output," not yet scheduled.
- [ ] If Option A: approve the call-graph/inlining boundary (recursion
      rejection, argument substitution rules, effect on existing Trotter/
      pattern-match paths). — N/A unless Option A is revisited later.
- [ ] If Option B or C: approve the new diagnostic code and message text. —
      Diagnostic code `QASM_FUNCTION_CALL_UNSUPPORTED` proposed (carried over
      from the original Option B description); exact message wording still
      needs explicit sign-off before Phase 1 Red.
- [ ] Approve Architecture Path design before any Phase 1 Red tests. —
      Option selection is recorded above; Phase 1 Red itself still needs a
      separate, explicit phase approval per the Approval Model (Architecture
      approval does not imply Phase approval).

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
- 2026-07-25: Architecture Path review. Adjudicator stated the controlling
  constraint: `emit-qasm` silently substituting the empty-program sketch
  (`h; measure`) for a program calling a measure-free `fn` is the compiler
  anti-pattern to avoid above all — a user could reasonably believe their
  circuit was processed correctly when it was silently discarded. This rules
  out Option C's "document the fallback as intentional" sub-choice (still
  ships wrong output, just documented) and leaves Option A (correct output
  via inlining, larger scope) or Option B (honest rejection, smallest scope)
  as the two paths that actually satisfy the constraint. **Option B
  selected** as the immediate accepted scope; Option A recorded as a
  possible future follow-up, not scheduled. No code changed — this is a
  documentation-only Architecture Path record. Phase 1 Red requires a
  separate explicit phase approval and confirmed diagnostic message text
  before any test is written.
