# Trace: LISS-0080 Slice B Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0080 |
| Slice | B — declaration phase on HIR decls |
| Phase | phase-1-red |
| Branch | `feature/liss-0080-slice-b-red` |
| Implementation | **forbidden** until Red approval → Green |

## [DESIGN CHECK]

- Scope: Red for `HirDecl` + `HirModule.declarations` with phase from
  LISS-0034 scope `kind`; optional `scope_contracts` on `build_hir`;
  unscoped `main` → `kernel`. No effects (C), provenance (D), 0076.
- Specs: Slice B plan approval (“承認”); Slice A on `main` via PR #114.
- Verification: suite must fail before Green on missing decl phases.

## Delivered

- `tests/test_hir_slice_b_red.py`

## Expected Red

Missing `HirDecl`, `HirModule.declarations`, or phase fields until Green.

## Next safe action

Adjudicator Red approval → Slice B Phase 2 Green.
