# 02 — Quantum basics: double slit

## Physics

Young’s experiment: amplitudes for path $A$ and path $B$ superpose on the
screen. Intensity follows

\[
I(x) \propto \bigl|\psi_A(x) + \psi_B(x)\bigr|^2
\]

Constructive / destructive interference is a property of **amplitudes**, not
of classical mixture of probabilities.

## QPex mapping

| Idea | Surface |
|------|---------|
| Which-path superposition | `when (slit) { … }` |
| Path-B phase $e^{i\pi}$ | `phase(screenB0, π)` |
| Path interference $\lvert A+B\rvert^2$ | `interfer(screenA, screenB)` |
| Look without collapse | `inspect` |
| Born sample of arrival bin | terminal `measure` |

Shared screen bin 1 receives opposite phases and **cancels spontaneously**
(SV-14). Outer bins keep Born mass $1/2$ each.
