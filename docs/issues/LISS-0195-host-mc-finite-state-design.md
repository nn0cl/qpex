# LISS-0195: Host Monte Carlo → finite State injection

## Metadata

- Local issue ID: LISS-0195
- Status: **complete**
- ADR boundary: [0126](../architecture/adr/0126-continuous-pdf-design-boundary.md) **maintained**
- Strategy: [ADR 0162](../architecture/adr/0162-continuous-host-bridge-first.md) **Accepted**
- Ship ADR: [0163](../architecture/adr/0163-host-mc-finite-state-inject.md) **Accepted**
- Program: [WP-0067](../work-plans/WP-0067-host-mc-finite-inject.md)
- Sketch: [`staqex-host-mc-finite-state-inject-sketch.md`](../specs/staqex-host-mc-finite-state-inject-sketch.md)
- Tests: `tests/test_host_mc_finite_state_red.py`
- Code: `compiler/staqex/host_monte_carlo.py`

## Exit

- [x] Ship ADR 0163 Accepted (Adjudicator: ship + Red→Green authorized)
- [x] Host equal-width histogram port + fail-closed diagnostics
- [x] Integer bin labels; normalized masses; `finite_inject_to_joint` (amp=√mass)
- [x] No Kernel `Continuous` syntax
- [x] Red suite green

## Non-goals (still out)

Kernel `Continuous`; Bridge sugar; cloud MC SDK; adaptive/KDE bins.
