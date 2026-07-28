# Trace: LISS-0072 Slice A Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0072 |
| Slice | A — trivia-aware lexing + CST skeleton |
| Phase | phase-1-red |
| Branch | `feature/liss-0072-slice-a-red` |
| Implementation | **forbidden** |

## [DESIGN CHECK]

- Scope and expected behavior: add failing tests for lossless trivia capture and
  a CST skeleton API only; no production implementation.
- Specifications and files inspected: `docs/issues/LISS-0072-lossless-cst-formatter-and-source-versioning.md`;
  `docs/specs/qpex-v1-cst-formatter-plan.md`; `compiler/qpex/lexer.py`;
  `compiler/qpex/parser.py`; `compiler/qpex/tokens.py`.
- Component boundaries: proposed `compiler/qpex/cst.py` module; existing lexer
  and parser remain the semantic baseline.
- Applicable constraints: tests only; no `compiler/qpex/` changes in Red.
- Decisions, assumptions, and unresolved ambiguities: accepted plan chooses
  trivia-attached tokens first; exact Green dataclass shapes remain to be
  finalized within the tested contract.
- Included and omitted AI context: included lexer/parser/token surfaces and
  approved plan; omitted unrelated runtime/backends.
- Task routing: deterministic file edits + local script execution.
- Verification plan: run the Red script directly and capture the expected
  missing-module failure.

## Delivered

- `tests/test_cst_slice_a_red.py`

## Verification

- `python3 tests/test_cst_slice_a_red.py`
- Expected Red observed: `ModuleNotFoundError: No module named 'compiler.qpex.cst'`

## Next safe action

Adjudicator Red approval → Slice A Phase 2 Green for trivia-aware token
retention and the initial `compiler/qpex/cst.py` skeleton.
