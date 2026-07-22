# 06 — Statistical physics: 1D Ising

## Physics

Canonical ensemble for Ising spins $s_i\in\{+1,-1\}$:

\[
\rho(s) \propto e^{-\beta H(s)},\qquad
H = -J\sum_i s_i s_{i+1}
\]

Low $T$ (large $\beta$) concentrates mass on ordered configs.

This is **classical** statistical mechanics on a product measure — not a
quantum Bell / entanglement demo.

## QPex mapping

| Idea | Surface |
|------|---------|
| All microstates | product of `coin()` → spin $\pm 1$ |
| Energy / agreement | `when (s0 == s1) { … }` pushforward on the **joint** |
| Soft project to low-energy sector | `project` |
| Thermal observable | `inspect` / `measure` magnetization proxy |

Masses stay non-negative PMF weights — exactly the statistical-mechanics
setting of Discrete QPex.

**Anti-pattern:** nested `when (s0) { when (s1) … }` looks like sequential
collapse; prefer equality (or any function) evaluated on the joint assignment.

