# WP-0060: Mixed-unit arithmetic reject

| Field | Value |
|---|---|
| Status | **complete** (2026-07-31) |
| Branch | `feature/wp-0060-mixed-unit-reject` |
| Parent | ADR 0124 |

## Issue rows

| ID | Topic | Mode | Status |
|---|---|---|---|
| LISS-0186 | Reject mixed-unit +/− (ADR 0154) | ship | complete |

## Verification

- `python3 tests/test_mixed_unit_reject_red.py`
- `python3 tests/test_tonne_mass_red.py`
- `python3 tests/test_troy_ounce_mass_red.py`
