# 01 — Classical mechanics: phase-space ensemble

## Physics

Classical Liouville picture: an ensemble of points $(x, p)$ on phase space
evolves under Hamilton’s equations. Even when each trajectory is deterministic,
the **distribution** $\rho(x,p)$ is a state.

\[
\dot x = \partial_p H,\qquad \dot p = -\partial_x H
\]

Euler step (pedagogical):

\[
x_{n+1} = x_n + \Delta t\, p_n,\qquad
p_{n+1} = p_n - \Delta t\, \partial_x V(x_n)
\]

## QPex mapping

| Formula | Surface |
|---------|---------|
| Ensemble $\rho$ | `State` / joint coords `x`, `p` |
| Uncertain initial data | `when (coin()) { … }` mixture |
| One Euler step on all worlds | `map` pushforward (unrolled `evolve`) |
| Read distribution | `inspect` / terminal `measure` |

Never extracts a mid-program scalar island: every update is Joint→Joint.
