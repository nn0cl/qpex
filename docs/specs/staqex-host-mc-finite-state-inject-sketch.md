# Host Monte Carlo → finite State injection (design sketch)

| Field | Value |
|---|---|
| Status | **shipped** under [ADR 0163](../architecture/adr/0163-host-mc-finite-state-inject.md) + [ADR 0164](../architecture/adr/0164-host-mc-inject-consumption-seam.md) |
| Issue | [LISS-0195](../issues/LISS-0195-host-mc-finite-state-design.md) (complete); [LISS-0198](../issues/LISS-0198-host-mc-inject-consumption-seam.md) (complete) |
| Strategy | [ADR 0162](../architecture/adr/0162-continuous-host-bridge-first.md) (**Accepted**) |
| Boundary | [ADR 0126](../architecture/adr/0126-continuous-pdf-design-boundary.md) maintained |
| Discretization family | [ADR 0074](../architecture/adr/0074-explicit-discretization-contract.md) |
| Code | `compiler/staqex/host_monte_carlo.py` |
| Example | `examples/host/mc_finite_inject_demo.py` |
| Program | [WP-0068](../work-plans/WP-0068-host-mc-inject-seam.md) |

## Type gate

Continuous (Host) → explicit equal-width histogram finiteization → finite
`State` / Joint. No Kernel `Continuous` mid-program value.

## Locked MVP choices (ADR 0163)

- Approximation: `EqualWidthHistogram` only
- Labels: integer bin indices (default)
- Host library port + `HostRngPort`; continuous draw callable supplied by Host
- `finite_inject_to_joint`: amp = √mass
- Fail closed on invalid spec / unsupported approximation / empty support

## Locked seam choices (ADR 0164)

- Optional `label_mode`: `bin_index` | `bin_midpoint` | `explicit_labels`
- Nested `discretization` provenance aligned with ADR 0074 vocabulary
- `run_host_mc_inject` helper + `examples/host/` consumption demo

## Still deferred

Bridge sugar; KDE/adaptive bins; cloud MC SDK; Kernel continuous syntax.
