# AI work trace: LISS-0305 classical multi-bind

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `feature/liss-0305-classical-multi-bind` |
| Issue | [LISS-0305](../../issues/LISS-0305-classical-multi-bind.md) |
| ADR | 0184 |

## Done

- Parser: `name, name = expr, expr` → TupleExpr RHS
- Evaluator: classical multi-scalar bind path
- B08: `J, h = 1.0, 0.5`
- Tests: `tests/test_liss_0305_classical_multi_bind_red.py`

## Note

Linear multi-ket `s0, s1 = |+>, |+>` remains deferred; use separate
`state s0 = |+>` lines or product evolve binds.

## Verification

```bash
.venv/bin/python -m pytest tests/test_liss_0305_classical_multi_bind_red.py -q
python3 -m compiler.staqex run --seed 0 \
  examples/basics/B08_operators_hamiltonians/operators_hamiltonians.sqx
```
