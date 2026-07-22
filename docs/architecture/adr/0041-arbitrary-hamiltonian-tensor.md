# ADR 0041: Arbitrary Operator Hamiltonians, tensor product, partial trace

## Status

Accepted (2026-07-23).

Companions: ADR 0038 (ket / Pauli evolve / expect). Verification: **SV-19**.

## Context

After physical-axiom gates (ADR 0039–0040) reject dishonest patterns, theorists
need blackboard vocabulary for $H$ beyond bare Pauli names, product spaces
$\mathcal{H}_A\otimes\mathcal{H}_B$, and $U=e^{-iHt}$ on those spaces.

## Decision

### A. Type-First `Operator`

```qpex
Operator H_osc = N + 0.5
Float J = 1.0
Operator H_ising = -J * (Z(0) * Z(1)) - h * (X(0) + X(1))
```

1. Operator polynomials: Pauli `I|X|Y|Z` (optional site `Z(i)`), Fock `N`,
   scalars / Type-First `Float` coeffs, `+ - *`, integer power `^`.
2. `evolve psi under H for t` (ℏ = 1) builds dense $U=\exp(-iHt)$ and applies
   it to qubit wires or truncated Fock levels.
3. Bare `X|Y|Z|I` remain as ADR 0038 shortcuts.

### B. Tensor product surface

`(a, b) = left *|* right` — product of independent preps, or relabel of two
existing joint coordinates. Precedence: above `*`/`/`, below unary `-`.

### C. `trace_out(coord)`

Prelude combinator: Born partial trace over `coord`; reduced amplitudes are
$\sqrt{p}$ (diagonal of $\rho$). Non-destructive w.r.t. remaining wires.

## Consequences

Positive: quantum HO / Ising examples become honest $e^{-iHt}$ surfaces.
Negative: dense matrices only (MVP); continuous $x,p$ HO still Open.
DTQW / `apply` shipped in ADR 0042.

## Verification

SV-19 — unitarity of `expm`, Fock/Ising evolve norms, tensor+trace_out,
example files `quantum_oscillator.qpex` / `quantum_ising.qpex`.
