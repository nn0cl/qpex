# LISS-0040: Symbolic Lindblad jump lowering

- Status: **Phase 3 reviewed; one-qubit symbolic jump slice complete**
- Phase: `phase-3-refactor`
- Type: feature
- Priority: high
- Initial size: M
- Current size: M
- Owner: Adjudicator / QPex agent
- Depends on: LISS-0039, LISS-0011, ADR 0057
- Related: LISS-0018, LISS-0037, LISS-0038, ADR 0069
- Branch: `codex/density-matrix-lindblad`

## Summary

Lower a resolved source-level `Operator` into a finite Lindblad jump matrix.
This extends the completed numeric `JumpSet([RawMatrix(...)])` slice without
reusing CPTP `Channel` semantics or adding a second operator algebra.

## Accepted surface

```qpex
Operator H = X
Operator decay = X + Z
DensityState<Qubit> rho = DensityState(
    RawMatrix([[0.0, 0.0], [0.0, 1.0]])
)
DensityState<Qubit> evolved = lindblad(
    rho, H, JumpSet([decay]), 0.1
)
measure evolved
```

For this slice, each symbolic jump must be a resolvable `Operator` binding and
must lower to a one-qubit finite matrix through the existing
`compile_hamiltonian` path. `RawMatrix` and `Operator` entries may not be mixed
implicitly with `Channel` values. The order of the list is preserved.

## Acceptance criteria

1. A `JumpSet` containing a bound one-qubit `Operator` lowers and is applied by
   the existing fixed-step RK4 Lindblad runtime.
2. Multiple symbolic jump operators are all applied in source list order.
3. A symbolic operator whose lowered matrix dimension does not match the
   source `DensityState` produces `LINDBLAD_JUMP_DIMENSION_ERROR`.
4. An unresolved jump symbol produces `SYMBOLIC_JUMP_LOWERING_REQUIRED`; it is
   never treated as an empty list or assigned a numeric default.
5. `Channel` values remain rejected as jump entries with
   `INVALID_LINDBLAD_JUMP_SET`; `INCOMPLETE_KRAUS_CHANNEL` remains Kraus-only.
6. Existing numeric `RawMatrix` jumps, empty jumps, pure-state behavior, and
   opaque terminal Host results remain unchanged.

## Non-goals

- New symbolic operator algebra, adjoint syntax, or general non-Hermitian type
  system.
- `FermionOperator`, `BosonOperator`, POVM effects, or dynamic measurement.
- Multi-qubit symbolic jump lowering beyond the existing one-qubit source lane.
- QPU execution, adaptive integration, or new numerical dependencies.

## AT-TDD plan

- Phase 1 Red: add source acceptance tests for one/multiple bound operators,
  unresolved symbols, dimension mismatch, and Channel rejection.
- Phase 2 Green: resolve Operator ASTs through the existing Hamiltonian compiler
  and pass the resulting matrices to the RK4 runtime.
- Phase 3 Refactor: clarify shared jump resolution and preserve numeric-path
  behavior.

## Adjudicator decision points

- Confirm `JumpSet([boundOperator])` as the symbolic MVP surface.
- Confirm one-qubit-only lowering for this slice.
- Confirm `SYMBOLIC_JUMP_LOWERING_REQUIRED` as the unresolved-symbol diagnostic.
- Approve the Phase 1 Red gate before tests are added.

## Phase 1 Red record

- Added [`test_symbolic_lindblad_jump_lowering_red.py`](../../tests/test_symbolic_lindblad_jump_lowering_red.py).
- Five acceptance tests are Red against the current implementation:
  bound operator lowering, multiple symbolic jumps, unresolved-symbol
  diagnosis, symbolic dimension mismatch, and Channel rejection.
- No production implementation was changed in this phase.
- Phase 2 was started only after the reviewed Red tests were approved.

## Phase 2 Green record

- Bound one-qubit `Operator` entries in `JumpSet` lower through the existing
  `compile_hamiltonian` path and are passed to the fixed-step RK4 runtime.
- Multiple symbolic jumps are preserved as a list and all are applied.
- Unresolved symbols produce `SYMBOLIC_JUMP_LOWERING_REQUIRED`.
- Operator site dimensions outside the one-qubit source domain produce
  `LINDBLAD_JUMP_DIMENSION_ERROR`.
- Channel entries remain rejected with `INVALID_LINDBLAD_JUMP_SET` and do not
  reuse `INCOMPLETE_KRAUS_CHANNEL`.
- The five reviewed acceptance tests pass; numeric jump regression behavior is
  unchanged.

## Phase 3 review record

- Shared one-qubit Operator compilation is centralized in the evaluator rather
  than duplicated between Hamiltonian and jump resolution.
- Jump contract diagnostics use explicit, nullable code/message typing and a
  source-level `JumpSet([...])` message that covers both numeric and symbolic
  entries.
- Reviewer empathy: a future reader can follow the same operator-to-matrix
  path for `H` and symbolic jumps while the source contract still keeps
  `Channel` separate.
- Verification: all standalone tests pass, Spec Verification is 165/165,
  `py_compile` passes, and `git diff --check` passes.
