# ADR 0043: capply — general controlled unitaries

## Status

Accepted (2026-07-23).

Companions: ADR 0042 (`apply` / `shift`), ADR 0038 (`cnot`). Verification: **SV-21**.

## Context

`cnot` and DTQW `shift` are special cases of controlled unitaries. Theorists need
blackboard `capply(ctrl, U, tgt)` for CZ, controlled-Hadamard, and Operator
targets — without nested `when`.

## Decision

### Surface

```qpex
state t = capply(c, X, t)         // ≡ cnot(c, t)
state t = capply(c, Z, t)         // CZ
state t = capply(c, Hadamard, t)
state t = capply(c, U, t)         // Operator U
```

Semantics: $C(U)=|0\rangle\langle 0|\otimes I + |1\rangle\langle 1|\otimes U$
with control as MSB on the joint wires `[ctrl, tgt…]`. Multi-target:
`capply(c, U, t0, t1)` when `U` is a 2-qubit Operator.

`cnot` remains sugar / prelude for CX.

## Consequences

Positive: Bell / phase-kick / controlled gates share one combinator.
Negative: no mid-circuit classical control; open-control / multi-ctrl deferred.

## Verification

SV-21 — CX≡cnot, CZ phase on |11⟩, ctrl=0 identity, example file.
