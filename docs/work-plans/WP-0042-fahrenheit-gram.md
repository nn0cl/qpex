# WP-0042: Fahrenheit affine + gram scale

| Field | Value |
|---|---|
| Status | **complete** (2026-07-31) |
| Branch | `feature/wp-0042-fahrenheit-gram` |
| Parent | WP-0041 |

## Issue rows

| ID | Topic | Mode | Status |
|---|---|---|---|
| LISS-0167 | Affine °F↔K (ADR 0135) | ship | complete |
| LISS-0168 | Mass `g`↔`kg` (ADR 0136) | ship | complete |

## Verification

- `python3 tests/test_fahrenheit_kelvin_affine_red.py`
- `python3 tests/test_gram_kilogram_scale_red.py`
