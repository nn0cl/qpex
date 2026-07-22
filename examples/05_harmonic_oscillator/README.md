# 05 — Harmonic oscillator

Four honest surfaces:

| File | Physics |
|------|---------|
| `classical_oscillator.qpex` | Phase-space Euler on $(q,p)$ — classical |
| `quantum_oscillator.qpex` | Fock $H = N + \tfrac12$ — quantum |
| `xp_oscillator.qpex` | Fock $H = \tfrac12(P^2+Q^2)$ — quadratures |
| `grid_oscillator.qpex` | Position-grid $\psi(x)$, $H=\tfrac12(P_x^2+X_x^2)$ |

## Quantum HO (Fock)

\[
H = N + \tfrac12
\quad\text{or}\quad
H = \tfrac12(P^2 + Q^2)
\]

## Quantum HO (position grid)

\[
H = \tfrac12(P_x^2 + X_x^2),\qquad
\psi(x,t)=e^{-iHt}\psi(x,0)
\]

on a truncated uniform abscissa (ℏ = m = ω = 1). Prep via `wavepacket`.

## QPex mapping

| Idea | Surface |
|------|---------|
| Fock number H | `Operator H = N + 0.5` |
| Fock $Q,P$ | `Operator H = 0.5 * (P * P + Q * Q)` |
| Grid $X,P$ | `Operator H = 0.5 * (P * P + X * X)` (Position context) |
| Grid prep | `wavepacket(xmin, xmax, n, x0, sigma)` |
| Evolve | `evolve psi under H for t` |

**Rejected:** classical Boolean `!psi` as Pauli-$X$ sugar — use `apply(X, …)`.
