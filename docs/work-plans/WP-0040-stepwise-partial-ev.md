# WP-0040: Stepwise Partial fill + eV↔J

| Field | Value |
|---|---|
| Status | **complete** (2026-07-31) |
| Branch | `feature/wp-0040-stepwise-partial-ev` |
| Parent | WP-0039 |

## Issue rows

| ID | Topic | Mode | Status |
|---|---|---|---|
| LISS-0163 | Stepwise Partial fill (ADR 0131) | ship | complete |
| LISS-0164 | Exact SI `eV`↔`J` (ADR 0132) | ship | complete |

## Verification

- `python3 tests/test_stepwise_partial_fill_red.py`
- `python3 tests/test_ev_joule_conversion_red.py`
