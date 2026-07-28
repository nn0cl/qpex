# Trace: LISS-0073 Slice D Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0073 |
| Slice | D — outer / projector punctuation |
| Phase | phase-1-red |
| Branch | `feature/liss-0073-slice-d-red` |
| Implementation | **forbidden** |

## [DESIGN CHECK]

- Scope: failing tests for `|ψ⟩⟨φ|` → `outer`, matching labels → `projector`,
  alone ket regression, EBNF + OpHop note.
- Specs: Slice D plan approval; lexer already yields KET+BRA.
- Boundaries: no `†` / brackets; no production code.
- Verification: run Red script; expect PARSE_ERROR on ket–bra fold.

## Delivered

- `tests/test_dirac_slice_d_red.py`

## Verification

- `python3 tests/test_dirac_slice_d_red.py`
- Expected Red: `PARSE_ERROR` on `|0⟩⟨1|`.

## Next safe action

Adjudicator Red approval → Slice D Phase 2 Green.
