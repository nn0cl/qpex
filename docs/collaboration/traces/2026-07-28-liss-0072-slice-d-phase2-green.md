# Trace: LISS-0072 Slice D Phase 2 Green

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0072 |
| Slice | D — EBNF catch-up + alignment gate |
| Phase | phase-2-green |
| Branch | `feature/liss-0072-slice-d-red` |
| Implementation | grammar catch-up + alignment helper only |

## [DESIGN CHECK]

- Scope and expected behavior: implement the smallest production/docs changes
  needed for the approved Slice D Red tests to pass.
- Specifications and files inspected: `docs/issues/LISS-0072-lossless-cst-formatter-and-source-versioning.md`;
  `docs/specs/staqex-v1-cst-formatter-plan.md`; `tests/test_ebnf_slice_d_red.py`;
  `docs/specs/grammar/staqex.ebnf`; `compiler/staqex/lexer.py`; `compiler/staqex/parser.py`;
  `compiler/staqex/tokens.py`.
- Component boundaries: grammar/documentation and deterministic comparison
  helper only; no runtime or formatter changes.
- Applicable constraints: no semantic parser/runtime changes in this phase.
- Decisions, assumptions, and unresolved ambiguities: the alignment helper
  tracks only the approved catch-up inventory, not full grammar completeness.
- Included and omitted AI context: included grammar and shipping inventory only;
  omitted runtime/backend/versioning/fix-it paths.
- Task routing: deterministic local edits + direct script execution.
- Verification plan: run `python3 tests/test_ebnf_slice_d_red.py`.

## Delivered

- `docs/specs/grammar/staqex.ebnf`
- `tests/spec_verification/harness/ebnf_inventory.py`

## Verification

- `python3 tests/test_ebnf_slice_d_red.py`
- Result: PASS

## Next safe action

Adjudicator Green approval → Slice D Phase 3 Refactor, if desired.
