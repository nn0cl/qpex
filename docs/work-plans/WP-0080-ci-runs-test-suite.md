# WP-0080: CI runs root test suite (LISS-0209)

| Field | Value |
|---|---|
| Status | **complete** (awaiting PR merge) |
| Branch | `batch/wp-0080-ci-runs-test-suite` |
| Batch | [execution-batch-wp-0080.json](../collaboration/reviews/execution-batch-wp-0080.json) |
| Parent | After WP-0079 green floor; Adjudicator「はい」2026-08-02 |

## Locked rulings

- Blocking `python3 -m pytest tests/ -q` on PR and `main` pushes.
- Spec-verification **out of scope** (defer).
- pytest installed in the CI job only (no Kernel dependency).
- Do not weaken `repository-sanity`.

## Issues

| ID | Status |
|---|---|
| LISS-0209 | complete when CI job lands |

## Verification

Local: `.venv/bin/pytest tests/ -q` → 1062 passed / 0 failed (WP-0079 floor).
