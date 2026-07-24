# LISS-0039: Explicit Lindblad jump inputs

- Status: **Phase 3 reviewed; explicit numeric jump slice complete**
- Phase: `phase-3-refactor`
- Type: feature
- Priority: high
- Initial size: M
- Current size: M
- Owner: Adjudicator / QPex agent
- Depends on: LISS-0011, ADR 0057
- Related: LISS-0018, LISS-0037, LISS-0038, ADR 0069
- Branch: `codex/density-matrix-lindblad`

## Summary

Add an explicit source-level representation for non-empty Lindblad jump
operators. The first slice accepts a typed list of `RawMatrix` values through
`JumpSet`; it does not reuse `Channel` as a jump list and does not infer
symbolic operators or dimensions.

## Decision boundary

The accepted MVP surface is:

```qpex
DensityState<Qubit> rho = DensityState(RawMatrix([[1.0, 0.0], [0.0, 0.0]]))
DensityState<Qubit> out = lindblad(
    rho, H, JumpSet([RawMatrix([[0.0, 1.0], [0.0, 0.0]])]), 0.1
)
```

`JumpSet` is a semantic wrapper for Lindblad operators, while `RawMatrix` is
the explicit numeric payload. `Channel` remains a CPTP map and is not
implicitly accepted as a Lindblad jump input. No symbolic jump lowering,
POVM construction, or QPU execution is included in this issue.

## Acceptance criteria

1. A non-empty `JumpSet([RawMatrix(...)])` is accepted by the source contract.
2. Each jump matrix must match the density-state Hilbert dimension.
3. A malformed jump payload is rejected without padding, truncation, or
   implicit conversion.
4. An unresolved symbolic jump remains an opaque contract path and does not
   receive a hidden numeric default.
5. The runtime applies all explicit jump matrices through the existing fixed
   step RK4 Lindblad path and preserves the declared numerical guards.
6. `INCOMPLETE_KRAUS_CHANNEL` is reserved for Kraus completeness failures.
   Jump-specific failures use `INVALID_LINDBLAD_JUMP_SET` or
   `LINDBLAD_JUMP_DIMENSION_ERROR`.
7. Existing empty-jump and pure-state behavior remains unchanged.

## Non-goals

- Reusing `Channel` as a Lindblad jump operator list.
- Symbolic `Operator` jump lowering.
- POVM/effect syntax or dynamic mid-circuit measurement.
- Adaptive integration, higher-order Suzuki methods, or QPU execution.
- New numeric dependencies or a new matrix storage technology.

## AT-TDD plan

- Phase 1 Red: add source acceptance tests for valid numeric jumps, invalid
  dimensions/payloads, diagnostics, and preservation of the opaque unresolved
  path. Do not change production code.
- Phase 2 Green: minimally connect `JumpSet` and explicit matrices to the
  existing runtime Lindblad evaluator.
- Phase 3 Refactor: review naming, error boundaries, and duplication without
  changing accepted behavior.

## Adjudicator decision points

- Confirm `JumpSet([RawMatrix(...)])` as the MVP source surface.
- Confirm that `Channel` is not accepted as a jump input.
- Confirm the diagnostic names and that Kraus completeness remains scoped to
  `INCOMPLETE_KRAUS_CHANNEL`.
- Approve the Phase 1 Red gate before test files are added.

## Phase 1 Red record

- Added [`test_lindblad_jump_inputs_red.py`](../../tests/test_lindblad_jump_inputs_red.py).
- Four acceptance tests are Red against the current implementation:
  non-empty numeric jump application, Hilbert-dimension rejection, malformed
  payload rejection, and Channel/non-Kraus diagnostic separation.
- The unresolved symbolic jump opaque-path test remains Green because that
  behavior is already provided by the existing source bridge.
- At the Phase 1 gate, no production implementation was changed.
- Phase 2 was started only after the reviewed Red tests were approved.

## Phase 2 Green record

- `JumpSet([RawMatrix(...)])` is accepted for non-empty numeric jump input.
- Jump matrices are resolved into the existing dependency-free fixed-step RK4
  Lindblad runtime.
- Qubit dimension mismatch produces `LINDBLAD_JUMP_DIMENSION_ERROR`.
- Non-matrix or malformed jump entries produce
  `INVALID_LINDBLAD_JUMP_SET`.
- `INCOMPLETE_KRAUS_CHANNEL` is not emitted for jump input.
- Reviewed Red tests were not changed to pass; all five focused tests now pass.
- Symbolic jump lowering and QPU execution remain out of scope.

## Phase 3 review record

- The runtime matrix conversion helper is now an explicit module boundary
  (`matrix_from_list`) rather than a private cross-module import.
- Jump resolution uses the shared `Matrix` type annotation; no behavior or
  accepted diagnostic changed.
- Reviewer empathy: a future reader can distinguish CPTP `Channel` values from
  Lindblad `JumpSet` values at the source and runtime boundaries, and can find
  dimension/payload failures in the named jump diagnostics.
- Verification remains: all standalone tests pass, Spec Verification is
  165/165, `py_compile` passes, and `git diff --check` passes.
