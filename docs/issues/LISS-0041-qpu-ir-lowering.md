# LISS-0041: Provider-neutral QPU IR lowering and opcode vocabulary

## Metadata

- Local issue ID: LISS-0041
- GitHub issue: none
- Status: **Phase 3 reviewed**
- Phase: Feature Path — Phase 3 Refactor complete
- Type: backend architecture + lowering
- Priority: P2
- Initial planning size: L
- Current planning size: L
- Depends on: LISS-0019, ADR 0077
- Related: ADR 0032, ADR 0059, LISS-0016, LISS-0027, LISS-0028

## Summary

Introduce the first concrete lowering slice from the existing DAG IR to an
immutable, provider-neutral QPU IR consumed directly by the OpenQASM adapter.
This issue does not add public source syntax, provider SDKs, serialization, or
dynamic-circuit semantics.

## Accepted scope

- Basic gate nodes: `H`, `X`, `Y`, `Z`, `CX`, `RX`, `RY`, `RZ`.
- Symbolic parameter nodes retained until a later Host binding boundary.
- Terminal measurement node preserving QPex measurement semantics.
- Immutable root metadata for Hilbert shape, parameters, measurement, and
  approximation provenance.
- Pure DAG-to-QPU-IR lowering with full provenance copying.
- Direct in-memory QPU IR input to the OpenQASM adapter.
- Hard `E_QPU_UNSUPPORTED_CAPABILITY` diagnostics for unsupported features.

## Explicit non-goals

- JSON or other serialization.
- Provider SDKs, credentials, submission, or Job objects.
- Dynamic control-flow opcodes and host fallback.
- New QPex source syntax or a public QPU IR API.
- Optimization, scheduling, routing, or target-specific gate expansion beyond
  the existing adapter contract.

## Acceptance criteria

1. A static register circuit lowers to immutable QPU IR with Hilbert shape and
   source provenance intact.
2. `Param<Angle>` remains symbolic in QPU IR and is not replaced with Host
   data.
3. Terminal `measure` becomes a QPU IR measurement node and is not rewritten
   as a provider operation.
4. Every lowered node retains the provenance of its source DAG node.
5. Unsupported dynamic or otherwise unavailable capabilities fail with
   `E_QPU_UNSUPPORTED_CAPABILITY`; no CPU/Host fallback occurs.
6. OpenQASM emission accepts the in-memory QPU IR representation without a
   serialization round trip.
7. Provider SDK objects and serialization code are absent from the Kernel
   boundary.

## Phase gates

- Phase 0: accepted by Adjudicator decision recorded in ADR 0085.
- Phase 1 Red: add only the acceptance tests above.
- Phase 2 Green: implement the smallest immutable IR and pure lowering pass.
- Phase 3 Refactor: review ownership, provenance copying, and adapter purity.

## Phase 1 Red record

- Added [`test_qpu_ir_lowering_red.py`](../../tests/test_qpu_ir_lowering_red.py).
- The tests intentionally require the accepted immutable QPU program metadata,
  instruction provenance, terminal `Measure` node, and unsupported-capability
  diagnostic that the inspection-only projection does not yet provide.
- No implementation code was changed. Phase 2 Green requires explicit approval.

## Phase 2 Green record

- Added immutable `QpuProgram` and frozen `QpuInstruction` in the compiler
  boundary.
- Added static register gate/measurement projection with source provenance,
  Hilbert shape metadata, symbolic parameter preservation, and the hard
  `E_QPU_UNSUPPORTED_CAPABILITY` diagnostic for dynamic evolve/QPU control.
- Added direct in-memory `QpuProgram` consumption by the OpenQASM adapter.
- Added Green regression checks. Serialization, provider SDKs, dynamic opcodes,
  and Host fallback remain out of scope.
- Verification: focused Red/Green checks, Spec Verification 165/165,
  `compileall`, and `git diff --check` passed.

## Phase 3 review record

- Centralized the accepted opcode vocabulary and kept the QASM gate mapping in
  the adapter rather than duplicating it in callers.
- Kept `QpuProgram` and `QpuInstruction` immutable at the object boundary;
  provider objects and serialization remain absent.
- Reviewer empathy: source provenance, Hilbert shape, measurement metadata,
  and instruction sequence are visible as separate concerns, while the
  adapter's unsupported-opcode path remains explicit.
- Verification: focused Red/Green checks, Spec Verification 165/165,
  `compileall`, and `git diff --check` passed.
