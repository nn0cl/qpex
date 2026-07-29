# Trace: LISS-0072 Slice C Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0072 |
| Slice | C — source versioning + fix-it surfacing |
| Phase | phase-1-red |
| Branch | `feature/liss-0072-slice-c-red` |
| Implementation | **forbidden** |

## [DESIGN CHECK]

- Scope and expected behavior: add failing tests for package-level
  `staqex_version` parsing and unsupported-version diagnostics while pinning the
  existing fix-it surfacing behavior.
- Specifications and files inspected: `docs/issues/LISS-0072-lossless-cst-formatter-and-source-versioning.md`;
  `docs/specs/staqex-v1-cst-formatter-plan.md`; `compiler/staqex/tokens.py`;
  `compiler/staqex/lexer.py`; `compiler/staqex/cli.py`.
- Component boundaries: parser/diagnostic work only; no formatter or EBNF
  changes.
- Applicable constraints: tests only; version marker is accept/reject metadata,
  not semantic branching.
- Decisions, assumptions, and unresolved ambiguities: diagnostic code name for
  unsupported versions is pinned in tests as `UNSUPPORTED_QPEX_VERSION`.
- Included and omitted AI context: included parser/diagnostic entry points only;
  omitted runtime/backend/formatter paths.
- Task routing: deterministic test-only edits + direct script execution.
- Verification plan: run `python3 tests/test_versioning_slice_c_red.py`.

## Delivered

- `tests/test_versioning_slice_c_red.py`

## Verification

- `python3 tests/test_versioning_slice_c_red.py`
- Expected Red observed:
  - `PARSE_ERROR` for top-level `staqex_version = "..."` metadata
  - fix-it surfacing tests already PASS

## Next safe action

Adjudicator Red approval → Slice C Phase 2 Green for package metadata parsing
and unsupported-version diagnostics only.
