# LISS-0029: Static Hilbert Kernel surface

## Metadata

- Local issue ID: LISS-0029
- Status: Open
- Phase: Architecture Path accepted; pending Phase 1 Red approval
- Type: language type system / static QPU shape
- Priority: P0
- Related: ADR 0069, LISS-0026, LISS-0019

## Acceptance specification

- [x] `QubitRegister<N>` is a normative type-level shape with no runtime
      allocation semantics.
- [x] Declaration and initialization syntax is specified without exposing a
      runtime classical loop/index model.
- [x] `forEach` accepts a register and binds an opaque element handle.
- [x] `State<T>` remains the pre-measurement state model; no `StateVector<N>`
      commitment is introduced.
- [ ] Logical qubit, ancilla, gate-count, depth, and post-routing resource
      checks have explicit ownership and diagnostics.
- [ ] Existing bounded `register(N)` implementation and example are migrated
      deliberately; no compatibility alias is assumed.

## Non-goals

- `Param<T>` semantics (LISS-0027).
- Dynamic circuits/feed-forward (LISS-0028).
- Density matrix/Lindblad representation (ADR 0057).

## Phase 1 record

- Status: **Red complete; awaiting Phase 2 Green approval**.
- Test file: `tests/test_static_parametric_dynamic_boundaries_red.py`.
- The test uses provisional `QubitRegister<N> reg = system()` syntax. The
  type-level shape contract is fixed for review; declaration initialization
  remains an explicit Phase 2 design point.

## Phase 2 record

- Status: **Green complete; awaiting Phase 3 Refactor approval**.
- Numeric type-level shapes, register bindings, and `forEach` over a register
  are accepted by the type boundary.
- The historical `register(N)` implementation remains available until the
  separately authorized migration slice; no compatibility policy was added.
- Verification: all unit tests and SV 165/165 passed.

## Phase 3 record

- Status: **Complete for the type-level boundary; migration/resource follow-up
  open**.
- Added physicist-facing documentation for `QubitRegister<N>` and clarified
  that `N` is Hilbert-space shape metadata rather than a runtime integer.
- Remaining: migrate the historical `register(N)` fixture, define resource
  profile ownership, and add post-routing checks.
