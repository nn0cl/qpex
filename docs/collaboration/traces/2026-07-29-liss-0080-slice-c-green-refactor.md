# Trace: LISS-0080 Slice C Green + Refactor

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0080 |
| Slice | C — effects / capabilities on HIR decls |
| Phase | phase-2-green + phase-3-refactor |
| Branch | `feature/liss-0080-slice-c-red` |

## Delivered

- `compiler/qpex/hir.py`: `HirDecl.effects: frozenset[str]` from
  `TypeChecker.fun_effects`; scope decls and `main` → `frozenset()`

## Policy (confirmed by Adjudicator)

- Only explicit `effects {…}` declarations recorded on HIR.
- `main` implicit full-effects permission deferred to execution-phase ADR.

## Verification

- `python3 tests/test_hir_slice_a_red.py` — PASS
- `python3 tests/test_hir_slice_b_red.py` — PASS
- `python3 tests/test_hir_slice_c_red.py` — PASS

## Next safe action

Slice D plan (provenance + HIR verifier) for Adjudicator review.
