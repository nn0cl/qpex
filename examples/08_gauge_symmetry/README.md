# 08 — Gauge symmetry (U(1) pedagogy)

## Honesty

| Claim | Status |
|-------|--------|
| Quantum Fourier Transform (QFT) | **No** — use a future dedicated example if Kernel `qft` lands |
| Local U(1) phase invariance | **Yes** — `phase` + Born-mass invariant |

Formerly numbered under a misleading `*_qft_*` folder name; renamed to
`08_gauge_symmetry` (LISS-0006).

## Physics

Local U(1) rotation $\psi(x)\mapsto e^{i\alpha(x)}\psi(x)$ leaves
gauge-invariant observables unchanged. Occupation / Born mass on site is the
simplest invariant.

## QPex mapping

| Idea | Surface |
|------|---------|
| Matter amplitude | Discrete site occupation `State` |
| Local phase rotation | `phase(site, α)` / `phase(site, pi)` |
| Invariant observable | site id via `project`+`measure` |
| Compare before/after | same support after gauge |

Do **not** fake phases with classical `when` label remaps.

## Run

```bash
python3 -m compiler.qpex run examples/08_gauge_symmetry/gauge_symmetry.qpex --seed 0
```
