# LISS-0073: Named Dirac notation and algebra AST

## Metadata

- Local issue ID: LISS-0073
- GitHub issue: not created
- Status: **Slice A complete — Refactor ready for review** (2026-07-28)
- Phase: slice-a phase-3-refactor
- Type: frontend / parser / typed algebra
- Priority: P0
- Initial planning size: XL
- Current planning size: XL (sliced A–G; F deferred until A–E)
- Owner/agent: —
- Related branch: `feature/liss-0073-slice-a-red`
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
| **A** | `BraLit` (or approved desugar) in `_primary` + EBNF; alone bra → algebra core | **complete — Refactor ready for review** |
| **B** | `⟨φ|ψ⟩` → `inner` (juxtaposition); collision regressions | plan → Red → Green → Refactor |
| **C** | `⟨φ|A|ψ⟩` matrix element; domain mismatch diagnostics | plan → Red → Green → Refactor |
| **D** | `|ψ⟩⟨φ|` / `|ψ⟩⟨ψ|` → `outer` / `projector`; document `OpHop` relation | plan → Red → Green → Refactor |
| **E** | Expression-side postfix `†` aligned with Operator-DSL `adjoint` | plan → Red → Green → Refactor |
| **F** | `[A,B]` / `{A,B}` → commutator / anticommutator (**deferred until A–E green**) | plan → Red → Green → Refactor |
| **G** | Typed algebra model freeze + formula→AST table proof; formatter emit follow | plan → Red → Green → Refactor |

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

- [ ] Approve Phase 3 Refactor (ket/bra typecheck merge; behavior unchanged).
- [ ] Confirm Slice A complete and allow Slice B plan intake.

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

## Verification

- Plan PR: docs-only; links resolve; no `compiler/` or `tests/` changes.
- Post-approval: each slice follows Red → Green → Refactor; SV sweep after
  Refactor of each Green.
