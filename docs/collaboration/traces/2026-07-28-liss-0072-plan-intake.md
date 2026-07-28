# Trace: LISS-0072 Phase 0 plan intake

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0072 |
| Path | Feature Path — documentation / plan only |
| Phase | phase-0-design |
| Branch | `docs/liss-0072-cst-formatter-plan` |
| Implementation | **forbidden** until plan approval |

## [DESIGN CHECK]

- Scope: Propose lossless CST, formatter, source-version markers, and EBNF
  catch-up as slices A–D; no Red.
- Specs inspected: WP-0025 E1; ADR 0106 Unicode + D9 pipeline; compiler
  blueprint §3.1; rebaseline register §6–7; LISS-0069 migrator/CLI; LISS-0071
  conformance catalog; `grammar/qpex.ebnf` gap list in language spec Appendix A.
- Boundaries: Python Kernel only; presentation layer; SV behavior oracle
  unchanged; Rust/LSP out.
- Decisions pending Adjudicator: CST strategy (trivia-attached tokens vs full
  tree); round-trip oracle (AST + comments); NFC on emit; `qpex format` CLI in
  Slice B vs LISS-0105; `qpex_version` syntax.
- Verification: docs PR; no `compiler/` or `tests/` mutations.

## Delivered

- `docs/issues/LISS-0072-lossless-cst-formatter-and-source-versioning.md`
- `docs/specs/qpex-v1-cst-formatter-plan.md`
- `docs/architecture/open-work-register.md` (LISS-0072 row)

## Requested approval

**Plan approval** for LISS-0072 slices A–D:

- Slice A: trivia-aware lexing + CST skeleton;
- Slice B: formatter + parse-format-parse + migration parity;
- Slice C: `qpex_version` + retired-keyword fix-its;
- Slice D: EBNF catch-up + alignment gate.

Phase 1 Red authorized for **Slice A only** after plan approval. Green not
implied unless batch autonomy granted.

## Explicitly not authorized yet

- Phase 1 Red tests
- `compiler/qpex/` production changes
- EBNF edits
- `qpex format` CLI (pending Adjudicator choice)

## Next safe action

Adjudicator plan approval → Slice A Phase 1 Red on a feature branch.
