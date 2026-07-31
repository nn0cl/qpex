# WP-0039: SI catalog wave-2 + KetLit user-fn args

| Field | Value |
|---|---|
| Status | **complete** (2026-07-31) |
| Branch | `feature/wp-0039-si-catalog-ketlit-fn-args` |
| Parent | WP-0038 |

## Issue rows

| ID | Topic | Mode | Status |
|---|---|---|---|
| LISS-0161 | SI scale catalog wave-2 (ADR 0129) | ship | complete |
| LISS-0162 | User-fn State-forming Call args (ADR 0130) | ship | complete |

## Verification

- `python3 tests/test_si_scale_catalog_wave2_red.py`
- `python3 tests/test_user_fn_ketlit_args_red.py`
