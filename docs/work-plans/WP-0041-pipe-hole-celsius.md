# WP-0041: Pipeline hole fill + °C↔K

| Field | Value |
|---|---|
| Status | **complete** (2026-07-31) |
| Branch | `feature/wp-0041-pipe-hole-celsius` |
| Parent | WP-0040 |

## Issue rows

| ID | Topic | Mode | Status |
|---|---|---|---|
| LISS-0165 | Pipeline leftmost hole fill (ADR 0133) | ship | complete |
| LISS-0166 | Affine °C↔K (ADR 0134) | ship | complete |

## Verification

- `python3 tests/test_pipeline_leftmost_hole_red.py`
- `python3 tests/test_celsius_kelvin_affine_red.py`
