# Trace: LISS-0072 Slice B Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0072 |
| Slice | B — formatter + round-trip + migration parity |
| Phase | phase-1-red |
| Branch | `feature/liss-0072-slice-b-red` |
| Implementation | **forbidden** |

## [DESIGN CHECK]

- Scope and expected behavior: add failing tests for formatter core, migration
  corpus parity, AST round-trip, and minimal `qpex format` CLI only.
- Specifications and files inspected: `docs/issues/LISS-0072-lossless-cst-formatter-and-source-versioning.md`;
  `docs/specs/qpex-v1-cst-formatter-plan.md`; `compiler/qpex/cli.py`;
  `compiler/qpex/pipeline.py`; `compiler/qpex/migrate_unicode_math.py`;
  `tests/fixtures/migration/`; `tests/test_unicode_math_migrate_cli_red.py`.
- Component boundaries: new formatter module should stay separate from parser
  and semantic pipeline logic; CLI mirrors `migrate` only.
- Applicable constraints: tests only; no `qpex_version` or EBNF work in this
  slice.
- Decisions, assumptions, and unresolved ambiguities: round-trip oracle is
  structural AST equality, not byte-identical source; migration goldens are the
  initial canonical emit corpus.
- Included and omitted AI context: included formatter/CLI/migrator fixtures;
  omitted runtime/backends/versioning/EBNF.
- Task routing: deterministic test-only edits + direct script execution.
- Verification plan: run `python3 tests/test_formatter_slice_b_red.py` and
  capture the expected missing-module / missing-command failures.

## Delivered

- `tests/test_formatter_slice_b_red.py`

## Verification

- `python3 tests/test_formatter_slice_b_red.py`
- Expected Red observed:
  - `ModuleNotFoundError: No module named 'compiler.qpex.format'`
  - `qpex format` CLI assertions fail because the subcommand is not wired

## Next safe action

Adjudicator Red approval → Slice B Phase 2 Green for `compiler/qpex/format.py`
and minimal CLI wiring only.
