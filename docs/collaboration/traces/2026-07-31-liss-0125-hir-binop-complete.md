# Trace: LISS-0125 HIR BinOp expr children

- Date: 2026-07-31
- Branch: `feature/liss-0125-hir-binop-children`
- Approval: Adjudicator 「承認」 (next after #171/#172 merge)
- Fix: `hir._expr_children` uses `BinOp.lhs`/`rhs`; walks `TensorExpr`
- Suite: `tests/test_liss_0125_hir_binop_expr_children_red.py` (3/3)
- B03/A01: no longer crash; remaining red is LINEAR (LISS-0122/0123)
