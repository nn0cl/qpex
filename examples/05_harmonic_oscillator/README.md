# 05 — Harmonic oscillator

Two honest surfaces:

| File | Physics |
|------|---------|
| `classical_oscillator.qpex` | Phase-space Euler on $(q,p)$ — classical |
| `quantum_oscillator.qpex` | Fock $H = N + \tfrac12$, $U=e^{-iHt}$ — quantum |

## Quantum HO

\[
H = N + \tfrac12,\qquad
|\psi(t)\rangle = e^{-iHt}|\psi(0)\rangle
\]

(ℏ = ω = 1). Truncated number basis; MVP uses dense `expm(-iHt)`.

## QPex mapping

| Idea | Surface |
|------|---------|
| Hamiltonian | Type-First `Operator H_osc = N + 0.5` |
| Time evolve | `evolve psi under H_osc for t` |
| Prep | `dirac(n)` Fock level |
| Watch | `inspect` / `measure` |
