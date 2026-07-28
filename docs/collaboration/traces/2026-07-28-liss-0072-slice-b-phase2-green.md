# Trace: LISS-0072 Slice B Phase 2 Green

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0072 |
| Slice | B — formatter + round-trip + migration parity |
| Phase | phase-2-green |
| Branch | `feature/liss-0072-slice-b-red` |
| Implementation | formatter core + minimal CLI wiring |

## [DESIGN CHECK]

- Scope and expected behavior: implement the smallest production code needed
  for the approved Slice B Red tests to pass.
- Specifications and files inspected: `docs/issues/LISS-0072-lossless-cst-formatter-and-source-versioning.md`;
  `docs/specs/qpex-v1-cst-formatter-plan.md`; `tests/test_formatter_slice_b_red.py`;
  `compiler/qpex/cli.py`; `compiler/qpex/migrate_unicode_math.py`; `compiler/qpex/parser.py`.
- Component boundaries: formatter remains a thin presentation-layer entry; it
  reuses the existing Unicode migrator rather than introducing a larger
  pretty-printer in this slice.
- Applicable constraints: no `qpex_version` or EBNF work; no broad parser
  rewrite.
- Decisions, assumptions, and unresolved ambiguities: AST round-trip is
  structural and span-free by approved correction; comment preservation matches
  actual migration fixtures.
- Included and omitted AI context: included formatter/CLI/migrator/parser touch
  points only; omitted runtime/backend/versioning/EBNF.
- Task routing: deterministic local edits + direct script execution.
- Verification plan: run `python3 tests/test_formatter_slice_b_red.py`.

## Delivered

- `compiler/qpex/format.py`
- `compiler/qpex/cli.py`
- `compiler/qpex/parser.py`

## Verification

- `python3 tests/test_formatter_slice_b_red.py`
- Result: PASS

## Next safe action

Adjudicator Green approval → Slice B Phase 3 Refactor, if desired.
