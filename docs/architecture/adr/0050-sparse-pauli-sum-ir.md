# ADR 0050: Sparse Pauli-sum IR for multi-qubit Schrödinger evolve

## Status

Accepted (2026-07-23).

Companions: ADR 0041 (Operator / dense `expm`). Verification: **SV-28**.

## Context

Dense $U=e^{-iHt}\in\mathbb{C}^{2^n\times 2^n}$ blocks modest multi-qubit
Ising / Heisenberg demos. Hamiltonians are already Pauli polynomials;
storing $\sum_k c_k P_k$ and applying the series to the state vector removes
the $4^n$ matrix.

## Decision

1. Compile qubit `Operator` AST → coalesced **sparse Pauli sum**
   (`PauliTerm(coeff, kinds)`).
2. Multi-qubit `evolve … under H for t` applies
   $|\psi'\rangle=\exp(-iHt)|\psi\rangle$ via Taylor + sparse matvec
   (no dense $U$).
3. Fock / `N`/`Q`/`P` remain dense truncated matrices (ADR 0041 / 0049).
4. Dense `compile_hamiltonian` retained for `apply` unitaries and small-n
   static Hermiticity checks.

## Consequences

Positive: 4+-qubit Pauli $H$ evolve is practical in the MVP kernel.
Negative: still $O(2^n)$ state vectors; symbolic / tensor-network IR later.

## Verification

SV-28 — sparse≡dense $H$, Taylor≡dense $U$ on $n=2$, 4-qubit example norm.
