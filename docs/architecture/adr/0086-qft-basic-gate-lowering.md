# ADR 0086: QFT lowering through the basic QPU opcode vocabulary

## Status

Accepted (2026-07-24) for the LISS-0042 Phase 1 Red/implementation slice.

Companion: [LISS-0042](../../issues/LISS-0042-qft-basic-gate-lowering.md).

## Decision

QFT and IQFT lowering must emit only the ADR 0085 basic QPU vocabulary:
`H`, `X`, `Y`, `Z`, `CX`, `RX`, `RY`, `RZ`, symbolic parameters, and terminal
`Measure`.

- Controlled phase rotations are fully decomposed into `CX` and `RZ` gates.
- Register bit reversal is fully decomposed into three `CX` gates per swap:
  `CX(a,b)`, `CX(b,a)`, `CX(a,b)`.
- No `CPHASE`, `CRZ`, or `SWAP` opcode is added to QPU IR.
- QFT/IQFT remain restricted to statically sized `QubitRegister<N>` values.
- The logical wire-order and QFT/IQFT provenance metadata are preserved.

## Consequences

The QPU IR remains provider-neutral and minimal. QFT lowering may produce more
gates, but the OpenQASM adapter and future basic-gate adapters do not need a
QFT-specific instruction family.

Deferred: approximate QFT, optimization, and hardware-specific
phase or swap instructions. Exact single-control `cqft`/`ciqft` is Accepted
under ADR 0120.
