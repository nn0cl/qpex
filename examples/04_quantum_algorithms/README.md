# 04 — Grover search (amplitude amplification)

## Physics

Grover iterates oracle + diffusion to amplify the marked basis:

\[
|\psi\rangle \mapsto W O |\psi\rangle
\]

Success probability rises to \(\sim 1\) in \(O(\sqrt{N})\) queries.

## QPex mapping

| Idea | Surface |
|------|---------|
| Uniform superposition over database | `coin` / joint index |
| Oracle phase flip on target | `phase(idx, π, target)` |
| Diffusion (invert about mean) | `grover_diffuse` / `diffuse` |
| Track amplitudes / Born | `inspect` between rounds |

For \(N=4\), one round yields the pure target (SV-14).

## Related

Shor / RSA **toy** (period finding) lives in
[`examples/11_shor_rsa_toy/`](../11_shor_rsa_toy/).

## Run

```bash
python3 -m compiler.qpex run examples/04_quantum_algorithms/grover_search.qpex --seed 0
```
