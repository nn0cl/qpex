# ADR 0048: Mixed open/filled control polarities (`!c`)

## Status

Accepted (2026-07-23).

Companions: ADR 0046–0047. Verification: **SV-26**.

## Context

Uniform filled (`capply`) and uniform open (`ocapply`) do not cover gates with
both ● and ○ controls on different wires.

## Decision

### Surface

```qpex
state t = capply(a, !b, X, t)   // fire iff a=|1⟩ and b=|0⟩
state t = capply(!a, !b, X, t)  // ≡ ocapply(a, b, X, t)
```

Lexer token `!` (BANG), distinct from `!=`. AST `UnaryNot` marks open
polarity on a control wire only (inside `capply` / `ocapply` arg lists).

Active mask is MSB-first over control polarities (1=filled, 0=open).

## Consequences

Positive: arbitrary ○/● patterns in one gate.
Negative: `!` outside control position is not a general Boolean operator yet.

## Verification

SV-26 — mixed fire/idle, `!!` ≡ `ocapply`, example file.
