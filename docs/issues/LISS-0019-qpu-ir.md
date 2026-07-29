# LISS-0019: Concrete QPU IR boundary

## Metadata

- Local issue ID: LISS-0019
- GitHub issue: none
- Status: **Phase 3 reviewed; inspection boundary complete**
- Phase: Feature Path — Phase 3 review complete; concrete lowering follow-up open
- Type: architecture + backend boundary
- Priority: P2
- Initial planning size: L
- Current planning size: TBD
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

## Summary

Determine whether Staqex needs a concrete QPU IR between the Kernel amplitude
model and OpenQASM/host adapters, and define its ownership if it does.

## Acceptance Notes

- [ ] Need for an intermediate QPU IR is demonstrated by a concrete use case.
- [ ] IR ownership, lifecycle, and ports are specified if retained.
- [ ] Relation to DAG IR and OpenQASM emission is explicit.
- [ ] State/measurement semantics cannot be weakened by lowering.
- [ ] No provider-specific IR is adopted without technology approval.

## Dependencies

- Parent: none
- Depends on: ADR 0032, ADR 0059, LISS-0016
- Blocks: multi-backend QPU lowering beyond OpenQASM
- Related: `staqex-backend-targets.md`, LISS-0011

## Adjudicator Decision Points

- [ ] Keep OpenQASM as the only public backend IR or add an internal IR?
- [ ] Which backend requirement justifies the additional layer?
- [ ] Which semantics are forbidden to encode as provider-specific behavior?

## Context

- Included: current DAG IR, OpenQASM 3, future QPU ports.
- Omitted: cloud submission implementation and provider SDK selection.
- Assumptions: CPU Kernel remains authoritative.

## Architecture decision record

- [ADR 0077](../architecture/adr/0077-provider-neutral-qpu-ir-boundary.md)
  accepts an internal provider-neutral QPU IR boundary.
- The decision does not authorize an opcode set, serialization format,
  provider SDK, or public source syntax.
- Phase 1 Red must first define the smallest observable contract for source
  provenance, Hilbert shape, symbolic parameters, measurement semantics, and
  explicit unsupported-feature diagnostics.

## AI Planning Records

### AIP-0019-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: L
- Intended execution route: Architecture Path only.
- Intended scope: boundary decision and non-goals.
- Estimation basis: potential new subsystem and backend consequences.
- Assumptions: no IR code is authorized by this issue.
- Confidence: medium

## Verification

- Architecture dependency review and backend portability examples after acceptance.

## Phase 1 Red intake boundary

The architecture decision is accepted, but the internal IR's observable test
contract is not yet fixed. Before adding Red tests, the Adjudicator must
choose the smallest inspection boundary from the following candidates:

- a compiler-internal `QpuPlan`/`QpuNode` object exposed only to backend tests;
- an inspectable `CompileResult` projection with source/provenance records;
- a backend adapter input contract tested through OpenQASM lowering fixtures.

The Red slice must then cover, without selecting an opcode inventory:

1. source/resolved provenance is retained for a static `QubitRegister<N>`
   circuit;
2. a symbolic `Param<Angle>` remains symbolic until binding;
3. terminal measurement semantics are represented and are not replaced by a
   provider-specific operation;
4. an unsupported capability produces an explicit diagnostic rather than Host
   fallback;
5. provider SDK objects do not appear in the Kernel boundary.

Unresolved before Phase 1 Red: the projection name, stable node vocabulary,
serialization policy, and diagnostic codes. No test file is added until that
minimal acceptance contract is reviewed; this avoids turning an implementation
detail into a language or backend commitment.

## Phase 1 Red contract decision

For the smallest testable slice, the internal IR is observed through an
inspectable `CompileResult.qpu_ir` projection. This is a compiler result
boundary, not public Staqex syntax and not a serialization commitment. The Red
tests require only these stable top-level fields:

- `provenance`: source/resolved identity for the lowered program;
- `parameters`: symbolic parameter names and domains, without Host values;
- `measurement`: terminal measurement semantics;
- no provider SDK object or provider-specific submission operation.

Opcode vocabulary, backend capability DTOs, serialization, and actual lowering
remain out of scope for this Red slice.

## Phase 2 Green record

- Added the internal `CompileResult.qpu_ir` projection with provider-neutral
  `kind`, symbolic `parameters`, terminal `measurement`, and source
  `provenance` fields.
- The projection is built from existing Symbolic IR provenance and source AST
  declarations; it does not emit gates, serialize provider objects, or submit
  Jobs.
- Verification: QPU IR boundary tests pass, all standalone tests pass, and
  specification verification passes 165/165 (100%). Phase 3 review remains
  pending.

## Phase 3 review record

- Projection construction now separates parameter metadata, terminal
  measurement metadata, and the stable provider-neutral kind name into small
  responsibilities.
- The projection remains an inspection boundary only; no opcode, serialization,
  provider capability, or submission behavior is inferred from it.
- Reviewer empathy: backend readers can identify the boundary's three promised
  concerns without confusing it with executable QPU IR or a provider API.
- Status: **Phase 3 reviewed; QPU IR inspection boundary complete**. Concrete
  lowering and backend capability slices remain open.

## Design intake: current boundary and decision scope

The repository already has three distinct concerns:

```text
Staqex source / resolved contracts
    -> DAG IR and symbolic provenance
    -> OpenQASM 3 emission
    -> Host Job adapter
```

The current OpenQASM emitter is sufficient for the shipped qubit gate and
first-order Trotter slices. It is not yet a complete provider-neutral
execution representation for the accepted/future boundaries: `Param<T>`
requires symbolic parameter nodes, Dynamic QPU requires capability-checked
control, and discretization/provenance must survive finite lowering.

### Candidate decision boundary

The design question is whether to add an **internal provider-neutral QPU IR**
between resolved/symbolic IR and backend adapters. If retained, it must:

- remain an implementation boundary, not a new public Staqex source language;
- preserve source/provenance links, Hilbert shape, parameter bindings,
  measurement semantics, approximation records, and resource estimates;
- be lowered to OpenQASM through a port/adapter without importing provider SDKs;
- reject unsupported dynamic/parametric features explicitly rather than
  silently emulating them on the Host;
- keep the CPU Kernel authoritative and prevent backend-specific semantics from
  changing `State<T>` or terminal `measure` behavior.

### Concrete evidence required before Architecture Approval

The next review must compare at least these two backend cases:

1. Static qubit circuit with `QubitRegister<N>` and symbolic `Param<Angle>`;
2. A future dynamic-capability or non-OpenQASM backend that cannot be
   represented faithfully by the current text emitter alone.

No IR type, opcode set, serialization format, or backend implementation is
accepted by this design intake. Those require a subsequent Architecture
Approval and technology-independent acceptance specification.
