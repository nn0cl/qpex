# Trace: LISS-0073 Slice F Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0073 |
| Slice | F — `[A,B]` / `{A,B}` brackets |
| Phase | phase-1-red |
| Branch | `feature/liss-0073-slice-f-red` |
| Implementation | **forbidden** until Red approval → Green |

## [DESIGN CHECK]

- Scope: Red for Operator `[X,Y]`/`{X,Y}` → `Call(commutator|anticommutator)`;
  expr `ListExpr` preserved; expr `{X,Y}` → anticommutator; EBNF note.
- Specs: Slice F plan approval (recommended disambiguation).
- Verification: suite must fail before Green.

## Delivered

- `tests/test_dirac_slice_f_red.py`
- Issue / plan / open-work-register → Slice F Red

## Expected Red

`PARSE_ERROR` on `Operator C = [X, Y]` (OpDSL / block recovery) and on
expression `{X, Y}`.

## Next safe action

Adjudicator Red approval → Slice F Phase 2 Green.
