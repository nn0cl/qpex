# WP-0061: Mixed-unit canonical promote

| Field | Value |
|---|---|
| Status | **complete** (2026-07-31) |
| Branch | `feature/wp-0061-mixed-unit-canonical-promote` |
| Parent | WP-0060 / ADR 0154 superseded |

## Issue rows

| ID | Topic | Mode | Status |
|---|---|---|---|
| LISS-0187 | Canonical promote on mixed +/− (ADR 0155) | ship | complete |

## Verification

- `python3 tests/test_mixed_unit_canonical_promote_red.py`
- `python3 tests/test_mixed_unit_reject_red.py`
- `python3 tests/test_tonne_mass_red.py`
