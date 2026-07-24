# LISS-0037: POVM, measurement, and channel contracts

- Status: **Phase 3 reviewed; terminal computational-basis POVM slice complete**
- Phase: `phase-3-refactor`
- Depends on: LISS-0011, ADR 0057, LISS-0028
- Blocks: general measurement and open-system semantics

## Summary

Define POVMs, measurement effects, projectors, classical result carriers, and
their relation to density matrices and CPTP maps. Terminal `measure` remains
the default language boundary. Mid-circuit measurement is owned by the Dynamic
QPU lane and must not be introduced as an implicit shortcut.

## Acceptance questions

- Which measurement forms are terminal-only and which require Dynamic QPU
  capability?
- How are outcome spaces and probabilities typed?
- How do channels compose with `State<T>` and the future density representation?
- What result DTO crosses into the Job/report boundary?

## Phase 0 design resolution

- Static Kernel `measure` remains terminal-only; mid-circuit measurement stays
  in LISS-0028.
- The shared explicit measurement contract is `POVM<T>`, while pure and mixed
  state representations remain distinct.
- The default basis is the finite computational basis of the source domain.
- The first implementation slice uses `ComputationalBasis()` for one qubit;
  general effect lists are specified but deferred.
- POVM completeness is distinct from Kraus completeness and receives its own
  diagnostics (`INVALID_POVM_EFFECT`, `INCOMPLETE_POVM`, and
  `POVM_DOMAIN_MISMATCH`).
- Terminal results remain opaque Host `MeasurementEnvelope` / `JobResult` DTOs.

See [ADR 0075](../architecture/adr/0075-povm-measurement-contract.md) and
[WP-0014](../work-plans/WP-0014-povm-measurement-contract.md).

## Phase 1 Red record

- Added [`test_povm_measurement_contract_red.py`](../../tests/test_povm_measurement_contract_red.py).
- Three acceptance tests are Red against the current language surface:
  explicit terminal POVM measurement of pure and mixed states, plus POVM
  domain mismatch rejection.
- No production implementation was changed in this phase.
- Phase 2 was started only after the reviewed Red tests were approved.

## Phase 2 Green record

- `POVM<Qubit> z_basis = ComputationalBasis()` is accepted as a typed
  terminal measurement contract.
- `measure state with z_basis` works for pure `State<Qubit>` and mixed
  `DensityState<Qubit>` values.
- Domain mismatch produces `POVM_DOMAIN_MISMATCH`; unsupported POVM
  constructors produce `INVALID_POVM_EFFECT`.
- Host results remain opaque and add `measurement_kind` metadata without
  exposing raw density matrices.
- The three reviewed acceptance tests pass; mid-circuit measurement and
  general effect lists remain deferred.

## Phase 3 review record

- POVM declaration validation is isolated in `measurement.py`; runtime POVM
  binding is isolated in `_bind_povm`.
- Domain extraction and diagnostic construction use small named helpers.
- Reviewer empathy: the source `POVM<T>` contract, runtime measurement choice,
  and opaque Host metadata are now easy to trace independently.
- Verification: all standalone tests pass, Spec Verification is 165/165,
  `py_compile` passes, and `git diff --check` passes.

## Non-goals

This issue does not replace or split the density/Lindblad representation
decision in LISS-0011.
