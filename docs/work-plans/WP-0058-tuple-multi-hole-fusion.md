# WP-0058: Tuple multi-hole pipe / Fusion fill

| Field | Value |
|---|---|
| Status | **complete** (2026-07-31) |
| Branch | `feature/wp-0058-tuple-multi-hole-fusion` |
| Parent | WP-0055 / ADR 0143 |

## Issue rows

| ID | Topic | Mode | Status |
|---|---|---|---|
| LISS-0184 | Tuple simultaneous multi-hole fill (ADR 0152) | ship | complete |

## Verification

- `python3 tests/test_tuple_multi_hole_fusion_red.py`
- `python3 tests/test_call_partial_fusion_red.py`
- `python3 tests/test_multi_hole_partial_pipe_red.py`
