# 01 — Classical mechanics: phase-space ensemble

## Physics

Classical Liouville picture: an ensemble of points $(x, p)$ on phase space
evolves under Hamilton’s equations. Even when each trajectory is deterministic,
the **distribution** $\rho(x,p)$ is a state.

\[
\dot x = \partial_p H,\qquad \dot p = -\partial_x H
\]

Euler step with explicit dimensions:

\[
x_{n+1} = x_n + \frac{\Delta t}{m}\, p_n,\qquad
p_{n+1} = p_n - (\Delta t\, k)\, x_n
\]

## QPex mapping (Type-First)

| Idea | Surface |
|------|---------|
| Time step as quantity | `Delta<Time> dt = 0.5.s` |
| Mass / stiffness | `Mass m = 1.0.kg`, `Stiffness k = 1.0.N_m` |
| Phase-space seeds | `State<Length> x0`, `State<Momentum> p0` |
| Correlated pushforward | `(x, p) = evolve (x0, p0) times 2 { … }` |

Dimensional analysis rejects `x + dt` at compile time
(`DIMENSION_MISMATCH_ERROR`, SV-15).
