# Trace: LISS-0072 Slice D plan intake

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0072 |
| Slice | D — EBNF catch-up + alignment gate |
| Phase | phase-0-design |
| Branch | `feature/liss-0072-slice-c-red` |
| Implementation | **forbidden** until Slice D plan approval |

## [DESIGN CHECK]

- Scope and expected behavior: propose Slice D only — catch up
  `docs/specs/grammar/staqex.ebnf` to shipped lexer/parser inventory and add a
  deterministic alignment gate.
- Specifications and files inspected: `docs/issues/LISS-0072-lossless-cst-formatter-and-source-versioning.md`;
  `docs/specs/staqex-v1-cst-formatter-plan.md`; `docs/specs/grammar/staqex.ebnf`;
  `docs/specs/staqex-language-specification.md` Appendix A; `compiler/staqex/lexer.py`;
  `compiler/staqex/parser.py`; `compiler/staqex/tokens.py`.
- Component boundaries: grammar/documentation and deterministic checks only; no
  runtime, formatter, or versioning behavior changes.
- Applicable constraints: named inventory catch-up, not full grammar redesign.
- Decisions, assumptions, and unresolved ambiguities: the alignment gate should
  compare documented inventory against shipping token maps / parser heads rather
  than asserting whole-parser completeness.
- Included and omitted AI context: included grammar and lexer/parser evidence;
  omitted runtime/backend/fix-it logic.
- Task routing: docs-only plan update.
- Verification plan: review the catch-up set and gate boundary; no compiler or
  test mutations in this step.

## Requested approval

**Plan approval** for Slice D only:

- EBNF catch-up for `until/max`, numeric separators, scientific scopes, Unicode
  math tokens, and modern keywords;
- a deterministic alignment gate against shipping lexer/parser inventory;
- no semantic/runtime changes.

Green is not implied unless later authorized.

## Next safe action

Adjudicator plan approval → Slice D Phase 1 Red.
