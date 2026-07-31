# WP-0062: SI residuals (`.u` / `.ton`)

| Field | Value |
|---|---|
| Status | **complete** (2026-07-31) |
| Branch | `feature/wp-0062-si-residuals` |
| Parent | ADR 0150 / 0151 |

## Issue rows

| ID | Topic | Mode | Status |
|---|---|---|---|
| LISS-0188 | Atomic mass `.u` | ship | complete |
| LISS-0189 | Bare `.ton` ≡ ton_us | ship | complete |

## Verification

- `python3 tests/test_si_residuals_red.py`
