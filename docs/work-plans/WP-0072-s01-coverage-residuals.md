# WP-0072: S01 coverage residuals (Joint NYI + shipped-surface wiring)

| Field | Value |
|---|---|
| Status | **proposed** (2026-08-01) — intake only; not approved for execution |
| Branch | `docs/wp-0072-s01-coverage-residuals` |
| Discovery | WP-0071 re-check shake; [scorecard](../specs/staqex-v1-s01-coverage-scorecard.md) residuals |

## Issues

| ID | Title | Kind | Status |
|---|---|---|---|
| [LISS-0228](../issues/LISS-0228-joint-apply-qft-runtime.md) | Joint `apply(qft/iqft/cqft, …)` runtime | Kernel | **proposed** |
| [LISS-0229](../issues/LISS-0229-inner-outer-joint-runtime-call.md) | `inner`/`outer` Joint runtime Call | Kernel | **proposed** |
| [LISS-0230](../issues/LISS-0230-s01-wire-shipped-surfaces.md) | S01 wire Basis / Trace-Out / Algebraic Fusion / Rankine·troy | Sample | **proposed** |
| [LISS-0231](../issues/LISS-0231-s01-impl-interface-dispatch.md) | S01 `impl` interface-mediated dispatch | Sample | **proposed** |
| [LISS-0232](../issues/LISS-0232-s01-index-lattice-beyond-two-wires.md) | S01 Index lattice beyond 2-wire toy | Sample | **proposed** |

## Order (recommended)

1. LISS-0228 / LISS-0229 (Kernel gates for honest QFT / Dirac runtime claims)
2. LISS-0232 (wider Index — may couple to register size / evolve)
3. LISS-0230 then LISS-0231 (showcase wiring of already-shipped Kernel)

## Out

- Live QPU SDK, Continuous Kernel, trait specialization, CUDA
- Architecture approval / Phase approval — Adjudicator must approve separately

## Verification (after execution approval)

Per-Issue Red tests + S01 mains seed 0; update coverage scorecard evidence paths.
