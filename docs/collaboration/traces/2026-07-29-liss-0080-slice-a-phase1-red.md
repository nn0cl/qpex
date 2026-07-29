# Trace: LISS-0080 Slice A Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0080 |
| Slice | A — immutable HIR DTO + build API |
| Phase | phase-1-red |
| Branch | `feature/liss-0080-slice-a-red` |
| Implementation | **forbidden** until Red approval → Green |

## [DESIGN CHECK]

- Scope: Red for `compiler.staqex.hir` (`HirModule`, `build_hir` from
  TypeChecker) exposing immutable symbols + typed map. Evaluator unwired;
  no phase/effects/provenance yet (B–D). No big-bang pipeline rewrite.
- Specs: plan approval (“承認”); PR #113 merged (`168315b`).
- Verification: suite must fail before Green on missing hir module/API.

## Delivered

- `tests/test_hir_slice_a_red.py`

## Expected Red

`ModuleNotFoundError: No module named 'compiler.staqex.hir'` (or missing
`HirModule` / `build_hir`).

## Next safe action

Adjudicator Red approval → Slice A Phase 2 Green.
