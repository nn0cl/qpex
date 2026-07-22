# 02 — Quantum basics: double slit

## Physics

Young’s experiment: amplitudes for path $A$ and path $B$ superpose on the
screen. Intensity follows

\[
I(x) \propto \bigl|\psi_A(x) + \psi_B(x)\bigr|^2
\]

Constructive / destructive interference is a property of **amplitudes**, not
of classical mixture of probabilities.

## QPex mapping (Discrete MVP)

| Idea | Surface |
|------|---------|
| Which-path superposition | `when (coin()) { 0 -> pathA, else -> pathB }` |
| Combine path contributions | `interfer(screenA, screenB)` |
| Look without collapse | `inspect` |
| Born sample of arrival bin | terminal `measure` |

Under stance (a) masses are non-negative; this sample encodes a **discrete
screen histogram** whose constructive peak is planted by design so the
control-flow (`when` / `interfer`) matches the textbook narrative. Full
complex phases land with the amplitude IR lift.
