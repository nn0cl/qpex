# ADR 0042: apply(U), hadamard, shift — true DTQW surface

## Status

Accepted (2026-07-23).

Companions: ADR 0041 (Operator / tensor). Verification: **SV-20**.

## Context

With Operator Hamiltonians and `*|*`, the remaining gap for coined quantum walks
is applying a unitary on a subsystem ($U\otimes I$) and a coin-controlled
position shift — not nested `when` and not `e^{-iHt}` for a one-shot Hadamard.

## Decision

### A. `apply(U, wire[, …])`

1. Apply a **unitary matrix** (not $\exp(-iHt)$) on listed qubit wires;
   identity on all other joint coordinates.
2. `U` may be:
   - a bound `Operator` name (compiled dense matrix),
   - built-in `Hadamard` / `H`,
   - Pauli `X`/`Y`/`Z`/`I` as gates.
3. Sugar: **`hadamard(w)`** ≡ `apply(Hadamard, w)`.

### B. `shift(coin, pos)`

DTQW conditional translation:

\[
|0\rangle|x\rangle \mapsto |0\rangle|x-1\rangle,\qquad
|1\rangle|x\rangle \mapsto |1\rangle|x+1\rangle
\]

Bind `state x = shift(c, x)` (coin unchanged).

### C. DTQW step

$U_{\mathrm{step}} = S\,(\mathrm{Coin}\otimes I)$:

```staqex
state c = apply(Coin, c)
state x = shift(c, x)
```

## Consequences

Positive: `dtqw.staqex` is an honest coined walk. Nested `when` remains banned.
Negative: no mid-circuit classical control; open-control / multi-ctrl deferred
(partially addressed by ADR 0043 `capply`).

## Verification

SV-20 — hadamard, apply(X), one- and two-step DTQW masses, example files.
