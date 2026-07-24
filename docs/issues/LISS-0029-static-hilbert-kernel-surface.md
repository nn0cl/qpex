# LISS-0029: Static Hilbert Kernel surface

## Metadata

- Local issue ID: LISS-0029
- Status: **Phase 3 reviewed; MVP migration/resource boundary complete**
- Phase: Feature Path — Phase 3 review complete; target profile follow-up open
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
  reviewed separately below**.
- Added physicist-facing documentation for `QubitRegister<N>` and clarified
  that `N` is Hilbert-space shape metadata rather than a runtime integer.
- Target-specific resource profile ownership and post-routing checks remain
  separate QPU IR/backend work.

## Migration/resource follow-up Phase 1 Red record

- Added [`test_static_hilbert_migration_red.py`](../../tests/test_static_hilbert_migration_red.py).
- The tests require the historical `register(N)` spelling to produce
  `STATIC_HILBERT_SURFACE_ERROR` rather than remain an implicit compatibility
  alias.
- The tests require an oversized `QubitRegister<N>` expansion to produce
  `STATIC_HILBERT_RESOURCE_ERROR` and never silently truncate.
- Red evidence: the first test fails against the current implementation
  because the legacy spelling is still accepted; Phase 2 Green is not started.

## Migration/resource follow-up Phase 2 Green record

- `register(N)` now produces `STATIC_HILBERT_SURFACE_ERROR` in the static
  `forEach` boundary; no compatibility alias is retained.
- `QubitRegister<N>` carries its compile-time shape through the local QASM and
  simulator elaboration paths. The MVP rejects logical shapes above 1024 with
  `STATIC_HILBERT_RESOURCE_ERROR` rather than truncating them.
- The existing static-register example and boundary fixtures were migrated to
  `QubitRegister<N> reg = system()`.
- Verification: all standalone tests pass and specification verification is
  165/165 (100%). Phase 3 Refactor remains pending.

## Migration/resource follow-up Phase 3 review record

- The shared `MVP_MAX_LOGICAL_QUBITS` policy constant now owns the compiler
  safety budget used by type checking, QASM lowering, and local simulation.
- Diagnostics and runtime failures retain the same stable codes; this refactor
  only removes the duplicated literal and keeps target-specific routing
  profiles deferred to the QPU IR/backend boundary.
- Reviewer empathy: the source-facing rule, compile-time diagnostic, and
  backend/runtime defense now point to one named policy rather than three
  independent limits.
- Status: **Phase 3 reviewed; migration/resource follow-up complete for the
  MVP boundary**. Logical/ancilla/depth/post-routing target profiles remain
  separate follow-up work.
