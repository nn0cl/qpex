# ADR 0049: Fock-basis position/momentum operators (`Q`, `P`)

## Status

Accepted (2026-07-23).

Companions: ADR 0041 (Operator / Fock `N`). Verification: **SV-27**.

## Context

ADR 0041 ships the quantum HO as $H=N+\tfrac12$ on truncated Fock levels.
Blackboard language often writes the same oscillator as
$H=\tfrac12(P^2+Q^2)$ with continuous quadratures $Q,P$. A full continuum
grid is still Open; the Fock matrix representation is the honest MVP bridge.

## Decision

### Surface

```staqex
Operator H_xp = 0.5 * (P * P + Q * Q)
state psi = evolve psi under H_xp for 1.0
```

Atoms `Q` and `P` inside Type-First `Operator` polynomials compile to the
standard truncated Fock matrices (ℏ = m = ω = 1):

$$
Q=\frac{a+a^\dagger}{\sqrt2},\qquad
P=\frac{-i(a-a^\dagger)}{\sqrt2}.
$$

They select Fock mode (same as `N`); mixing with site-indexed Pauli remains
illegal.

## Consequences

Positive: $x,p$ HO vocabulary without leaving the truncated-state kernel.
Negative: continuum / open-boundary HO still Open beyond truncated grid
(ADR 0051); truncation edge makes
$\tfrac12(P^2+Q^2)\neq N+\tfrac12$ exactly (ground energy still $\tfrac12$).

## Verification

SV-27 — Hermitian $H$, $E_0=\tfrac12$, evolve $|0\rangle$ under $H_{xp}$,
example `xp_oscillator.staqex`.
