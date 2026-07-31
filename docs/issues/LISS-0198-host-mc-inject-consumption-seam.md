# LISS-0198: Host MC inject consumption seam

## Metadata

- Local issue ID: LISS-0198
- Status: **complete**
- Type: Feature Path (Host library + example)
- Priority: medium
- Planning size: S
- ADR: [0164](../architecture/adr/0164-host-mc-inject-consumption-seam.md) (**Accepted**)
- Strategy: [ADR 0162](../architecture/adr/0162-continuous-host-bridge-first.md)
- Parent MVP: [ADR 0163](../architecture/adr/0163-host-mc-finite-state-inject.md) / [LISS-0195](LISS-0195-host-mc-finite-state-design.md)
- Program: [WP-0068](../work-plans/WP-0068-host-mc-inject-seam.md)
- Sketch: [`staqex-host-mc-finite-state-inject-sketch.md`](../specs/staqex-host-mc-finite-state-inject-sketch.md)
- Tests: `tests/test_host_mc_inject_seam_red.py`
- Code: `compiler/staqex/host_monte_carlo.py`
- Example: `examples/host/mc_finite_inject_demo.py`

## Goal

Deepen Host Monte Carlo finiteization consumption without Kernel `Continuous`:

1. Optional `label_mode`: `bin_index` (default) | `bin_midpoint` | `explicit_labels`
2. ADR 0074-aligned nested `discretization` provenance
3. Host helper + runnable `examples/host/` demo (draw → finiteize → Joint)

## Exit (after ADR Accepted + ship/phase approval)

- [x] ADR 0164 Accepted as ship
- [x] Red suite for label modes + provenance + helper
- [x] Green on `host_monte_carlo.py` + example
- [x] No Kernel continuous syntax
- [x] Living docs / CLAUDE Open Topics updated

## Non-goals

Kernel `Continuous`; Bridge sugar; adaptive/KDE; cloud MC SDK.
