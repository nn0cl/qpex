# WP-0038: Partial holes, SI scale `to`, and reopen design ADRs

| Field | Value |
|---|---|
| Status | **complete** (2026-07-31) |
| Branch | `feature/wp-0038-partial-si-scale-design` |
| Parent | WP-0037 |

## Issue rows

| ID | Topic | Mode | Status |
|---|---|---|---|
| LISS-0155 | Partial `_` holes (ADR 0123) | ship | complete |
| LISS-0156 | SI `expr to unit` (ADR 0124) | ship | complete |
| LISS-0157 | Rational design boundary (ADR 0125) | docs | complete |
| LISS-0158 | Continuous PDF boundary (ADR 0126) | docs | complete |
| LISS-0159 | Live QPU credentials boundary (ADR 0127) | docs | complete |
| LISS-0160 | Trait/effect expansion boundary (ADR 0128) | docs | complete |

## Verification

- `python3 tests/test_function_partial_holes_red.py`
- `python3 tests/test_si_scale_conversion_red.py`
