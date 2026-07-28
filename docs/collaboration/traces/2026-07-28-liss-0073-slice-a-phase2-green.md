# Trace: LISS-0073 Slice A Phase 2 Green

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0073 |
| Slice | A — BraLit primary wiring |
| Phase | phase-2-green |
| Branch | `feature/liss-0073-slice-a-red` |
| Tests modified | helper only: walk `MainDecl` not `FunDecl` (Red fixture defect) |

## [DESIGN CHECK]

- Scope: minimal Green for Slice A Red — `BraLit`, `_primary` BRA, EBNF
  `bra_lit` in `primary`, alone-bra typecheck as State carrier matching ket.
- Specs: approved LISS-0073 plan; Red suite.
- Boundaries: no juxtaposition, no evaluator bra bind, no Slice B+.
- Verification: `python3 tests/test_dirac_slice_a_red.py` PASS.

## Delivered

- `compiler/qpex/ast_nodes.py` — `BraLit` + `Expr` union
- `compiler/qpex/parser.py` — `TokenKind.BRA` → `BraLit`
- `compiler/qpex/typecheck.py` — `BraLit` infers `State<Qubit>` (Slice A alone)
- `docs/specs/grammar/qpex.ebnf` — `bra_lit` in `primary`
- `tests/test_dirac_slice_a_red.py` — MainDecl walk fix (behavior assertions unchanged)

## Verification

- `python3 tests/test_dirac_slice_a_red.py` PASS
- Note: `tests/test_operator_algebra_red.py` fails on `OPERATOR_DOMAIN_ERROR`
  with or without this Green (pre-existing; not introduced here).

## Next safe action

Adjudicator Green approval → Slice A Phase 3 Refactor (readability only).
