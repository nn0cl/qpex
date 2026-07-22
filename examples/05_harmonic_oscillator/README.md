# 05 — Classical harmonic oscillator (phase-space Euler)

## Physics

Linearized harmonic oscillator on $(q,p)$:

\[
(q,p)\;\mapsto\;\bigl(q + \tfrac{\Delta t}{m}p,\;
p - (\Delta t\,k)\,q\bigr)
\]

This sample is **classical** statistical mechanics / symplectic Euler — not
Fock-space quantum HO ($e^{-iHt}$). Naming the file `classical_*` is intentional
(ADR / physical-soundness audit 2026-07-23).

## QPex mapping

| Idea | Surface |
|------|---------|
| Quantities | Type-First `Delta<Time>`, `Mass`, `Stiffness` |
| Ensemble | `when (coin())` mixture of nearby $q$ |
| Flow | correlated `evolve` pushforward |
| Watch | `inspect` / `measure` |
