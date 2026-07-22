# 03 — Quantum information: Bell / EPR

## Physics

Bell state

\[
|\Phi^+\rangle = \frac{1}{\sqrt{2}}\bigl(|00\rangle + |11\rangle\bigr)
\]

is prepared unitarily (Hadamard on control + CNOT), not by nesting classical
`when` branches on two bits. Correlation is the Pauli observable
$\langle Z\otimes Z\rangle=+1$ (non-destructive `expect`).

## QPex mapping

| Idea | Surface |
|------|---------|
| Control in superposition | `alice = \|+>` |
| Target ground | `bob = \|0>` |
| Entangling gate | `bob = cnot(alice, bob)` |
| Z–Z correlation | `expect(ZZ, alice, bob)` |
| Host view / terminal | `inspect` / `measure` |

**Anti-pattern:** `when (s0) { when (s1) { … } }` re-labels Born masses and
drops relative phases — that is classical agreement, not Bell correlation.

CHSH with rotated bases needs additional single-qubit unitaries; this sample
locks the EPR prep + $\langle ZZ\rangle$ contract.
