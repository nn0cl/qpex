# 06 — Statistical / quantum Ising

| File | Physics |
|------|---------|
| `ising_model.qpex` | Classical product measure + `when` agreement — **not** entanglement |
| `quantum_ising.qpex` | Quantum $H=-J Z_0 Z_1 - h(X_0+X_1)$, $U=e^{-iHt}$ |

## Quantum Ising

\[
H = -J\,Z_0 Z_1 - h\,(X_0 + X_1),\qquad
|\psi(t)\rangle = e^{-i H t}|\psi(0)\rangle
\]

Coefficients may be Type-First `Float` scalars referenced inside `Operator`.

## QPex mapping

| Idea | Surface |
|------|---------|
| Hamiltonian | `Operator H_ising = -J * (Z(0)*Z(1)) - h * (X(0)+X(1))` |
| Joint evolve | `state (s0, s1) = evolve (s0, s1) under H_ising for t` |
| Correlator | `expect(ZZ, s0, s1)` (non-destructive) |

**Anti-pattern (classical file):** nested `when (s0) { when (s1) … }` — prefer joint predicates.
