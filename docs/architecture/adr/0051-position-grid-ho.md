# ADR 0051: Position-grid quantum HO (`Xx`, `Px`, `wavepacket`)

## Status

Accepted (2026-07-23).

Companions: ADR 0049 (Fock `Q`/`P`), ADR 0041. Verification: **SV-29**.

**Non-goal (explicit):** general Boolean `!` on states / `State<Bool>` sugar
for Pauli $X$. Control-polarity `!c` (ADR 0048) remains; classical-style
`!psi` is Rejected to keep the surface on blackboard operators.

## Context

Fock `N` / `Q` / `P` are number-basis truncations. Theorists also evolve
wavefunctions $\psi(x)$ on a real-line grid under
$H=\tfrac12(P^2+X^2)$ (ℏ = m = ω = 1).

## Decision

### Surface

```qpex
state psi = wavepacket(-6.0, 6.0, 48, 0.0, 0.7071067811865476)
Operator H = 0.5 * (Px * Px + Xx * Xx)
state psi = evolve psi under H for 1.0
measure psi
```

1. `wavepacket(xmin, xmax, n, x0, sigma)` — prelude prep; Born weights on
   Float grid abscissae $x_i$ (discrete MVP of $L^2(\mathbb{R})$).
2. Operator atoms `Xx`, `Px` (names distinct from Pauli `X` and Fock `Q`/`P`):
   - $X_x=\mathrm{diag}(x_i)$
   - $P_x$ = Hermitian central-difference $-i\partial_x$ (periodic)
3. `evolve` under an `Xx`/`Px` polynomial uses the dense grid $H$ on those
   abscissae (same Schrödinger path as Fock, different carrier).

Mixing grid atoms with Fock `N`/`Q`/`P` or site Pauli in one $H$ is illegal.

## Consequences

Positive: honest $\psi(x)$ HO demos without classical Boolean sugar.
Negative: finite grid + periodic $P_x$; true continuum / open BC still Open.

## Verification

SV-29 — Hermitian $H$, norm preservation, short-time Gaussian stability,
example `grid_oscillator.qpex`.
