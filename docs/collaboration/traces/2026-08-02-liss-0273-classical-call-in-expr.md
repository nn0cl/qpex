# AI work trace — LISS-0273 classical Call in expr

| Field | Value |
|---|---|
| Date | 2026-08-02 |
| ADR | 0179 Accepted |
| Issue | LISS-0273 / #282 |

## Change

Evaluator: `_eval_classical_call` / `_eval_classical_method_call` so pure
classical Calls may appear as operands in classical BinOps (ADR 0179).

## Verification

`PYTHONPATH=. pytest tests/test_liss_0273_classical_call_in_expr_red.py` — 3 passed
