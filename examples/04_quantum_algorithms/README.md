# 04 — Grover search (amplitude / mass amplification)

## Physics

Grover iterates oracle + diffusion to amplify the marked basis:

\[
|\psi\rangle \mapsto W O |\psi\rangle
\]

Success probability rises to $\sim 1$ in $O(\sqrt{N})$ queries.

## QPex mapping

| Idea | Surface |
|------|---------|
| Uniform superposition over database | `when` / `coin` mixture over indices |
| Oracle marks target | `when` / `map` tagging |
| Diffusion / amplify | `interfer` + reweight via `when` |
| Track probabilities | `inspect` between rounds |

Discrete MVP replaces complex amplitude flips with **mass concentration** on
the marked index while keeping every step Joint→Joint.
