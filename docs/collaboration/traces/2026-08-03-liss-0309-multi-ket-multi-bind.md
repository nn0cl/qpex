# AI work trace: LISS-0309 multi-ket multi-bind

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `feature/liss-0309-multi-ket-multi-bind` |
| Issue | [LISS-0309](../../issues/LISS-0309-multi-ket-multi-bind.md) |

## Done

- `hir._check_multi_state_bind` + tuple item linear introduction
- `evaluator._bind_names` TupleExpr → sequential `_bind`
- B08 multi-ket face
- Tests: `tests/test_liss_0309_multi_ket_multi_bind_red.py`

## Verification

```bash
.venv/bin/python -m pytest \
  tests/test_liss_0309_multi_ket_multi_bind_red.py \
  tests/test_liss_0305_classical_multi_bind_red.py \
  tests/test_qasm3_codegen.py::test_trotter_ising_evolve_qasm -q
python3 -m compiler.staqex run --seed 0 \
  examples/basics/B08_operators_hamiltonians/operators_hamiltonians.sqx
```
