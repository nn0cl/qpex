# Trace: LISS-0082 Slice F Green + Refactor

| Field | Value |
|---|---|
| Date | 2026-07-31 |
| Issue | LISS-0082 |
| Slice | F — soft `CompileResult.quantum_semantic_ir` |
| Branch | `feature/liss-0082-slice-f-adr-batch` |
| Path | Feature Path / Phase 2 Green → Phase 3 Refactor |
| Approval | Adjudicator “承認” after Red, then “承認” after Green |

## Green

- Added `CompileResult.quantum_semantic_ir`.
- Soft-lowered via `lower_physics_to_quantum_semantic_ir` with empty finite
  evidence (plan §9); append `QSEM_*` diagnostics without `_HARD_CODES`.
- `tests/test_quantum_semantic_ir_slice_f_red.py` PASS; integrated Semantic IR
  and Physics soft-wire runners PASS.

## Refactor

- Extracted `_soft_quantum_semantic_input` so the empty-evidence soft-wire
  contract is named once beside `_soft_quantum_semantic_ir`.
- Behavior and reviewed assertions unchanged.

## Verification

- `python3 tests/test_quantum_semantic_ir_slice_f_red.py`
- `python3 tests/test_quantum_semantic_ir_integrated_red.py`
- `python3 tests/test_physics_ir_lower_d_red.py`
- `python3 -m py_compile compiler/staqex/pipeline.py`
- `git diff --check`

## Stop

Await commit / PR / merge approval for the ADR acceptance + Slice F packet.
