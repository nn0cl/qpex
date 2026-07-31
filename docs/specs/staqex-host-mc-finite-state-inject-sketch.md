# Host Monte Carlo → finite State injection (design sketch)

| Field | Value |
|---|---|
| Status | **shipped MVP** under [ADR 0163](../architecture/adr/0163-host-mc-finite-state-inject.md) |
| Issue | [LISS-0195](../issues/LISS-0195-host-mc-finite-state-design.md) |
| Strategy | [ADR 0162](../architecture/adr/0162-continuous-host-bridge-first.md) (**Accepted**) |
| Boundary | [ADR 0126](../architecture/adr/0126-continuous-pdf-design-boundary.md) maintained |
| Discretization family | [ADR 0074](../architecture/adr/0074-explicit-discretization-contract.md) |
| Code | `compiler/staqex/host_monte_carlo.py` |

## Type gate

Continuous (Host) → explicit equal-width histogram finiteization → finite
`State` / Joint. No Kernel `Continuous` mid-program value.

## Locked MVP choices (ADR 0163)

- Approximation: `EqualWidthHistogram` only
- Labels: integer bin indices
- Host library port + `HostRngPort`; continuous draw callable supplied by Host
- `finite_inject_to_joint`: amp = √mass
- Fail closed on invalid spec / unsupported approximation / empty support

## Still deferred

Bridge sugar; KDE/adaptive bins; cloud MC SDK; Kernel continuous syntax.
