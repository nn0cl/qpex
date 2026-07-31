# Trace: LISS-0136 sparse Pauli Operator return

- Date: 2026-07-31
- Branch: `feature/liss-0136-sparse-pauli-operator-return`
- After: PR #179 merged (Showcase S1)
- Approval: Adjudicator 「1.承認その後2に着手」
- Root cause: Operator factory resolve copied AST with unbound `OpVar`
  coeffs (`J`, `h`) instead of folding factory-local `Float` binds
- Fix: `materialize_op_scalar_vars` + factory scalar capture in
  `_resolve_operator_expr`
- Tests: `tests/test_sparse_pauli_operator_return_red.py` green;
  showcase S1 still green with physics factory return
