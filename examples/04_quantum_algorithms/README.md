# 04 — Grover search (amplitude amplification)

## Physics

Grover iterates oracle + diffusion to amplify the marked basis:

\[
|\psi\rangle \mapsto W O |\psi\rangle
\]

Success probability rises to $\sim 1$ in $O(\sqrt{N})$ queries.

## QPex mapping

| Idea | Surface |
|------|---------|
| Uniform superposition over database | `coin` / `when` over indices |
| Oracle phase flip on target | `phase(idx, π, target)` |
| Diffusion (invert about mean) | `diffuse(marked)` |
| Track amplitudes / Born | `inspect` between rounds |

Complex IR: marking multiplies the target amplitude by $e^{i\pi}=-1$;
`diffuse` applies $c\mapsto 2\mu-c$ on the amplitude marginal. For $N=4$,
one round yields the pure target (SV-14).
