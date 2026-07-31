# ADR 0120: Controlled exact QFT / IQFT (`cqft` / `ciqft`)

## Status

**Accepted** (2026-07-31) — unlocks LISS-0151 under WP-0036.
Companions: [ADR 0078](0078-kernel-qft-iqft-surface.md);
[ADR 0086](0086-qft-basic-gate-lowering.md); [ADR 0046](0046-multi-controlled-capply.md).

Does **not** accept approximate QFT (separate follow-up).

## Context

Exact `qft(reg)` / `iqft(reg)` and basic-gate lowering are shipped. ADR 0078
Decision 5 and ADR 0086 deferred controlled QFT. Multi-controlled `capply`
semantics exist, but QFT-as-controlled-unitary needs an explicit surface and
lowering contract.

## Decisions

### D1 — Surface

```staqex
Operator CF = cqft(ctrl, reg)
Operator CI = ciqft(ctrl, reg)
```

- `ctrl` is a single qubit wire (filled control `|1⟩`), typed as a qubit /
  register element already accepted by `capply`’s first control position, or a
  `QubitRegister<1>` / named qubit binding resolvable to one logical wire.
- `reg` is a statically typed `QubitRegister<N>` (same as ADR 0078).
- MVP is **one filled control**. Multi-ctrl `cqft` is deferred (reuse ADR 0046
  later).

### D2 — Meaning

`cqft(c, reg)` is the exact unitary that applies `qft(reg)` when the control
is `|1⟩` and identity on `reg` when the control is `|0⟩`. `ciqft` is the
exact inverse in the same sense.

Wire order on `reg` remains **logical** (ADR 0078). No silent truncation.

### D3 — Lowering

Lower to ADR 0085 / 0086 basic vocabulary only (`H`,`X`,`Y`,`Z`,`CX`,`RX`,
`RY`,`RZ`,`Measure`). No `CPHASE` / `CRZ` / `SWAP` / `CCX` opcodes.

Implementation strategy: expand exact `_qft_instructions(N)`, then lift each
gate under the outer control via basic-gate decompositions (controlled-H,
controlled-RZ, controlled-CX → Toffoli-free CX/H/RZ/RY decomposition).

Provenance `source` is `cqft` / `ciqft`; preserve `wire_order: logical`.

### D4 — Resources

`N + 1` logical qubits (register + control) must fit
`MVP_MAX_LOGICAL_QUBITS`. Excess → `QFT_RESOURCE_ERROR` (shared family with
`qft`).

Bad arity / non-register → `QFT_REGISTER_TYPE_ERROR` (message names cqft).

### D5 — Approximate QFT

**Out of this ADR.** No `approx_qft`, no dropping small phases, no ε/m
parameters. A future ADR must name honesty and error budgets explicitly.

## Consequences

- Typecheck accepts `cqft` / `ciqft`.
- QPU IR projects controlled expansions for `Operator … = cqft(…)`.
- Existing `qft` / `iqft` tests remain green.

## Deferred

Multi-controlled cqft; approximate QFT; SV dense matrix factory (optional
follow-up); open-control `ocqft`.
