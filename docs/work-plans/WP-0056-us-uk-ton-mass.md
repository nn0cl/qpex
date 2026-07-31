# WP-0056: US/UK ton mass scales

| Field | Value |
|---|---|
| Status | **complete** (2026-07-31) |
| Branch | `feature/wp-0056-us-uk-ton-mass` |
| Parent | WP-0054 / ADR 0148 |

## Issue rows

| ID | Topic | Mode | Status |
|---|---|---|---|
| LISS-0182 | `.ton_us` / `.ton_uk` (ADR 0150) | ship | complete |

## Verification

- `python3 tests/test_us_uk_ton_mass_red.py`
- `python3 tests/test_tonne_mass_red.py`
