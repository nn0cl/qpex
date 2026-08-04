# Host Monte Carlo → finite State injection (design sketch)

| Field | Value |
|---|---|
| Status | **shipped** under [ADR 0163](../architecture/decision-themes/dec-0006-host-qpu-and-external-ports.md) + [ADR 0164](../architecture/decision-themes/dec-0006-host-qpu-and-external-ports.md) |
| Issue | [LISS-0195](../architecture/documentation-compression-map.md) (complete); [LISS-0198](../architecture/documentation-compression-map.md) (complete) |
| Strategy | [ADR 0162](../architecture/decision-themes/dec-0006-host-qpu-and-external-ports.md) (**Accepted**) |
| Boundary | [ADR 0126](../architecture/decision-themes/dec-0006-host-qpu-and-external-ports.md) maintained |
| Discretization family | [ADR 0074](../architecture/decision-themes/dec-0004-type-first-scientific-model.md) |
| Code | `compiler/staqex/host_monte_carlo.py` |
| Example | `examples/host/mc_finite_inject_demo.py` |
| Program | [WP-0068](../architecture/documentation-compression-map.md) |

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
