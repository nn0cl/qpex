# LISS-0154: Pipeline unary bare stage

## Metadata

- Local issue ID: LISS-0154
- Status: **complete** — 2026-07-31
- Depends on: [ADR 0122](../architecture/adr/0122-pipeline-unary-bare-stage.md)
- Program: [WP-0037](../work-plans/WP-0037-permanent-out-reopen.md)
- Tests: `tests/test_pipeline_unary_bare_red.py`

## Summary

Accept `lhs |> f` when `f` is a unary pure `fn` (ADR 0080 Decision 1 lock).

## Exit

- [x] Red/Green: unary bare stage typechecks; Operator bare stage rejected
