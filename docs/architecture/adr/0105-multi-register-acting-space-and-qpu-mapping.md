# ADR 0105: Multi-register acting-space and QPU mapping boundary

- Status: Accepted architecture boundary
- Date: 2026-07-27
- Related: ADR 0069, ADR 0102, LISS-0041, LISS-0058, LISS-0065, LISS-0066,
  LISS-0067

## Context

Staqex currently has an accepted acting-space boundary for one static
`QubitRegister<N>`. Realistic multi-particle and multi-system expressions need
more than one register while preserving the separation between physical
meaning, compiler logical shape, QPU IR, and eventual provider mapping.

## Decisions

Treat a multi-register system as a typed, immutable tensor-product space. Each
register has a stable logical identity and static size. Operators carry the
set of registers on which they act. QPU IR may derive flat logical indices,
but it retains the source register reference and tensor-order provenance.

```text
named registers
  → typed tensor-product space
  → operator acting-space validation
  → resolved logical QPU references
  → later provider physical mapping
```

The single-register `QubitRegister<N>` contract remains valid and does not gain
an implicit compatibility alias for multiple registers.

### D1 — Use a declarative system shape with named registers

The surface uses the existing scientific `system` declaration boundary. A
system shape declares named registers and their static sizes:

```staqex
system BellPair {
    register data : QubitRegister<2>
    register ancilla : QubitRegister<1>
}
```

This keeps the physical system visible without introducing a builder API or a
generic runtime register allocator.

### D2 — Use `RegisterSet<SystemName>` as the composite acting-space type

The composite semantic carrier is `RegisterSet<SystemName>`. A multi-register
operator therefore has an explicit acting-space type such as
`Operator<RegisterSet<BellPair>>`. The existing single-register
`Operator<QubitRegister<N>>` remains canonical for one register.

### D3 — Qualify indexed references by register name

Register-local sites use the equation-shaped form `data[0]` and
`ancilla[0]`. An unqualified site is permitted only inside a context with one
register; it is a hard ambiguity otherwise. No register is selected by a
numeric offset or declaration hash.

### D4 — Preserve declaration order as tensor order

The source declaration order is the tensor-product order. It is deterministic,
visible to the physicist, and does not require a second canonical sorting
rule. A future explicit reorder operation would be a separate decision.

### D5 — Retain both logical and derived flat identity in QPU IR

Each QPU IR logical-qubit reference retains `logical_register`,
`logical_index`, and the derived `flat_index`, together with tensor-order
provenance. The flat index is an implementation mapping, not a replacement for
the source identity.

### D6 — Split shape checks between Kernel and QPU IR

The static Hilbert boundary validates register widths, tensor width, and
Hilbert dimension. QPU IR lowering validates the derived logical flat mapping
and provenance consistency. Physical-device capacity and routing remain Host
provider responsibilities and are not selected here.

### D7 — Composite acting spaces are invariant

`Operator<RegisterSet<A>>` and `Operator<RegisterSet<A, B>>` are distinct
types. No implicit covariance, register merging, or single-register lift is
allowed. Embedding an operator into a larger space must be a future explicit
operation with its own acceptance contract.

## Candidate value objects

- `RegisterId`: stable source identity.
- `RegisterShape`: identity plus static width.
- `RegisterSet`: immutable named collection with explicit order.
- `TensorProductShape`: derived total logical width and Hilbert dimension.
- `LogicalQubitRef`: register-qualified logical site reference.

## Proposed invariants

- register widths are statically known and positive;
- tensor order is deterministic and explicit;
- total logical qubits are additive while Hilbert dimension is multiplicative;
- logical-to-flat mapping is derived and provenance-preserving;
- unknown or incompatible acting space is a hard diagnostic;
- no one-register fallback or provider-specific mapping occurs in the Kernel.

## Consequences

- Register identity remains visible in source, semantic types, and QPU IR.
- Source order is the only tensor-order rule in the initial slice.
- Ambiguous or cross-space operations fail explicitly rather than being
  flattened or defaulted.
- Provider physical routing remains a separate Host concern.

## Approval status

This ADR is accepted as the architecture boundary for LISS-0067. The
Adjudicator subsequently approved Phase 2 Green and reviewed Phase 3 for the
accepted Kernel/QPU-IR slice. Provider selection and physical routing remain
separately gated.
