# Trace: WP-0075 Regression clusters LISS-0204..0207

| Field | Value |
|---|---|
| Date | 2026-08-01 |
| Program | WP-0075 |
| Issues | LISS-0204, LISS-0205, LISS-0206, LISS-0207 |
| Branch | `batch/wp-0075-regression-clusters-0204-0207` |

## Reason

Adjudicator「はい」 after WP-0074 merge: continue top-down with regression
clusters 0204–0207.

## Changes

- `parser.py`: `_ALGEBRA_EXPR_CALLEES` for `Operator A = adjoint(…)`; `{A,B}`
  anticommutator before bare-block `let`; `_peek_at`
- Suites: OOP `-> Float`; SI `to bob`; evolve drop unused `coin`; foreach QASM
  regex; operator algebra uncompute; Dirac F/G list assert parse-only

## Verification

Named batch suites: 60 passed (`.venv/bin/pytest` on the Issue file list).
