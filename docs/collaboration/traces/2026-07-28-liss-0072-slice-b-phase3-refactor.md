# Trace: LISS-0072 Slice B Phase 3 Refactor

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0072 |
| Slice | B — formatter + round-trip + migration parity |
| Phase | phase-3-refactor |
| Branch | `feature/liss-0072-slice-b-red` |
| Implementation | shared CLI helper extraction only |

## [DESIGN CHECK]

- Scope and expected behavior: refactor the new `format` CLI wiring for
  readability only after Green; no assertion or behavior changes.
- Specifications and files inspected: `docs/issues/LISS-0072-lossless-cst-formatter-and-source-versioning.md`;
  `tests/test_formatter_slice_b_red.py`; `compiler/staqex/cli.py`.
- Component boundaries: formatter logic stays in `compiler/staqex/format.py`;
  CLI just shares rewrite helper code.
- Applicable constraints: behavior unchanged; no parser/formatter feature growth.
- Decisions, assumptions, and unresolved ambiguities: the formatter remains a
  migrator-backed minimal implementation for this slice.
- Included and omitted AI context: included only the formatter CLI touch points;
  omitted versioning/EBNF/runtime/backend paths.
- Task routing: deterministic local edit + direct script verification.
- Verification plan: rerun `python3 tests/test_formatter_slice_b_red.py`.

## Delivered

- `compiler/staqex/cli.py` helper extraction for shared rewrite emit/check paths

## Verification

- `python3 tests/test_formatter_slice_b_red.py`
- Result: PASS; behavior unchanged from Green

## Next safe action

Adjudicator Refactor approval → mark Slice B complete and open Slice C plan
intake.
