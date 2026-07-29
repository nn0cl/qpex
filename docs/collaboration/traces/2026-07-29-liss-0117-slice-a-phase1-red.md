# Trace: LISS-0117 Slice A Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0117 |
| Slice | A — fixture layout + snapshot loader |
| Phase | Phase 1 Red |
| Branch | `feature/liss-0117-slice-a` |
| Approval | Adjudicator “LISS-0117 Slice Aを進めて” |

## [DESIGN CHECK]

- Scope: load six `PIR-G-*` fixture snapshots; verify provenance; keep
  `oracle_promoted=False`. No lowering, no Equation assertions, no
  `physics_ir.py` edits.
- Exclusive: `physics_ir_goldens.py`, `tests/fixtures/physics_ir/**`,
  `tests/test_physics_ir_goldens_*.py`.
- Verification: runner fails with ImportError until Green.

## Delivered

- `tests/test_physics_ir_goldens_slice_a_red.py`
- Issue / register / claims → Agent C in progress

## Next safe action

Adjudicator Slice A Red approval → Phase 2 Green (loader + fixtures only).
