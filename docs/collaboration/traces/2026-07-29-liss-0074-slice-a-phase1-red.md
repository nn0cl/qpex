# Trace: LISS-0074 Slice A Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0074 |
| Slice | A — qutrit/qudit type surface |
| Phase | phase-1-red |
| Branch | `feature/liss-0074-slice-a-red` |
| Implementation | **forbidden** until Red approval → Green |

## [DESIGN CHECK]

- Scope: Red for valid `Qutrit`/`Qudit<D>`/registers; reject `D=0`, bad arity,
  nonpositive `N`; EBNF note. No label checks (B) / acting-space (C).
- Specs: plan approval with recommended defaults.
- Verification: suite must fail before Green.

## Delivered

- `tests/test_qudit_slice_a_red.py`
- Issue / plan / WP / register → Slice A Red

## Expected Red

`Qudit<0>` and arity mismatches currently compile without
`LOCAL_DIMENSION_TYPE_ERROR`; EBNF lacks qutrit/qudit docs.

## Next safe action

Adjudicator Red approval → Slice A Phase 2 Green.
