# LISS-0043: Finite mathematical binder lowering

## Metadata

- Local issue ID: LISS-0043
- GitHub issue: none
- Status: **Phase 2 Green**
- Phase: Feature Path — Phase 2 Green complete; Phase 3 review pending
- Type: compiler lowering + tests
- Priority: P1
- Planning size: L
- Depends on: LISS-0030, LISS-0038, LISS-0029, ADR 0088
- Related: LISS-0033, LISS-0017, LISS-0041

## Summary

Lower the accepted symbolic finite-binder surface into concrete Pauli
Hamiltonian operators while preserving source provenance and rejecting invalid
open-boundary access.

## Accepted scope

- Inclusive `Index<start..end>` range syntax.
- Static open-boundary domains.
- `next(i)` validation during expansion.
- Restricted Pauli nearest-neighbor `sum` body.
- Concrete Pauli Operator tree output for the existing Suzuki path.
- Binder provenance and resource metadata.

## Deferred

Periodic boundaries, `product`, `Basis<N>`, indexed coefficient arrays,
arbitrary functions, non-Pauli operators, symbolic fallback, and direct QPU or
provider lowering.

## Phase 1 Red record

- Added `tests/test_finite_binder_lowering_red.py`.
- Tests define inclusive range parsing, open-boundary rejection, invalid-range
  diagnostics, resource rejection, concrete term count, and provenance.
- Production parser, AST, type checker, and lowering code are unchanged.
- Expected Red result: the current compiler does not yet recognize the range
  domain or expose the resolved binder lowering contract.

## Phase 2 Green record

- Existing implementation commits `b0f12ed` and `50da9f3` provide the accepted
  parser, static validation, concrete lowering, diagnostics, resource guard,
  and provenance projection.
- `python3 tests/test_finite_binder_lowering_red.py` passes all five scenarios.
- No periodic, general-operator, provider, or direct-QPU lowering was added.
- Phase 3 refactor review remains separate and is not inferred from this
  Phase 2 approval.
