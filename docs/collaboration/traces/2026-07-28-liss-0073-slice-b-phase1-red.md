# Trace: LISS-0073 Slice B Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0073 |
| Slice | B — `⟨φ|ψ⟩` → `inner` |
| Phase | phase-1-red |
| Branch | `feature/liss-0073-slice-b-red` |
| Implementation | **forbidden** |

## [DESIGN CHECK]

- Scope: failing tests for north-star `⟨φ|ψ⟩` → `Call(inner, [BraLit, KetLit])`,
  alone-bra regression, pipeline vs ket-close collision, EBNF note.
- Specs: Slice B plan approval; clarification that source is single-bar
  `⟨φ|ψ⟩` (not `⟨φ||ψ⟩`).
- Boundaries: no matrix element / outer / `†` / brackets.
- Verification: run Red script; expect `LEX_ERROR` on `⟩` after bra.

## Delivered

- `tests/test_dirac_slice_b_red.py`

## Verification

- `python3 tests/test_dirac_slice_b_red.py`
- Expected Red: `LEX_ERROR` / assertion failure on juxtaposition parse.

## Next safe action

Adjudicator Red approval → Slice B Phase 2 Green.
