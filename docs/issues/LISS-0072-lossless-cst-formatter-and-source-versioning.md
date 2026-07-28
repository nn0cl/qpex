# LISS-0072: Lossless CST, formatter, and source versioning

## Metadata

- Local issue ID: LISS-0072
- GitHub issue: not created
- Status: **plan proposed** — Phase 0 Design Intake (2026-07-28)
- Phase: phase-0-design (plan approval required before Red)
- Type: frontend / CST / formatter / specification sync
- Priority: P0
- Initial planning size: L
- Current planning size: L (sliced A–D proposed)
- Owner/agent: —
- Related branch: `docs/liss-0072-cst-formatter-plan`
- Parent: [WP-0025](../work-plans/WP-0025-qpex-v1-north-star.md) E1 — Source and frontend
- Depends on: [LISS-0069](LISS-0069-canonical-mathematical-source-and-migration.md) **complete**;
  [LISS-0071](LISS-0071-versioned-conformance-and-differential-oracle.md) **complete** (catalog + SV index)

## Summary

Introduce a **lossless concrete syntax tree (CST)** with trivia preservation,
a **canonical formatter** that emits Unicode math spellings (ADR 0106 / M-P02–
M-P04), **source-version markers** for migration policy, and **EBNF catch-up**
for productions already shipped in the Python Kernel but absent from
[`grammar/qpex.ebnf`](../specs/grammar/qpex.ebnf).

Plan companion:
[`qpex-v1-cst-formatter-plan.md`](../specs/qpex-v1-cst-formatter-plan.md).

## Acceptance Notes (Issue complete when)

1. Lexer/parser retain comments and whitespace through a documented CST (or
   trivia-attached token stream) without discarding source structure needed for
   formatting.
2. `parse → format → parse` preserves **structural AST equality** and
   **comments** on a reviewed golden corpus (including
   `tests/fixtures/migration/` and selected SV snippets).
3. Formatter emits **canonical Unicode** for M-P02–M-P04 forms; output agrees
   with `migrate_unicode_math_source` on the migration golden corpus.
4. Malformed Unicode math (unterminated ket/bra, confusable pairs when
   enabled) produces **precise named diagnostics** — no silent repair.
5. Programs may declare `qpex_version = "…"` in package metadata; implicit
   default remains documented; unsupported versions fail with a named diagnostic.
6. [`grammar/qpex.ebnf`](../specs/grammar/qpex.ebnf) matches `lexer.py` /
   `parser.py` for: `evolve … until … max N`, numeric literal separators (ADR
   0101), scientific-scope keywords, and Unicode math tokens (LISS-0069).
7. Full SV regression remains green; no new language semantics without a
   separate Issue.

## Planned slices

| Slice | Scope | Phase gate |
|---|---|---|
| **A** | Trivia-aware lexing + CST skeleton (lossless capture contract) | plan → Red → Green → Refactor |
| **B** | Formatter emit + parse-format-parse AST equality + migration corpus parity | plan → Red → Green → Refactor |
| **C** | Source `qpex_version` markers + retired-keyword fix-it hints (diagnostic only) | plan → Red → Green → Refactor |
| **D** | EBNF catch-up + alignment check against shipping lexer/parser | plan → Red → Green → Refactor |

Optional follow-on (not in initial slice table unless Adjudicator expands scope):

- `qpex format` CLI surface (mirror `qpex migrate`; may land in Slice B if
  approved).
- NFC normalization at format boundary (deferred from LISS-0069 Slice A–C).
- LSP / notebook authoring (LISS-0105).

## Non-goals (initial)

- Rust CST/formatter (LISS-0070 deferred).
- Pauli ASCII removal (M-P01) or `state` sugar migration (M-P05).
- Bra / matrix-element desugar (LISS-0073).
- Automatic insertion of numeric literal separators (LISS-0061 non-goal).
- Semantic lowering or IR changes.

## Adjudicator Decision Points (plan)

- [ ] Approve planned slices A–D and Issue acceptance notes above.
- [ ] Confirm CST strategy: trivia-attached token stream vs full CST tree
      (plan recommends trivia-attached tokens first).
- [ ] Confirm round-trip oracle: structural AST equality + comment text
      preservation (not byte-identical source).
- [ ] Confirm NFC policy at format boundary: **preserve source NFC** in Slice B
      unless a follow-up Issue mandates normalize-on-emit.
- [ ] Confirm `qpex format` CLI in Slice B vs defer to LISS-0105.
- [ ] Approve Phase 1 Red for **Slice A only** after plan approval.

## Work Notes

- 2026-07-28: Phase 0 plan intake opened on `docs/liss-0072-cst-formatter-plan`.
  No compiler or test mutations until plan approval.

## Verification

- Plan PR: docs-only; links resolve; no `compiler/` or `tests/` changes.
- Post-approval: each slice follows Red → Green → Refactor with SV sweep after
  Refactor.
