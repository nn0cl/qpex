# LISS-0072: Lossless CST, formatter, and source versioning

## Metadata

- Local issue ID: LISS-0072
- GitHub issue: not created
- Status: **complete — Slice A/B/C/D approved** (2026-07-28)
- Phase: done (planned slices)
- Type: frontend / CST / formatter / specification sync
- Priority: P0
- Initial planning size: L
- Current planning size: L (sliced A–D)
- Owner/agent: —
- Related branch: `feature/liss-0072-slice-d-red`
- Parent: [WP-0025](../work-plans/WP-0025-staqex-v1-north-star.md) E1 — Source and frontend
- Depends on: [LISS-0069](LISS-0069-canonical-mathematical-source-and-migration.md) **complete**;
  [LISS-0071](LISS-0071-versioned-conformance-and-differential-oracle.md) **complete** (catalog + SV index)

## Summary

Introduce a **lossless concrete syntax tree (CST)** with trivia preservation,
a **canonical formatter** that emits Unicode math spellings (ADR 0106 / M-P02–
M-P04), **source-version markers** for migration policy, and **EBNF catch-up**
for productions already shipped in the Python Kernel but absent from
[`grammar/staqex.ebnf`](../specs/grammar/staqex.ebnf).

Plan companion:
[`staqex-v1-cst-formatter-plan.md`](../specs/staqex-v1-cst-formatter-plan.md).

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
5. Programs may declare `staqex_version = "…"` in package metadata; implicit
   default remains documented; unsupported versions fail with a named diagnostic.
6. [`grammar/staqex.ebnf`](../specs/grammar/staqex.ebnf) matches `lexer.py` /
   `parser.py` for: `evolve … until … max N`, numeric literal separators (ADR
   0101), scientific-scope keywords, and Unicode math tokens (LISS-0069).
7. Full SV regression remains green; no new language semantics without a
   separate Issue.

## Planned slices

| Slice | Scope | Phase gate |
|---|---|---|
| **A** | Trivia-aware lexing + CST skeleton (lossless capture contract) | **complete** |
| **B** | Formatter emit + parse-format-parse AST equality + migration corpus parity + minimal `staqex format` CLI | **complete** |
| **C** | Source `staqex_version` markers + retired-keyword fix-it hints (diagnostic only) | **complete** |
| **D** | EBNF catch-up + alignment check against shipping lexer/parser | **complete** |

Remaining intentional follow-ons (out of this Issue):

- NFC normalization at format boundary (deferred from LISS-0069 Slice A–C).
- Full pretty-printer beyond migrator-backed canonical emit.
- LSP / notebook authoring (LISS-0105).

## Non-goals (initial)

- Rust CST/formatter (LISS-0070 deferred).
- Pauli ASCII removal (M-P01) or `state` sugar migration (M-P05).
- Bra / matrix-element desugar (LISS-0073).
- Automatic insertion of numeric literal separators (LISS-0061 non-goal).
- Semantic lowering or IR changes.

## Adjudicator Decision Points (plan)

- [x] Approve planned slices A–D and Issue acceptance notes above.
- [x] Confirm CST strategy: trivia-attached token stream vs full CST tree
      (plan recommends trivia-attached tokens first).
- [x] Confirm round-trip oracle: structural AST equality + comment text
      preservation (not byte-identical source).
- [x] Confirm NFC policy at format boundary: **preserve source NFC** in Slice B
      unless a follow-up Issue mandates normalize-on-emit.
- [x] Confirm `staqex format` CLI in Slice B vs defer to LISS-0105.
- [x] Approve Phase 1 Red for **Slice A only** after plan approval.

## Adjudicator Decision Points (Slice A Red)

- [x] Approve Phase 1 Red assertions (`tests/test_cst_slice_a_red.py`).
- [x] Authorize Phase 2 Green for trivia-aware token retention plus CST
      skeleton only.

## Adjudicator Decision Points (Slice A Green)

- [x] Approve Phase 2 Green (`compiler/staqex/cst.py` only; no parser rewrite).
- [x] Authorize Phase 3 Refactor for readability only; no behavior change.

## Adjudicator Decision Points (Slice A Refactor)

- [x] Approve Phase 3 Refactor (helper extraction only; behavior unchanged).
- [x] Confirm Slice A complete and allow Slice B plan intake.

## Adjudicator Decision Points (Slice B plan)

- [x] Approve **Slice B** plan for Phase 1 Red (formatter core + round-trip +
      migration parity + minimal `staqex format` CLI only).
- [x] Confirm initial emit policy: canonical Unicode for M-P02–M-P04; preserve
      existing comment text and logical blank lines; no aggressive reflow.
- [x] Confirm round-trip oracle: structural AST equality, not byte-identical
      source.
- [x] Confirm initial corpus: `tests/fixtures/migration/` plus a small selected
      set of parser-valid snippets as follow-up if needed.
- [x] Confirm Slice B excludes `staqex_version` parsing and EBNF edits.
- [x] Approve Phase 1 Red for **Slice B only** after plan approval.

## Adjudicator Decision Points (Slice B Red)

- [x] Approve Phase 1 Red assertions (`tests/test_formatter_slice_b_red.py`).
- [x] Authorize Phase 2 Green for formatter core + minimal `staqex format` CLI
      only.

## Adjudicator Decision Points (Slice B Green)

- [x] Approve Phase 2 Green (`compiler/staqex/format.py` + minimal CLI wiring).
- [x] Authorize Phase 3 Refactor for readability only; no behavior change.

## Adjudicator Decision Points (Slice B Refactor)

- [x] Approve Phase 3 Refactor (shared rewrite helpers only; behavior unchanged).
- [x] Confirm Slice B complete and allow Slice C plan intake.

## Adjudicator Decision Points (Slice C plan)

- [x] Approve **Slice C** plan for Phase 1 Red (`staqex_version` parsing + named
      unsupported-version diagnostic + fix-it surfacing only).
- [x] Confirm initial `staqex_version` surface stays at package metadata level and
      does not imply semantic version switching beyond accept/reject.
- [x] Confirm fix-it scope: reuse existing `replacement` payload for
      `RETIRED_KEYWORD`; do not auto-edit source during compile.
- [x] Confirm `FORBIDDEN_KEYWORD` remains message-only unless a unique
      replacement already exists.
- [x] Confirm Slice C excludes EBNF sync and formatter policy changes.
- [x] Approve Phase 1 Red for **Slice C only** after plan approval.

## Adjudicator Decision Points (Slice C Red)

- [x] Approve Phase 1 Red assertions (`tests/test_versioning_slice_c_red.py`).
- [x] Authorize Phase 2 Green for package-level `staqex_version` parsing and
      named unsupported-version diagnostics only.

## Adjudicator Decision Points (Slice C Green)

- [x] Approve Phase 2 Green (parser + AST metadata + hard diagnostic only).
- [x] Authorize Phase 3 Refactor for readability only; no behavior change.

## Adjudicator Decision Points (Slice C Refactor)

- [x] Approve Phase 3 Refactor (helper extraction only; behavior unchanged).
- [x] Confirm Slice C complete and allow Slice D plan intake.

## Adjudicator Decision Points (Slice D plan)

- [x] Approve **Slice D** plan for Phase 1 Red (EBNF catch-up + alignment gate
      only; no runtime semantics changes).
- [x] Confirm minimum catch-up set: `until/max`, numeric separators, scientific
      scopes, Unicode math tokens, and modern keywords (`namespace`, `enum`,
      `struct`, `dynamic`, …).
- [x] Confirm the alignment gate may compare EBNF inventory against shipping
      lexer/parser keyword/operator sets.
- [x] Confirm Slice D excludes formatter policy, `staqex_version`, and runtime
      behavior changes.
- [x] Approve Phase 1 Red for **Slice D only** after plan approval.

## Adjudicator Decision Points (Slice D Red)

- [x] Approve Phase 1 Red assertions (`tests/test_ebnf_slice_d_red.py`).
- [x] Authorize Phase 2 Green for grammar catch-up and alignment helper only.

## Adjudicator Decision Points (Slice D Green)

- [x] Approve Phase 2 Green (`staqex.ebnf` catch-up + alignment helper only).
- [x] Authorize Phase 3 Refactor for readability only; no behavior change.

## Adjudicator Decision Points (Slice D Refactor / Issue)

- [x] Approve Phase 3 Refactor (inventory grouping only; behavior unchanged).
- [x] Confirm Slice D complete and LISS-0072 Slice A–D complete; remaining NFC /
      full pretty-print / LSP stay out or under LISS-0105.

## Work Notes

- 2026-07-28: Phase 0 plan intake opened on `docs/liss-0072-cst-formatter-plan`.
  No compiler or test mutations until plan approval.
- 2026-07-28: Adjudicator **plan approved** with the recommended direction:
  trivia-attached tokens first, structural AST + comment preservation as the
  round-trip oracle, preserve source NFC in formatter output, include a minimal
  `staqex format` CLI in Slice B, and allow the draft `staqex_version` surface for
  Red review.
- 2026-07-28: Phase 1 Red — `tests/test_cst_slice_a_red.py`. Expected Red state
  is a compile/import failure because `compiler/staqex/cst.py` and the lossless
  trivia API do not exist yet.
- 2026-07-28: Slice A Phase 2 Green — `compiler/staqex/cst.py` adds
  `lossless_lex()` and `build_lossless_cst()` with trivia-attached token
  records built from existing lexer spans. `python3 tests/test_cst_slice_a_red.py`
  PASS.
- 2026-07-28: Slice A Phase 3 Refactor — extracted small trivia-attachment
  helpers in `compiler/staqex/cst.py`; no behavior change.
- 2026-07-28: Slice A completion **approved**; Slice B plan proposed using the
  existing migration golden corpus as the initial parity and formatting oracle.
- 2026-07-28: Slice B plan **approved**. Phase 1 Red —
  `tests/test_formatter_slice_b_red.py`. Expected Red state is
  `ModuleNotFoundError: No module named 'compiler.staqex.format'` plus failing
  CLI assertions because `format` is not yet wired into `compiler/staqex/cli.py`.
- 2026-07-28: Adjudicator approved two test corrections discovered during Green:
  use fixture-real comment text for `comments_preserved.staqex`, and treat
  round-trip as **span-free structural AST equality** rather than raw dataclass
  equality.
- 2026-07-28: Slice B Phase 2 Green — `compiler/staqex/format.py` delegates the
  current canonical emit to the LISS-0069 migrator, `compiler/staqex/cli.py`
  wires a minimal `staqex format` subcommand, and `parser.py` treats `adjoint`
  as an operator-DSL reserved atom so ASCII and Unicode adjoint forms normalize
  consistently in `Operator` bindings. `python3 tests/test_formatter_slice_b_red.py`
  PASS.
- 2026-07-28: Slice B Phase 3 Refactor — shared rewrite emit/check helpers in
  `compiler/staqex/cli.py`; no behavior change.
- 2026-07-28: Slice B completion **approved**; Slice C plan proposed for
  package-level `staqex_version` validation and diagnostic fix-it surfacing.
- 2026-07-28: Slice C plan **approved**. Phase 1 Red —
  `tests/test_versioning_slice_c_red.py`. Expected Red state is
  `PARSE_ERROR` on top-level `staqex_version` because package metadata parsing is
  not implemented yet. Existing fix-it surfacing for `RETIRED_KEYWORD` already
  passes through `staqex check`.
- 2026-07-28: Slice C Phase 2 Green — `parser.py` accepts package-level
  `staqex_version = "1.0"` metadata, records the value on `CompilationUnit`, and
  reports `UNSUPPORTED_QPEX_VERSION` for unsupported values. `pipeline.py`
  treats that diagnostic as hard. Existing `RETIRED_KEYWORD` / `FORBIDDEN_KEYWORD`
  fix-it surfacing remains unchanged. `python3 tests/test_versioning_slice_c_red.py`
  PASS.
- 2026-07-28: Slice C Phase 3 Refactor — extracted a small parser helper for
  the package-level `staqex_version` detection path; no behavior change.
- 2026-07-28: Slice C completion **approved**; Slice D plan proposed for EBNF
  catch-up and a deterministic alignment gate against shipping lexer/parser
  inventory.
- 2026-07-28: Slice D plan **approved**. Phase 1 Red —
  `tests/test_ebnf_slice_d_red.py`. Expected Red state is missing EBNF coverage
  for `until/max`, numeric separators, scientific scopes, Unicode math tokens,
  and modern keywords, plus a missing alignment helper module.
- 2026-07-28: Slice D Phase 2 Green — `docs/specs/grammar/staqex.ebnf` catches up
  the named inventory (`until/max`, numeric separators, scientific scopes,
  Unicode math tokens, modern keywords, package metadata), and
  `tests/spec_verification/harness/ebnf_inventory.py` adds a deterministic
  grammar-vs-shipping inventory check. `python3 tests/test_ebnf_slice_d_red.py`
  PASS.
- 2026-07-28: Slice D Phase 3 Refactor — grouped inventory constants in
  `ebnf_inventory.py`; no behavior change.
- 2026-07-28: Slice D Refactor / Issue completion **approved** (“承認”).
  Planned slices A–D closed.

## Verification

- Slice A/B/C/D Red suites PASS through Refactor (`test_cst_slice_a_red.py`,
  `test_formatter_slice_b_red.py`, `test_versioning_slice_c_red.py`,
  `test_ebnf_slice_d_red.py`).
- Closeout: Adjudicator approved Slice A–D completion (2026-07-28).
- WP-0025 current next: LISS-0073.
