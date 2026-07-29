# LISS-0073: Named Dirac notation and algebra AST

## Metadata

- Local issue ID: LISS-0073
- GitHub issue: not created
- Status: **Slice G plan ready for review** (2026-07-29)
- Phase: slice-g phase-0-design
- Type: frontend / parser / typed algebra
- Priority: P0
- Initial planning size: XL
- Current planning size: XL (sliced A–G; A–F complete)
- Owner/agent: —
- Related branch: `feature/liss-0073-slice-f-red`
- Parent: [WP-0025](../work-plans/WP-0025-qpex-v1-north-star.md) E1 — Source and frontend
- Depends on: [LISS-0069](LISS-0069-canonical-mathematical-source-and-migration.md) **complete**;
  [LISS-0072](LISS-0072-lossless-cst-formatter-and-source-versioning.md) **complete**;
  [LISS-0031](LISS-0031-operator-algebra-and-dirac-notation.md) **Phase 3 reviewed**
  (function-shaped typed algebra remains the semantic core)

## Summary

Extend the shipping frontend so **named Dirac punctuation** — bras, matrix
elements, projectors / outer products, expression-side adjoints, and
commutator / anticommutator brackets — parses into **one typed algebra model**
that lowers to the same contracts as LISS-0031 / ADR 0087
(`adjoint` / `inner` / `outer` / `projector` / `commutator` /
`anticommutator`, plus existing `KetLit` / `TensorExpr`).

No macro or string rewriting of formulas. Domain mismatches and pipeline /
Unicode collisions remain hard errors. Physics IR lowering (LISS-0081) stays
out of scope.

Plan companion:
[`qpex-v1-dirac-algebra-ast-plan.md`](../specs/qpex-v1-dirac-algebra-ast-plan.md).

## Acceptance Notes (Issue complete when)

1. Formula-to-AST mappings for the approved punctuation surface are
   **unambiguous** and documented (companion §formula map).
2. Each punctuation form lowers to the **same typed algebra contracts** as the
   corresponding function-shaped call (or an Adjudicator-approved equivalent
   first-class node that typechecks identically).
3. Domain / carrier mismatches and pipeline / `|>` / `⟩` collisions produce
   **named hard diagnostics** — not silent repair or string macros.
4. `⟨φ|ψ⟩`, `⟨φ|A|ψ⟩`, `|ψ⟩⟨φ|` / `|ψ⟩⟨ψ|`, expression-side `†` (if approved),
   and `[A,B]` / `{A,B}` (if approved) parse on a reviewed golden corpus.
5. Function-shaped forms remain dual-accept unless Adjudicator selects an
   M-P06 deprecate gate in this Issue.
6. EBNF / language-spec precedence catch-up for accepted forms lands with the
   slices that introduce them (or a final sync slice).
7. Full SV regression remains green; no new Physics IR / symbolic evaluator.

## Planned slices

| Slice | Scope | Phase gate |
|---|---|---|
| **A** | `BraLit` (or approved desugar) in `_primary` + EBNF; alone bra → algebra core | **complete** |
| **B** | `⟨φ|ψ⟩` → `inner` (juxtaposition); collision regressions | **complete** |
| **C** | `⟨φ|A|ψ⟩` matrix element; domain mismatch diagnostics | **complete** |
| **D** | `|ψ⟩⟨φ|` / `|ψ⟩⟨ψ|` → `outer` / `projector`; document `OpHop` relation | **complete** (PR #99) |
| **E** | Expression-side postfix `†` aligned with Operator-DSL `adjoint` | **complete** |
| **F** | `[A,B]` / `{A,B}` → commutator / anticommutator | **complete** |
| **G** | Typed algebra model freeze + formula→AST table proof; formatter emit follow | **plan ready for review** |

## Non-goals (initial)

- Physics IR / symbolic Hamiltonian lowering (LISS-0081).
- NFC normalize-on-read (deferred from LISS-0069).
- Pauli ASCII removal (M-P01) or `state` sugar (M-P05).
- Full CST pretty-printer beyond LISS-0072 migrator-backed emit.
- Rust frontend (LISS-0070 deferred).
- Non-square operator codomain algebra (still deferred from LISS-0031).
- Continuous / second-quantized sugar beyond existing JW paths.

## Adjudicator Decision Points (plan)

- [x] Approve planned slices A–G and Issue acceptance notes above.
- [x] Confirm bra strategy: first-class `BraLit` vs immediate desugar to
      `Call`/`OpCall` (plan recommends **first-class `BraLit` + lower to
      adjoint(ket) / algebra contracts in typecheck**).
- [x] Confirm matrix-element parse strategy: `BRA` + middle expr + `KET`
      juxtaposition (plan recommends this; no composite lexer token).
- [x] Confirm `[A,B]` / `{A,B}`: include in Slice F with explicit disambiguation
      vs `ListExpr` / braces, **or** defer bracket sugar and keep function forms
      only (plan recommends **defer F until A–E green**, then decide).
- [x] Confirm expression-side `†`: align with Operator DSL in Slice E
      (plan recommends **yes**).
- [x] Confirm M-P06: keep function-shaped dual-accept through this Issue
      (plan recommends **dual-accept**; deprecate gate is a later Issue).
- [x] Confirm diagnostics: reuse `OPERATOR_ALGEBRA_TYPE_ERROR` where applicable;
      add named parse codes only when collision/shape needs a distinct code.
- [x] Approve Phase 1 Red for **Slice A only** after plan approval.

## Adjudicator Decision Points (Slice A Red)

- [x] Approve Phase 1 Red assertions (`tests/test_dirac_slice_a_red.py`).
- [x] Authorize Phase 2 Green for `BraLit` + `_primary` BRA wiring + EBNF
      `bra_lit` in `primary` + alone-bra typecheck only.

## Adjudicator Decision Points (Slice A Green)

- [x] Approve Phase 2 Green (`BraLit` + parser BRA + typecheck + EBNF).
- [x] Authorize Phase 3 Refactor for readability only; no behavior change.

## Adjudicator Decision Points (Slice A Refactor)

- [x] Approve Phase 3 Refactor (ket/bra typecheck merge; behavior unchanged).
- [x] Confirm Slice A complete and allow Slice B plan intake.

## Adjudicator Decision Points (Slice B plan)

- [x] Approve **Slice B** plan for Phase 1 Red only (`⟨φ|ψ⟩` → `inner` +
      collision regressions).
- [x] Confirm parse shape: AST is `Call(inner, [BraLit, KetLit])` for
      north-star spelling `⟨φ|ψ⟩` (single bar; Green synthesizes the ket half
      after bra close — not a double-bar `⟨φ||ψ⟩` source requirement).
- [x] Confirm Slice B excludes matrix elements (`⟨φ|A|ψ⟩`), outer/projector,
      expression `†`, and bracket sugar.
- [x] Confirm collision tests: `|>` remains pipeline; Unicode ket close `⟩`
      does not lex as pipeline; alone `BraLit` from Slice A still parses.
- [x] Approve Phase 1 Red for **Slice B only** after plan approval.

## Adjudicator Decision Points (Slice B Red)

- [x] Approve Phase 1 Red assertions (`tests/test_dirac_slice_b_red.py`).
- [x] Authorize Phase 2 Green for `⟨φ|ψ⟩` → `inner` Call + EBNF note +
      collision/alone-bra regressions only.

## Adjudicator Decision Points (Slice B Green)

- [x] Approve Phase 2 Green (lexer ket-half after bra + parser `inner` Call +
      EBNF `bra_ket_inner`).
- [x] Authorize Phase 3 Refactor for readability only; no behavior change.

## Adjudicator Decision Points (Slice B Refactor)

- [x] Approve Phase 3 Refactor (`_bra_or_inner` + lexer checkpoint; behavior
      unchanged).
- [x] Confirm Slice B complete and allow Slice C plan intake.

## Adjudicator Decision Points (Slice C plan)

- [x] Approve **Slice C** plan for Phase 1 Red only (`⟨φ|A|ψ⟩` matrix element +
      domain mismatch diagnostics).
- [x] Confirm AST lowering (recommended):
      `Call(inner, [BraLit(φ), Call(A, [KetLit(ψ)])])`
      i.e. `inner(φ, A(ψ))` dual with function-shaped algebra; middle `A` is a
      primary/call-level expression (typically Operator ident).
- [x] Confirm parse disambiguation vs Slice B: after `BRA`, if next token is
      `KET` → inner (B); else parse mid-expr then require `KET` for matrix
      element; if mid-expr fails or no trailing `KET`, alone `BraLit` (A).
- [x] Confirm domain mismatches reuse `OPERATOR_ALGEBRA_TYPE_ERROR` (and
      existing operator/state checks on `inner` / call apply).
- [x] Confirm Slice C excludes outer/projector (D), expression `†` (E), brackets
      (F).
- [x] Approve Phase 1 Red for **Slice C only** after plan approval.

## Adjudicator Decision Points (Slice C Red)

- [x] Approve Phase 1 Red assertions (`tests/test_dirac_slice_c_red.py`).
- [x] Authorize Phase 2 Green for matrix-element parse + EBNF + A/B regressions
      only.

## Adjudicator Decision Points (Slice C Green / Refactor)

- [x] Approve Phase 2 Green + Phase 3 Refactor (`_bra_or_inner` matrix fold,
      `_check_matrix_element_middle`, `_PAULI_ATOM_NAMES`).
- [x] Confirm Slice C complete and allow Slice D plan intake.

## Adjudicator Decision Points (Slice D plan)

- [x] Approve **Slice D** plan for Phase 1 Red only (`|ψ⟩⟨φ|` → `outer`,
      `|ψ⟩⟨ψ|` → `projector`; document `OpHop` relation).
- [x] Confirm AST (recommended): after `KET`, if next is `BRA` then
      `Call(outer, [KetLit, BraLit])`; if bra label equals ket label,
      `Call(projector, [KetLit])` (prefer `projector` when labels match).
- [x] Confirm Slice D excludes expression `†` (E) and brackets (F).
- [x] Approve Phase 1 Red for **Slice D only** after plan approval.

## Adjudicator Decision Points (Slice D Red)

- [x] Approve Phase 1 Red assertions (`tests/test_dirac_slice_d_red.py`).
- [x] Authorize Phase 2 Green for ket–bra outer/projector + EBNF/`OpHop` note
      only.

## Adjudicator Decision Points (Slice D Green / Refactor)

- [x] Approve Phase 2 Green + Phase 3 Refactor (`_ket_or_outer`, Operator bind
      KET/BRA routing, `_algebra_call`, EBNF `ket_bra_outer`).
- [x] Confirm Slice D complete and allow Slice E plan intake.

## Adjudicator Decision Points (Slice E plan)

- [x] Approve **Slice E** plan for Phase 1 Red only (expression-side postfix
      `†` → `Call(adjoint, [expr])` in `_call`; dual-accept with `adjoint(…)`;
      Operator DSL `OpCall("adjoint")` unchanged).
- [x] Confirm precedence: `†` is a postfix in the `_call` loop (same tier as
      call / attr), so `X†(ψ)` = `adjoint(X)(ψ)` and `(X+Y)†` works after
      parentheses.
- [x] Confirm Slice E excludes brackets (F) and does not change OpDSL dagger.
- [x] Approve Phase 1 Red for **Slice E only** after plan approval.

## Adjudicator Decision Points (Slice E Red)

- [x] Approve Phase 1 Red assertions (`tests/test_dirac_slice_e_red.py`).
- [x] Authorize Phase 2 Green for expression `_call` dagger + EBNF note only.

## Adjudicator Decision Points (Slice E Green / Refactor)

- [x] Approve Phase 2 Green + Phase 3 Refactor (`_call` `DAGGER` →
      `_algebra_call("adjoint", …)`, EBNF `dagger_suffix`).
- [x] Confirm Slice E complete and allow Slice F plan intake (deferred brackets)
      or Issue closeout path via Slice G.

## Adjudicator Decision Points (Slice F plan)

- [x] Approve **Slice F** plan for Phase 1 Red only (`[A,B]` → `commutator`,
      `{A,B}` → `anticommutator`) with the recommended disambiguation below.
- [x] Confirm disambiguation (recommended):
      - **Operator bind / OpDSL**: `[A, B]` → commutator; `{A, B}` →
        anticommutator (exactly two comma-separated operands).
      - **Expression `_primary`**: keep existing `ListExpr` for `[…]`; do **not**
        steal two-element lists. Expression-side punctuation for commutator
        remains optional follow-up (function form stays dual-accept).
      - `{A, B}` in expression primary (no set/dict literal today) →
        `Call(anticommutator, [A, B])`.
- [x] Confirm Slice F excludes model freeze (G) and does not change ListExpr
      semantics for length ≠ 2 or non-Operator contexts beyond the above.
- [x] Approve Phase 1 Red for **Slice F only** after plan approval.

## Adjudicator Decision Points (Slice F Red)

- [x] Approve Phase 1 Red assertions (`tests/test_dirac_slice_f_red.py`).
- [x] Authorize Phase 2 Green for Operator-context brackets + expr `{A,B}` +
      EBNF only.

## Adjudicator Decision Points (Slice F Green / Refactor)

- [x] Approve Phase 2 Green + Phase 3 Refactor (Operator-context `[A,B]`,
      `{A,B}` → algebra `Call`, EBNF `bracket_commutator` /
      `brace_anticommutator`, comma-item helpers).
- [x] Confirm Slice F complete and allow Slice G plan intake (algebra model
      freeze + formula→AST table).

## Adjudicator Decision Points (Slice G plan)

- [ ] Approve **Slice G** plan for Phase 1 Red only (docs + proof suite; no new
      punctuation surface).
- [ ] Confirm Slice G deliverables (recommended):
      1. Freeze §4 formula→AST map to match shipped A–F behavior (update
         `[A,B]` / `{A,B}` rows from “if approved” to shipped Operator-context
         / brace rules).
      2. Red/Green proof suite `tests/test_dirac_slice_g_red.py` that asserts
         each table row’s punctuation parses to the documented AST shape
         (reusing A–F oracles; no new runtime).
      3. Formatter emit policy note: dual-accept retained; `qpex format` /
         migrator **may** emit function forms or Unicode punctuation; full
         pretty-print rewrite is **out of scope** (LISS-0072 follow-up).
      4. Mark LISS-0073 acceptance notes satisfied when the proof suite and
         formula table are Green; Issue status → complete.
- [ ] Confirm Slice G excludes: new sugar, Physics IR, NFC, M-P06 deprecate.
- [ ] Approve Phase 1 Red for **Slice G only** after plan approval.

## Work Notes

- 2026-07-28: Plan intake opened after LISS-0072 completion merge (PR #94).
  Dependencies LISS-0069 / LISS-0072 confirmed complete. LISS-0031 remains the
  semantic core (function-shaped typed algebra).
- 2026-07-28: Plan **approved** (“承認”) with recommended defaults: first-class
  `BraLit`; juxtaposition matrix elements; defer Slice F until A–E; expression
  `†` in E; M-P06 dual-accept; reuse `OPERATOR_ALGEBRA_TYPE_ERROR` where
  applicable; Slice A Phase 1 Red authorized.
- 2026-07-28: Slice A Phase 1 Red — `tests/test_dirac_slice_a_red.py`. Expected
  Red state is `ImportError: cannot import name 'BraLit'` (node not yet in
  `ast_nodes`); subsequent assertions cover PARSE_ERROR / EBNF primary gap.
- 2026-07-28: Slice A Phase 1 Red **approved**; Phase 2 Green — `BraLit` node,
  `_primary` BRA wiring, typecheck carrier parity with `KetLit` for alone bra,
  EBNF `bra_lit` in `primary`. Red helper corrected to walk `MainDecl` (not
  `FunDecl`). `python3 tests/test_dirac_slice_a_red.py` PASS.
- 2026-07-28: Slice A Phase 2 Green **approved**; Phase 3 Refactor — merged
  ket/bra typecheck branch; adjacent parser matches. Behavior unchanged;
  `python3 tests/test_dirac_slice_a_red.py` PASS.
- 2026-07-28: Slice A Refactor / completion **approved** (“承認”). Slice B plan
  proposed for `⟨φ|ψ⟩` → `inner` juxtaposition.
- 2026-07-28: Slice B plan **approved** (“承認”). Phase 1 Red —
  `tests/test_dirac_slice_b_red.py`. Clarified north-star single-bar `⟨φ|ψ⟩`
  (not `⟨φ||ψ⟩`); AST remains `Call(inner, [BraLit, KetLit])`. Expected Red:
  `LEX_ERROR` / missing juxtaposition on `⟨0|1⟩`.
- 2026-07-28: Slice B Phase 1 Red **approved**; Phase 2 Green — lexer emits
  optional ket half after `BRA` for `⟨φ|ψ⟩`; parser builds
  `Call(inner, [BraLit, KetLit])`; EBNF `bra_ket_inner`. 
  `python3 tests/test_dirac_slice_b_red.py` PASS.
- 2026-07-28: Slice B Phase 2 Green **approved**; Phase 3 Refactor — extracted
  `_bra_or_inner`; lexer ket-half backtrack uses a checkpoint tuple. Behavior
  unchanged; Slice B/A Red suites PASS.
- 2026-07-28: Slice B Refactor / completion **approved** (“承認”). Slice C plan
  proposed for `⟨φ|A|ψ⟩` → `inner(φ, A(ψ))`.
- 2026-07-28: Slice C plan **approved** (“承認”). Phase 1 Red —
  `tests/test_dirac_slice_c_red.py`. Expected Red: `PARSE_ERROR` on
  `⟨0|X|1⟩` (BRA + IDENT + KET not folded). Function-shaped
  `inner(|0>, X(|1>))` already typechecks (Green oracle).
- 2026-07-28: Adjudicator “進めて” — Slice C Phase 2 Green + Phase 3 Refactor.
  Parser folds `BRA`+mid+`KET` to `inner(φ, A(ψ))`; typecheck rejects State
  middle; EBNF `bra_op_ket`. Suites A/B/C PASS. Slice D plan proposed.
- 2026-07-28: Slice D plan **approved** (“承認”). Phase 1 Red —
  `tests/test_dirac_slice_d_red.py`. Expected Red: `PARSE_ERROR` on
  `|0⟩⟨1|` (KET+BRA not folded). Function-shaped `outer` / `projector` already
  typecheck (Green oracle).
- 2026-07-28: Slice D Phase 1 Red **approved** (“承認”); Phase 2 Green +
  Phase 3 Refactor. Parser `_ket_or_outer` folds KET+BRA to `outer` /
  matching-label `projector`; `Operator` bind routes Dirac tokens to
  `_expression`; EBNF `ket_bra_outer`. Suites A/B/C/D PASS.
- 2026-07-28: Slice D merged via PR #99 (`ba29b2c`).
- 2026-07-29: Slice D completion **approved** (“承認”). Slice E plan proposed
  for expression-side postfix `†` → `Call(adjoint, [expr])`.
- 2026-07-29: Slice E plan **approved** (“承認”). Phase 1 Red —
  `tests/test_dirac_slice_e_red.py`. Expected Red: `PARSE_ERROR` on
  `state a = X†` (expression `_call` does not fold `DAGGER`). Function-shaped
  `adjoint(X)` and OpDSL `Operator A = X†` already typecheck (Green oracles).
- 2026-07-29: Slice E Phase 1 Red **approved** (“承認”); Phase 2 Green +
  Phase 3 Refactor. Expression `_call` folds `DAGGER` to
  `Call(adjoint, [expr])`; EBNF `dagger_suffix`. Suites A–E + unicode math
  PASS.
- 2026-07-29: Slice E completion **approved** (“承認”). Slice F plan proposed
  for `[A,B]` / `{A,B}` with Operator-context vs `ListExpr` disambiguation.
- 2026-07-29: Slice E merged via PR #100 (`c1e2fdf`).
- 2026-07-29: Slice F plan **approved** (“承認”, recommended disambiguation).
  Phase 1 Red — `tests/test_dirac_slice_f_red.py`. Expected Red: `PARSE_ERROR`
  on `Operator C = [X, Y]` / `{X, Y}` and expression `{X, Y}`. Function-shaped
  forms and expression `ListExpr` already Green.
- 2026-07-29: Slice F Phase 1 Red **approved** (“承認”); Phase 2 Green +
  Phase 3 Refactor. Operator-context `[A,B]` → `commutator`; `{A,B}` →
  `anticommutator`; expr `ListExpr` preserved; EBNF bracket productions.
  Suites A–F PASS.
- 2026-07-29: Slice F completion **approved** (“承認”). Slice G plan proposed
  (formula→AST freeze + proof suite + formatter emit policy note).

## Verification

- Slice A: merged via PR #96.
- Slice B: merged via PR #97.
- Slice C: merged via PR #98.
- Slice D: merged via PR #99.
- Slice E: merged via PR #100.
- Slice F: Green/Refactor on `feature/liss-0073-slice-f-red`; suites A–F PASS
  (PR pending).
- Slice G: plan only until approval; Red suite TBD
  `tests/test_dirac_slice_g_red.py`.
- Post-approval: each slice follows Red → Green → Refactor; SV sweep after
  Refactor of each Green.
