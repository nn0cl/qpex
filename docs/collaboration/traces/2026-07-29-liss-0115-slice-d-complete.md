# Trace: LISS-0115 Slice D + Issue closeout

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0115 |
| Slice | D — soft `compile_source` / `CompileResult.physics_ir` wire |
| Branch | `feature/liss-0115-slice-d` |
| Path | Feature Path / Phase 1 Red → Phase 2 Green → Phase 3 Refactor |

## Design note

Soft-attach `lower_hir_to_physics_ir(hir, unit=unit)` inside `_analyze_unit`
without equations. Append `verify_lowered_physics_ir` diagnostics; keep
`PHYSICS_IR_*` outside `_HARD_CODES`. Evaluator unchanged. Equation
auto-extraction remains out of scope.

## Artifacts

- `compiler/staqex/pipeline.py` — `CompileResult.physics_ir`, `_soft_physics_ir`
- `compiler/staqex/physics_ir_lower.py` — docs + validation cleanup
- `tests/test_physics_ir_lower_d_red.py`
- Slice A guard updated for approved soft wire
- Docs sync: Issue/plan, open-work-register, WP-0025 Current next, WP-0028
  closed, local-issue-planning, golden catalog remaining work, LISS-0081
  follow-up note

## Verification

- Direct runners A–D PASS
- `py_compile` / `git diff --check` PASS

## Next

Adjudicator: commit → PR → merge; then LISS-0081 closeout judgment and/or
LISS-0082 plan intake.
