# 03 — Quantum information: Bell / controlled unitaries

## Physics

Bell state

\[
|\Phi^+\rangle = \frac{1}{\sqrt{2}}\bigl(|00\rangle + |11\rangle\bigr)
\]

is prepared unitarily (Hadamard on control + CNOT / `capply(_, X, _)`), not by
nesting classical `when` branches. Correlation is $\langle Z\otimes Z\rangle=+1$.

## Files

| File | Meaning |
|------|---------|
| `bell_state.qpex` | Φ⁺ via `cnot` + `expect(ZZ)` |
| `controlled_unitary.qpex` | `capply` — CX ≡ CNOT, CZ phase kick |

## QPex mapping

| Idea | Surface |
|------|---------|
| Entangling CX | `cnot(c,t)` or `capply(c, X, t)` |
| Controlled-Z | `capply(c, Z, t)` |
| Controlled arbitrary U | `capply(c, U, t)` (`Operator` / `Hadamard` / Pauli) |
| Z–Z correlation | `expect(ZZ, a, b)` |

**Anti-pattern:** nested `when` on two bits — classical agreement, not Bell.
