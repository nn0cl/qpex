# AI work trace: LISS-0297 Operator free-fn struct coeffs

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `feature/liss-0297-operator-freefn-struct-coeffs` |
| Issue | [LISS-0297](../../architecture/documentation-compression-map.md) |

## Done

- `evaluator._resolve_operator_factory_call`: object params → local_objects;
  OpAttr materialize; intermediate Float from param fields.
- S01: ConstraintDrive / Lattice demoted to free Operator factories.
- Tests: `tests/test_liss_0297_operator_freefn_struct_coeffs_red.py`
- Friction ledger + WP-0089 residual note

## Verification

```bash
.venv/bin/python -m pytest tests/test_liss_0297_operator_freefn_struct_coeffs_red.py -q
python3 -m compiler.staqex run --seed 0 \
  examples/showcase/S01_quantum_disaster_response/main_disaster_response.sqx
python3 -m compiler.staqex run --seed 0 \
  examples/showcase/S01_quantum_disaster_response/main_day2_recovery.sqx
python3 -m compiler.staqex run --seed 0 \
  examples/showcase/S01_quantum_disaster_response/main_lattice_four.sqx
```
