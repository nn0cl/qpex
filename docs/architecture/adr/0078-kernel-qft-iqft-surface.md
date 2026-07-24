# ADR 0078: Register-typed Kernel QFT and IQFT surface

## Status

Accepted (2026-07-24). This ADR accepts the small exact QFT/IQFT boundary only;
it does not authorize implementation or an official example yet.

Companions: [LISS-0010](../../issues/LISS-0010-kernel-qft-surface.md),
ADR 0069 (Static Hilbert Kernel), and ADR 0077 (provider-neutral QPU IR).

## Decision

1. The MVP QFT and IQFT operate only on a statically typed
   `QubitRegister<N>`.
2. QFT is the exact unitary discrete Fourier transform on the register Hilbert
   space; IQFT is its exact mathematical inverse.
3. The surface is an operator-valued call: `qft(reg)` / `iqft(reg)`. A later
   acceptance slice may define the final application spelling, but it must not
   turn QFT into a runtime integer loop or provider-specific instruction.
4. Logical register order is the Fourier wire-order convention. Any reversed
   output convention must be an explicit future surface choice, never an
   implicit backend transformation.
5. Controlled-QFT, approximate QFT, arbitrary dynamic registers, and
   provider-specific QFT instructions are excluded from this MVP.
6. Lowering must preserve the source QFT/IQFT identity and wire-order
   metadata through the provider-neutral QPU IR. Unsupported register sizes or
   target resource budgets are hard diagnostics; no truncation is allowed.
7. No official QFT example is added until Kernel semantics and SV coverage are
   accepted. Existing examples must continue to state honestly that QFT is
   deferred.

## Consequences

Positive:

- QFT is grounded in the static Hilbert-space model rather than a classical
  `Int` register API.
- IQFT correctness and wire order are testable independently of a provider.
- A later gate decomposition can target the existing QPU IR without changing
  source semantics.

Deferred:

- final call/application grammar;
- decomposition opcode contract and resource accounting;
- controlled/approximate QFT;
- a dedicated educational example.

## Enforcement

- Reject non-register or runtime-sized QFT inputs before lowering.
- Preserve QFT/IQFT provenance and wire order in lowering metadata.
- Never label a phase or pedagogical stand-in as QFT.
