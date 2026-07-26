# 06 — Statistical / quantum Ising

| File | Physics |
|------|---------|
| `ising_model.qpex` | Transverse-field quantum Ising $H=-J Z_0Z_1-h(X_0+X_1)$, $U=e^{-iHt}$ |
| `quantum_ising.qpex` | Same TFIM surface (companion / correlator focus) |
| `quantum_ising_4.qpex` | 4-site ZZ ring via sparse Pauli-sum evolve (ADR 0050) |

Classical coin/`when`/`project` Ising pedagogy was **removed** (ADR 0053):
filters are not Hilbert projectors.

## Quantum TFIM

\[
H = -J\,Z_0 Z_1 - h\,(X_0 + X_1),\qquad
|\psi(t)\rangle = e^{-i H t}|\psi(0)\rangle
\]

## QPex mapping

| Idea | Surface |
|------|---------|
| Hamiltonian | `Operator H_tfim = -J * (Z[0]*Z[1]) - h * (X[0]+X[1])` |
| Joint evolve | `state (s0, s1) = evolve (s0, s1) under H_tfim for t` |
| Correlator | `expect(ZZ, s0, s1)` (classical scalar — do not `measure`) |
