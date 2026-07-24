# LISS-0038: Semantic discrete carriers and phase-local types

- Status: **Phase 3 reviewed** (carrier slice complete; indexed syntax remains deferred)
- Depends on: ADR 0018, ADR 0069, ADR 0070, LISS-0018
- Blocks: LISS-0030 and every indexed/operator surface using discrete labels
- AT-TDD Phase 1 Red: [`test_semantic_discrete_carriers_red.py`](../../tests/test_semantic_discrete_carriers_red.py)

## Summary

Replace the overloaded surface role of `Int` with meaning-bearing discrete
carriers and phase-local types before adding indexed expressions. Machine
representation may be shared internally; surface semantics and legal operations
must not be shared implicitly.

## Candidate type families

### Meta / host and execution phase

- `Nat` — internal or explicitly scoped natural-number foundation;
- `Dimension` — finite Hilbert-space dimension;
- `Index<N>` — an index into a specific finite domain;
- `Count` / `ShotCount` / `IterationCount` — execution quantities;
- `BitWidth` / `Order` — structural compilation metadata.

### Theory / quantum-object phase

- `Bit` — a two-element physical carrier;
- `Basis<N>` — a basis label for a declared finite space;
- `EnergyLevel<N>` — a typed discrete physical quantity;
- `SpinProjection<S>` and other domain-specific physical carriers;
- user-defined closed enums and finite symbols.

The list is a design inventory, not an acceptance of all names. The key rule is
that `Index<N>` and `Basis<N>` are not implicitly interchangeable, and a
`ShotCount` is not visible in a theory expression.

## Required decisions

- whether generic `Int` remains available in host-only code;
- whether `Nat` is surface-visible or compiler-internal;
- representation and bounds for `Index<N>`;
- literal construction and explicit conversions;
- legal operations for each semantic carrier;
- visibility rules across Theory, Experiment, Workflow, and Execution;
- diagnostics for mixing carriers with equal machine representation;
- interaction with `State<T>`, `QubitRegister<N>`, and `Param<T>`.

## Non-goals

- no indexed syntax, `sum`, or `product` grammar;
- no general physical unit system redesign;
- no general classical collection/runtime loop;
- no implicit conversion from a host count to a quantum basis label.

## Required evidence before dependent work

Provide a type/phase matrix and negative examples for:

```text
Index<N> + ShotCount
Basis<N> + Dimension
State<EnergyLevel<N>> + IterationCount
theory expression reading backend or shots
```

LISS-0030 may proceed only after this carrier boundary is accepted.

## Phase 3 review record

- Generic `Int` remains available only where legacy Kernel behavior already
  requires it; it is not a synonym for any semantic carrier.
- `Dimension`, `ShotCount`, and `IterationCount` accept only their declared
  non-negative/positive literal policy. No implicit conversion from a literal
  or another carrier creates `Index<N>` or `Basis<N>`.
- `index(...)` and `basis(...)` are the explicit construction boundary for the
  corresponding semantic values. Their bounds and domain argument rules remain
  dependent on LISS-0030.
- Public names are locked to the semantic names in the specification; aliases
  such as `IntIndex` or `QuantumInt` are not introduced.
- Full module-phase visibility is deferred to LISS-0034. The current Kernel
  entry boundary enforces only the implemented carrier diagnostics.
- Status: **Phase 3 reviewed; LISS-0038 carrier slice complete**.

## Phase 2 Green record

- Implemented compile-time carrier kinds for `Dimension`, `Index<N>`,
  `Basis<N>`, `Bit`, `EnergyLevel<N>`, `SpinProjection<S>`, `ShotCount`,
  `IterationCount`, `Count`, and `Nat`.
- Added explicit mismatch, phase-visibility, and unsupported-operation
  diagnostics.
- `index(...)` and `basis(...)` now carry semantic types in the checker; they
  do not introduce runtime indexed evaluation or `Int` conversion.
- Regression checks: all standalone `tests/test_*.py` scripts passed;
  specification verification passed 165/165 (100%).

Follow-on work remains outside this slice: full module-phase visibility belongs
to LISS-0034, and indexed-expression syntax belongs to LISS-0030. Neither is
implicitly accepted by this completion record.
