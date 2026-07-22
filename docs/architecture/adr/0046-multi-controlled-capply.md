# ADR 0046: Multi-controlled capply / toffoli

## Status

Accepted (2026-07-23).

Companions: ADR 0043 (single-ctrl `capply`). Verification: **SV-24**.

## Context

Single-ctrl `capply(c, U, t)` covers CX/CZ. Theorists also need Toffoli / CCZ /
$C^n(U)$ without nested classical control.

## Decision

### Surface

```qpex
state t = capply(c0, c1, X, t)     // CCX / Toffoli
state t = toffoli(c0, c1, t)       // sugar
state t = capply(c0, c1, Z, t)     // CCZ
state t = capply(c0, c1, c2, U, t) // three controls
```

Argument split: the unique Operator/gate name (`X`/`Hadamard`/bound `Operator`)
sits between control wires and target wires.

Semantics: apply $U$ on targets iff **all** controls are $|1\rangle$; otherwise
identity. Controls are MSBs in the joint computational basis.

## Consequences

Positive: Toffoli and multi-ctrl phase kick share one combinator.
Negative: mixed open/filled polarities and mid-circuit classical multi-ctrl
remain Deferred. Open (uniform $|0\rangle$) control shipped in ADR 0047.
Gate-named state variables shadow poorly — avoid naming qubits `X`/`Z`.

## Verification

SV-24 — CCX flip, idle when ctrls≠11, single-ctrl compat, `toffoli.qpex`.
