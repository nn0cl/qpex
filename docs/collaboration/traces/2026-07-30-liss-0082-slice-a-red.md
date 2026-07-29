# LISS-0082 Slice A Phase 1 Red

- Date: 2026-07-30
- Branch: `feature/liss-0082-slice-a-red`
- Operating path: Feature Path after Architecture Path intake
- Issue: LISS-0082
- Slice/phase: Slice A / Phase 1 Red
- Approval: user P0-start approval, interpreted under the already reviewed
  next-safe-action boundary as Slice A Red only
- Implementation permission: **none**
- Technology selection permission: **none**
- Post-review required: Adjudicator review before Phase 2 Green

## Scope

Added only `tests/test_quantum_semantic_ir_slice_a_red.py` for immutable
semantic IDs, provenance, schema version, deterministic identity, and root
verifier diagnostics. Region behavior, lowering, pipeline, simulator, target,
provider, and later Slices remain out of scope.

## Red evidence

- `python3 tests/test_quantum_semantic_ir_slice_a_red.py`
  **fails as expected** with `ModuleNotFoundError` because the Green module
  does not yet exist.
- `python3 -m pytest -q tests/test_quantum_semantic_ir_slice_a_red.py`
  could not run because pytest is not installed in this workspace.

The expected Red is the missing `compiler.staqex.quantum_semantic_ir` API, not
an assertion workaround. No implementation was added.

## Stop condition

Stop after Red evidence. Do not modify `compiler/`, do not edit assertions to
make them pass, and do not begin Slice B, Green, Refactor, simulator, or
provider work without separate approval.
