# 06 — Statistical physics: 1D Ising

## Physics

Canonical ensemble for Ising spins $s_i\in\{+1,-1\}$:

\[
\rho(s) \propto e^{-\beta H(s)},\qquad
H = -J\sum_i s_i s_{i+1}
\]

Low $T$ (large $\beta$) concentrates mass on ordered configs.

## QPex mapping

| Idea | Surface |
|------|---------|
| All microstates | product of `coin()` → spin $\pm 1$ |
| Energy / Boltzmann tag | `when` / `map` on configs |
| Soft project to low-energy sector | `project` |
| Thermal observable | `inspect` / `measure` magnetization proxy |

Masses stay non-negative PMF weights — exactly the statistical-mechanics
setting of Discrete QPex.
