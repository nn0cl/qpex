# ADR 0164: Host MC inject consumption seam (labels + 0074 provenance)

## Status

**Accepted** (2026-07-31) — ship + Phase 1–3 authorized for LISS-0198 /
WP-0068
([review](../../collaboration/reviews/2026-07-31-adr-0164-host-mc-inject-seam.md)).
Extends [ADR 0163](0163-host-mc-finite-state-inject.md) under
[ADR 0162](0162-continuous-host-bridge-first.md). Companions:
[ADR 0074](0074-explicit-discretization-contract.md),
[ADR 0126](0126-continuous-pdf-design-boundary.md),
[LISS-0198](../../issues/LISS-0198-host-mc-inject-consumption-seam.md),
[WP-0068](../../work-plans/WP-0068-host-mc-inject-seam.md).

## Context

ADR 0163 shipped equal-width histogram → `FiniteStateInject` → Joint with
integer bin indices. Physicist DX still lacks (a) optional physical bin
labels, (b) provenance that speaks ADR 0074 discretization vocabulary, and
(c) a documented Host consumption path (draw → finiteize → Joint → measure).
Kernel `Continuous` remains deferred (0162); this ADR deepens Host only.

## Dependency Adoption Evidence

Not applicable — Host library and example only; no new provider SDK.

## Decision

1. **Default labels preserved.** `label_mode = "bin_index"` (default) keeps
   ADR 0163 integer atoms `0 .. n_bins-1`. Zero-count bins stay omitted.
2. **Optional label modes (fail-closed).** `MonteCarloSpec` gains
   `label_mode` with exactly these MVP values:
   - `bin_index` — integer bin indices (default).
   - `bin_midpoint` — atom label is the float midpoint of
     `[lo + i·w, lo + (i+1)·w)` for width `w = (hi-lo)/n_bins`.
   - `explicit_labels` — Host supplies `bin_labels` of length `n_bins`;
     each accepted bin `i` uses `bin_labels[i]`. Wrong length, missing
     sequence, or duplicate labels → `MONTE_CARLO_SPEC_INVALID`.
   Unsupported `label_mode` → `MONTE_CARLO_LABEL_MODE_UNSUPPORTED`.
3. **Atom type widening.** `FiniteStateInject.atoms` become
   `tuple[tuple[Any, float], ...]` where the label is `int | float |`
   Host-supplied hashable from `explicit_labels`. Masses remain normalized
   Σ = 1; `finite_inject_to_joint` still uses `amp = √mass`.
4. **ADR 0074-aligned provenance block.** Every successful inject must
   include a nested `discretization` map with at least:
   - `domain` ← `domain_label`
   - `basis` ← `"EqualWidthHistogram"`
   - `resolution` ← `n_bins`
   - `boundary` ← `{ "interval": [lo, hi], "convention": "half_open_right" }`
   - `approximation` ← spec approximation string
   - `error_bound` ← `"Unbounded"` unless Host sets a declared/empirical
     bound in `spec.provenance["error_bound"]`
   - `label_mode` ← chosen mode
   Top-level ADR 0163 keys (`domain_label`, `interval`, `n_bins`, …) remain
   for compatibility; they must not contradict the `discretization` block.
5. **Consumption seam (Host only).** Ship:
   - a small helper `run_host_mc_inject(...)` (or equivalent) that wires
     `HostRngPort` + `continuous_draw` + `EqualWidthHistogramMonteCarlo` +
     `finite_inject_to_joint` and returns `(FiniteStateInject, Joint)`;
   - one runnable Host example under `examples/host/` demonstrating
     continuous draw → finiteize → Joint Born masses (no Kernel
     `Continuous` syntax; may call Kernel measure on the finite Joint only).
6. **Type gate unchanged.** No Kernel mid-program `Continuous`; no Bridge
   sugar; no `monte_carlo(...)` Kernel syntax; no cloud/HPC MC SDK.

## Non-goals

Adaptive/KDE bins; multi-dimensional histograms; Bridge `discretization`
syntax; Kernel continuous values; provider technology selection.

## Consequences

Positive:

- Host finiteization becomes physicist-readable (midpoints / explicit labels)
  while keeping the reversible Host-first path (0162).
- MC inject provenance shares vocabulary with ADR 0074 Bridge contracts.

Negative:

- Atom labels are no longer always `int`; callers must tolerate widened types.
- Example + helper add a thin Host surface to maintain.

## Enforcement

Code review should reject:

- Kernel continuous syntax under this ADR.
- Silent default change away from `bin_index` without an explicit
  `label_mode`.
- Provenance that omits the `discretization` block or contradicts it.
- Adaptive/KDE or cloud MC SDK selection without a separate ADR.
