# Trace: WP-0035 Basis binder / partial Float

| Field | Value |
|---|---|
| Date | 2026-07-31 |
| Agent | Cursor Composer |
| Branch | `feature/wp-0035-basis-and-partial-float` |
| Issues | LISS-0148, LISS-0149 |
| ADR | 0118 Accepted |

## Shipped

- `Basis<N>` / `rev(Basis<N>)` binder expansion (computational-basis labels)
- Classical partial Float bind `Float[M…] row = h[i]` + alias lookup in binders

## Still deferred

Host/Param tensors; non-literal partial indices; EnergyLevel/Bit/SpinProjection
domains; cQFT; permanent-out.
