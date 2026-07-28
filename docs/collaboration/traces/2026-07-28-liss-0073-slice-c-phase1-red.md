# Trace: LISS-0073 Slice C Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0073 |
| Slice | C — `⟨φ|A|ψ⟩` matrix element |
| Phase | phase-1-red |
| Branch | `feature/liss-0073-slice-c-red` |
| Implementation | **forbidden** |

## [DESIGN CHECK]

- Scope: failing tests for `⟨0|X|1⟩` → `Call(inner, [BraLit, Call(X, [KetLit])])`,
  state-middle algebra error, Slice B regression, EBNF `bra_op_ket`.
- Specs: Slice C plan approval; lexer evidence BRA+IDENT+KET.
- Boundaries: no outer/`†`/brackets; no production code.
- Verification: run Red script; expect PARSE_ERROR on matrix element.

## Delivered

- `tests/test_dirac_slice_c_red.py`

## Verification

- `python3 tests/test_dirac_slice_c_red.py`
- Expected Red: `PARSE_ERROR` (BRA+IDENT+KET not folded into `inner`).

## Next safe action

Adjudicator Red approval → Slice C Phase 2 Green.
