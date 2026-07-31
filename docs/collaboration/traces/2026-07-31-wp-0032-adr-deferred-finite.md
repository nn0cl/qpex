# Trace: WP-0032 ADR deferred finite slices

| Field | Value |
|---|---|
| Date | 2026-07-31 |
| Agent | Cursor Composer |
| Branch | `feature/wp-0032-adr-deferred-finite` |
| Issues | LISS-0140 … LISS-0143 |
| Path | Architecture Path (ADR amendments) + Feature Path Red→Green |

## What changed

- Honesty: non-`Index` binder domains and unbound `J[i]` → hard diagnostics
- Compound `where &&` (binder-only; F-01 carve-out)
- Suzuki S4 product formula + order-4 step contract (ADR 0084)
- 1D `Float[N]` + binder `J[i]` lowering (ADR 0096 promotion)

## Verification

- `tests/test_binder_honesty_red.py`
- `tests/test_binder_compound_where_red.py`
- `tests/test_higher_order_suzuki_red.py`
- `tests/test_indexed_coefficient_family_red.py`
- Plus mathematical/finite binder regression (pass)

## Out of scope (unchanged)

`rev`/dependent ranges, Basis expansion, 2D coeffs, controlled/approx QFT,
permanent-out topics.
