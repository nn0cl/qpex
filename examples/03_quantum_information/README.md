# 03 — Quantum information: Bell / EPR

## Physics

Bell state

\[
|\Phi^+\rangle = \frac{1}{\sqrt{2}}\bigl(|00\rangle + |11\rangle\bigr)
\]

exhibits correlations that no local hidden-variable model can reproduce in
full CHSH form. Even at the correlation level, support lives only on
$\{(0,0),(1,1)\}$.

## QPex mapping

| Idea | Surface |
|------|---------|
| Shared randomness / entanglement seed | one `coin()` feeding both parties |
| Joint $(A,B)$ | correlated binds (same `bit`) |
| Alice/Bob settings | `when` / `project` on chosen bases |
| Read correlation | `inspect` joint marginals; `measure` |

CHSH inequality numerics for continuous settings need amplitude IR; this
sample locks the **EPR correlation structure** in the Joint store.
