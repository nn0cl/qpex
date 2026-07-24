# LISS-0042: QFT/IQFT basic-gate lowering

## Metadata

- Local issue ID: LISS-0042
- GitHub issue: none
- Status: **Phase 3 reviewed**
- Phase: Feature Path — Phase 3 Refactor complete
- Type: QPU lowering
- Priority: P2
- Initial planning size: M
- Current planning size: M
- Depends on: LISS-0010, LISS-0019, LISS-0041, ADR 0078, ADR 0085, ADR 0086

## Summary

Lower exact register-typed QFT and IQFT calls into the provider-neutral basic
QPU opcode vocabulary without introducing `CPHASE`, `CRZ`, or `SWAP` nodes.

## Acceptance criteria

- Static `QubitRegister<N>` QFT/IQFT calls produce immutable QPU instructions.
- All emitted opcodes belong to `H/X/Y/Z/CX/RX/RY/RZ` plus terminal `Measure`.
- Controlled phase rotations are represented by the accepted `CX`/`RZ` sequence.
- Register reversal is represented by three-CX swap decompositions at the end.
- IQFT uses inverse phase signs and inverse operation order while preserving
  logical wire-order provenance.
- Dynamic or non-register QFT inputs retain existing hard diagnostics.
- No provider-specific QFT opcode or serialization boundary is introduced.

## Non-goals

Controlled/approximate QFT, hardware-native phase gates, optimization,
provider SDKs, and official educational examples.

## Phase 1 Red record

- Added [`test_qft_basic_gate_lowering_red.py`](../../tests/test_qft_basic_gate_lowering_red.py).
- Tests intentionally fail against the existing metadata-only QFT projection
  until basic-gate instruction lowering is implemented.
- No production implementation was changed. Phase 2 Green requires explicit
  approval.

## Phase 2 Green record

- Added static QFT/IQFT instruction expansion for `QubitRegister<N>`.
- Controlled phase rotations lower only to `CX` and `RZ`.
- Register reversal lowers to three `CX` instructions per swap pair.
- IQFT reverses the operation order and phase signs while preserving logical
  wire-order provenance.
- Verification: QFT lowering tests, Spec Verification 165/165,
  `compileall`, and `git diff --check` passed.

## Phase 3 review record

- Extracted controlled-phase and register-reversal decomposition helpers from
  the QFT traversal so each mathematical lowering rule has one reviewable
  implementation point.
- Preserved the basic opcode boundary, inverse ordering, phase signs, and
  provenance behavior without adding provider-specific operations.
- Reviewer empathy: the QFT traversal now communicates ordering, while the
  two decomposition helpers communicate the gate contracts directly.
- Verification: focused QFT tests, Spec Verification 165/165, `compileall`,
  and `git diff --check` passed.
