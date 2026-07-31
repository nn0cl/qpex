# WP-0065: CPU data-parallel Deferred workers

| Field | Value |
|---|---|
| Status | **complete** (2026-07-31) |
| Branch | `feature/wp-0065-data-parallel-workers` |
| Parent | WP-0046 / ADR 0140 |

## Issue rows

| ID | Topic | Mode | Status |
|---|---|---|---|
| LISS-0192 | CPU ThreadPool over Joint worlds (ADR 0159) | ship | complete |

## Verification

- `python3 tests/test_data_parallel_workers_red.py`
- `python3 tests/test_deferred_pushforward_red.py` (if present)
