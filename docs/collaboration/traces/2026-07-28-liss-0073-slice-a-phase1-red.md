# Trace: LISS-0073 Slice A Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0073 |
| Slice | A — BraLit primary wiring |
| Phase | phase-1-red |
| Branch | `feature/liss-0073-slice-a-red` |
| Implementation | **forbidden** |

## [DESIGN CHECK]

- Scope and expected behavior: failing tests for first-class `BraLit`, alone
  bra parse/typecheck, and EBNF `primary` including `bra_lit`; no production
  implementation.
- Specifications and files inspected: LISS-0073 issue + plan; ADR 0087;
  `parser.py` `_primary` (KET only); `ast_nodes.KetLit`; `grammar/qpex.ebnf`
  (`bra_lit` lexical, absent from `primary`).
- Component boundaries: parser / AST / typecheck / EBNF only; no juxtaposition
  (Slice B+); no Physics IR.
- Applicable constraints: tests only; no `compiler/qpex/` changes in Red.
- Decisions: plan-approved first-class `BraLit`; alone bra bound like ket for
  Slice A primary acceptance (`state bra = ⟨0|`).
- Included AI context: approved plan defaults; omitted Slices B–G.
- Task routing: deterministic test edit + local script run.
- Verification plan: run Red script; expect ImportError / PARSE_ERROR /
  missing `bra_lit` in primary.

## Delivered

- `tests/test_dirac_slice_a_red.py`

## Verification

- `python3 tests/test_dirac_slice_a_red.py`
- Expected Red: failure before all PASS (BraLit missing and/or PARSE_ERROR
  and/or EBNF primary gap).

## Next safe action

Adjudicator Red approval → Slice A Phase 2 Green for `BraLit` + `_primary`
BRA wiring + EBNF `bra_lit` in `primary` + alone-bra typecheck only.
