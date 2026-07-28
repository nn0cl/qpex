# Trace: LISS-0072 Slice D Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0072 |
| Slice | D — EBNF catch-up + alignment gate |
| Phase | phase-1-red |
| Branch | `feature/liss-0072-slice-d-red` |
| Implementation | **forbidden** |

## [DESIGN CHECK]

- Scope and expected behavior: add failing tests for the named EBNF catch-up
  inventory and a deterministic alignment helper.
- Specifications and files inspected: `docs/issues/LISS-0072-lossless-cst-formatter-and-source-versioning.md`;
  `docs/specs/qpex-v1-cst-formatter-plan.md`; `docs/specs/grammar/qpex.ebnf`;
  `compiler/qpex/lexer.py`; `compiler/qpex/parser.py`; `compiler/qpex/tokens.py`.
- Component boundaries: grammar/documentation and deterministic checks only; no
  runtime or formatter work.
- Applicable constraints: tests only; no semantic changes in Red.
- Decisions, assumptions, and unresolved ambiguities: alignment helper contract
  is intentionally small — report missing and extra inventory entries.
- Included and omitted AI context: included grammar and token inventory only;
  omitted runtime/backend/versioning/fix-it paths.
- Task routing: deterministic test-only edits + direct script execution.
- Verification plan: run `python3 tests/test_ebnf_slice_d_red.py`.

## Delivered

- `tests/test_ebnf_slice_d_red.py`

## Verification

- `python3 tests/test_ebnf_slice_d_red.py`
- Expected Red observed:
  - EBNF lacks `until/max`, numeric separators, scientific-scope heads, Unicode
    token alternates, and modern keywords
  - `tests.spec_verification.harness.ebnf_inventory` does not exist yet

## Next safe action

Adjudicator Red approval → Slice D Phase 2 Green for grammar catch-up and the
alignment helper only.
