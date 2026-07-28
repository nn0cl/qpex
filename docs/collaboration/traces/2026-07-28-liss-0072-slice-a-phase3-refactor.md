# Trace: LISS-0072 Slice A Phase 3 Refactor

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0072 |
| Slice | A — trivia-aware lexing + CST skeleton |
| Phase | phase-3-refactor |
| Branch | `feature/liss-0072-slice-a-red` |
| Implementation | helper extraction only |

## [DESIGN CHECK]

- Scope and expected behavior: refactor `compiler/qpex/cst.py` for readability
  only after Green; no assertion or behavior changes.
- Specifications and files inspected: `docs/issues/LISS-0072-lossless-cst-formatter-and-source-versioning.md`;
  `tests/test_cst_slice_a_red.py`; `compiler/qpex/cst.py`.
- Component boundaries: keep the new CST module isolated; no parser or formatter
  work in this phase.
- Applicable constraints: behavior unchanged; Red/Green assertions fixed.
- Decisions, assumptions, and unresolved ambiguities: parser integration remains
  for a later slice; this phase only reduces duplication in trivia attachment.
- Included and omitted AI context: included the minimal CST module and approved
  test contract; omitted unrelated compiler paths.
- Task routing: deterministic local edit + direct script verification.
- Verification plan: rerun `python3 tests/test_cst_slice_a_red.py`.

## Delivered

- `compiler/qpex/cst.py` helper extraction (`_with_leading`, `_with_trailing`)

## Verification

- `python3 tests/test_cst_slice_a_red.py`
- Result: PASS; behavior unchanged from Green

## Next safe action

Adjudicator Refactor approval → mark Slice A complete and open Slice B plan
intake for formatter + round-trip + migration parity.
