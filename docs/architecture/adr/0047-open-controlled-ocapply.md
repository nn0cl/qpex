# ADR 0047: Open-controlled ocapply (U on |0…0⟩)

## Status

Accepted (2026-07-23).

Companions: ADR 0046 (filled multi-ctrl). Verification: **SV-25**.

## Context

Circuit diagrams distinguish filled (● / $|1\rangle$) and open (○ / $|0\rangle$)
controls. ADR 0046 covered filled $C^n(U)$; open control was still Deferred.

## Decision

### Surface

```qpex
state t = ocapply(c, X, t)          // open CX
state t = ocapply(c0, c1, Z, t)     // both open
```

Same argument split as `capply`: Operator/gate name between controls and
targets. Semantics: apply $U$ iff **all** controls are $|0\rangle$; else $I$.

`capply` remains filled ($|1\rangle^{\otimes n}$).

## Consequences

Positive: open/filled control pair matches blackboard / QASM intuition.
Negative: mixed polarities per wire (`●` and `○` together) deferred.

## Verification

SV-25 — open-X on $|00\rangle$, idle on $|10\rangle$, dual-open, example file.
