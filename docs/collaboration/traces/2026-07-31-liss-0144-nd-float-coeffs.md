# Trace: LISS-0144 ND Float coefficient tensors

| Field | Value |
|---|---|
| Date | 2026-07-31 |
| Agent | Cursor Composer |
| Branch | `feature/liss-0144-nd-float-coeffs` |
| Issue | LISS-0144 |
| Path | Architecture Path (ADR 0096) + Feature Path |

## Changes

- `Float[N][M]…` type + nested list literals (trailing commas allowed)
- Chained `a[i][j]…` OpIndexed parse + binder full-rank check
- Nested tensor collect/lookup in finite binder lowering

## Verification

`python3 tests/test_nd_float_coefficient_tensors_red.py` (+ 1D / honesty / where regression)
