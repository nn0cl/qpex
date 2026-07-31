# Trace: WP-0036 Host tensors + exact cqft

| Field | Value |
|---|---|
| Date | 2026-07-31 |
| Agent | Cursor Composer |
| Branch | `feature/wp-0036-host-tensor-cqft` |
| Issues | LISS-0150, LISS-0151 |
| ADRs | 0119, 0120 Accepted |

## Shipped

- Host `CoefficientTensor` + Kernel `Float[…] = host("…")` overlay merge
- Exact `cqft` / `ciqft` typecheck + basic-gate controlled lift

## Still out

Approximate QFT; multi-ctrl cqft; geometry/file Host adapters; permanent-out
(LISS-0132 not reopened).
