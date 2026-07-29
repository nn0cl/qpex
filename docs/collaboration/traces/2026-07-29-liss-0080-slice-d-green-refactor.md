# Trace: LISS-0080 Slice D Green + Refactor (Issue closeout)

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0080 |
| Slice | D — provenance + HIR verifier + closeout |
| Phase | phase-2-green + phase-3-refactor + issue-complete |
| Branch | `feature/liss-0080-slice-d-red` |

## Delivered

- `compiler/qpex/hir.py`:
  - `HirSpan(line, col)` — decl-level source location
  - `HirDecl.span: HirSpan | None` from AST decl spans via optional `unit`
  - `build_hir(..., unit=...)` — optional `CompilationUnit` for span extraction
  - `verify_hir(module)` — lightweight invariant checker (phase + effects)

## Verification

- `python3 tests/test_hir_slice_a_red.py` — PASS
- `python3 tests/test_hir_slice_b_red.py` — PASS
- `python3 tests/test_hir_slice_c_red.py` — PASS
- `python3 tests/test_hir_slice_d_red.py` — PASS

## Issue status

**LISS-0080 complete.** LISS-0075 (linear usage) is now unblocked.

## Next safe action

- Merge PR for Slice D.
- Create LISS-XXXX for PalQuantum / `.pq` rename (deferred per Adjudicator).
- Begin LISS-0075 or next dependency.
