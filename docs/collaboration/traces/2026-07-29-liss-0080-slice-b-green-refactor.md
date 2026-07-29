# Trace: LISS-0080 Slice B Green + Refactor

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0080 |
| Slice | B — declaration phase on HIR decls |
| Phase | phase-2-green + phase-3-refactor |
| Branch | `feature/liss-0080-slice-b-red` |

## Delivered

- `compiler/staqex/hir.py`: `HirDecl`, `HirModule.declarations`,
  `build_hir(..., scope_contracts=...)`
- `compiler/staqex/typecheck.py`: `has_entry_main` for kernel `main` phase
- `tests/test_hir_slice_b_red.py`: immutability assertion fix (direct assign)

## Verification

- `python3 tests/test_hir_slice_a_red.py` — PASS
- `python3 tests/test_hir_slice_b_red.py` — PASS

## Next safe action

Slice C plan (effects / capabilities on HIR) for Adjudicator review.
