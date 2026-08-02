# LISS-0273: Kernel Red — classical Call in expression (ADR 0179)

## Metadata

- Local issue ID: LISS-0273
- GitHub issue: https://github.com/nn0cl/staqex/issues/282
- Status: **complete** (2026-08-02) — Red → Green
- Type: Feature Path
- Priority: P1 (good first Kernel ship of Wave C — smallest surface)
- ADR: [0179](../architecture/adr/0179-classical-call-in-expr.md) (**Accepted**)
- Program: WP-0088
- Parent: LISS-0269

## Intent

Allow pure classical Calls/method results as operands in classical arithmetic
without mandatory temps. Reject State/Joint-forming Calls as classical operands.

## Exit

- [x] Red: `c.get() * 0.4` / `twice(x) + y` failed pre-Green
- [x] Green: `_eval_classical_call` / `_eval_classical_method_call` in evaluator
- [x] Negative: `coin() * 0.5` still fails
- [x] Tests: `tests/test_liss_0273_classical_call_in_expr_red.py`
