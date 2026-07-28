# Trace: LISS-0072 Slice A Phase 2 Green

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0072 |
| Slice | A — trivia-aware lexing + CST skeleton |
| Phase | phase-2-green |
| Branch | `feature/liss-0072-slice-a-red` |
| Implementation | `compiler/qpex/cst.py` only |

## [DESIGN CHECK]

- Scope and expected behavior: implement the smallest production code needed
  for the approved Slice A Red tests to pass.
- Specifications and files inspected: `docs/issues/LISS-0072-lossless-cst-formatter-and-source-versioning.md`;
  `docs/specs/qpex-v1-cst-formatter-plan.md`; `tests/test_cst_slice_a_red.py`;
  `compiler/qpex/lexer.py`; `compiler/qpex/tokens.py`.
- Component boundaries: new `compiler/qpex/cst.py` module; existing lexer stays
  the token authority and existing parser remains unchanged.
- Applicable constraints: no parser rewrite, no formatter work, no EBNF edits.
- Decisions, assumptions, and unresolved ambiguities: trivia is reconstructed
  from source gaps between lexer token spans; parser integration is deferred to
  later slices/refactor.
- Included and omitted AI context: included only the approved Red contract and
  lexer/token surfaces; omitted unrelated runtime/backend paths.
- Task routing: deterministic local edits + direct script execution.
- Verification plan: run `python3 tests/test_cst_slice_a_red.py`.

## Delivered

- `compiler/qpex/cst.py`

## Verification

- `python3 tests/test_cst_slice_a_red.py`
- Result: PASS (`lossless_lex` and `build_lossless_cst` satisfy the Red tests)

## Next safe action

Adjudicator Green approval → Slice A Phase 3 Refactor, if readability changes
are desired; otherwise move to Slice A completion / Slice B plan.
