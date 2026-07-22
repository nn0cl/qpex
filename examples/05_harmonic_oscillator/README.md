# 05 — Harmonic oscillator

Three honest surfaces:

| File | Physics |
|------|---------|
| `classical_oscillator.qpex` | Phase-space Euler on $(q,p)$ — classical |
| `quantum_oscillator.qpex` | Fock $H = N + \tfrac12$, $U=e^{-iHt}$ — quantum |
| `xp_oscillator.qpex` | Fock $H = \tfrac12(P^2+Q^2)$ — same HO via quadratures |

## Quantum HO

\[
H = N + \tfrac12
\quad\text{or}\quad
H = \tfrac12(P^2 + Q^2),\qquad
|\psi(t)\rangle = e^{-iHt}|\psi(0)\rangle
\]

(ℏ = m = ω = 1). Truncated number basis; MVP uses dense `expm(-iHt)`.
`Q`/`P` are Fock matrices for continuum quadratures (ADR 0049), not a
position grid.

## QPex mapping

| Idea | Surface |
|------|---------|
| Hamiltonian (number) | `Operator H_osc = N + 0.5` |
| Hamiltonian $(x,p)$ | `Operator H_xp = 0.5 * (P * P + Q * Q)` |
| Time evolve | `evolve psi under H for t` |
| Prep | `dirac(n)` Fock level |
| Watch | `inspect` / `measure` |
