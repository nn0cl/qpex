# 05 — Harmonic oscillator / coherent-like orbit

## Physics

Coherent states of the quantum harmonic oscillator follow classical ellipses
in $(q,p)$ while remaining minimum-uncertainty packets:

\[
\langle q\rangle(t) = |\alpha|\sqrt{2}\,\cos(\omega t+\phi)
\]

## QPex mapping

| Idea | Surface |
|------|---------|
| Packet as ensemble | `when (coin())` mixture of nearby $q$ |
| Rotation in phase space | `Math.cos` / `Math.sin` pushforwards |
| Multi-step orbit | unrolled `evolve` via successive binds |
| Watch shape | `inspect` |

True $|\alpha\rangle$ Fock structure needs amplitude IR; this sample shows
**rigid rotation of a Discrete ensemble** under harmonic flow.
