# ADR 0163: Host Monte Carlo → finite State inject MVP

## Status

**Accepted** (2026-07-31) — unlocks LISS-0195 Feature Path under WP-0067.
Ship ADR under [ADR 0162](0162-continuous-host-bridge-first.md) /
[ADR 0126](0126-continuous-pdf-design-boundary.md).
Companions: [ADR 0074](0074-explicit-discretization-contract.md);
sketch [`staqex-host-mc-finite-state-inject-sketch.md`](../../specs/staqex-host-mc-finite-state-inject-sketch.md).

## Context

Adjudicator authorized ship + Red→Green for Host Monte Carlo finiteization
(2026-07-31). Continuous carriers remain outside Kernel mid-program values;
the programmer supplies interval/resolution and a continuous draw callable.

## Decisions

1. **Host library port only (MVP).** Ship `HostMonteCarloPort` +
   `EqualWidthHistogramMonteCarlo` in `compiler/staqex/host_monte_carlo.py`.
   No Kernel `Continuous` type, no `monte_carlo(…)` syntax, no `host("…")`
   wiring in this ADR.
2. **Finiteization mode.** `approximation = "EqualWidthHistogram"` only.
   Interval `[lo, hi)`, `n_bins ≥ 1`, `n_samples ≥ 1` required. Missing or
   invalid fields → fail closed (`MonteCarloInjectError`).
3. **Labels.** Atom labels are **integer bin indices** `0 .. n_bins-1`.
   Zero-count bins are omitted from the support.
4. **Masses.** Counts / accepted samples, normalized so Σ mass = 1.
   Samples outside `[lo, hi)` are rejected (counted in provenance); if zero
   samples are accepted → fail closed.
5. **RNG.** Host sampling uses an injected `HostRngPort` (`random() → [0,1)`).
   This is not Kernel terminal `measure` entropy.
6. **Continuous draw.** Host supplies `Callable[[HostRngPort], float]` (the
   continuous sampler). The port never invents a PDF.
7. **Kernel intake helper.** `finite_inject_to_joint(inject) → Joint` builds
   worlds with `amp = √mass` on the inject coordinate. Ordinary finite `State`
   semantics thereafter.
8. **Provenance.** Inject provenance must record domain, interval, n_bins,
   n_samples, approximation, seed (if any), n_accepted, n_rejected, and a
   statement that the support is a finite approximation.

## Non-goals

Kernel `Continuous`; Bridge sugar; adaptive/KDE bins; cloud/HPC MC SDK;
QPU of raw continuous samples.

## Consequences

- LISS-0195 may proceed Red→Green→Refactor on this MVP.
- Agents must not add Kernel continuous syntax under this ADR.
