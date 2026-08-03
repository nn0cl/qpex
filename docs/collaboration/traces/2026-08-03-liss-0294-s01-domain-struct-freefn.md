# AI work trace: LISS-0294 S01 domain struct + free-fn

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `feature/liss-0294-s01-domain-struct-freefn` |
| Issue | [LISS-0294](../../architecture/documentation-compression-map.md) |

## Done

- Domain demote: roads, shelters, morning, recovery, requests, hazards →
  struct + free scores.
- Mains: spine / morning / day2 free-fn call sites + imports.
- Kernel residual (`evaluator.py`):
  - nested classical free-fn receives parent `assign`
  - Attr field read prefers free-fn locals over outer `self.objects`
- Outer board scores inline leaf formulas (ADR 0177 selective import does not
  transitively link sibling free-fns).
- Tests: `tests/test_liss_0294_nested_freefn_args_red.py` (3 cases).
- seed-0 green on S01 mains (incl. disaster / morning / day2).

## Verification

```bash
.venv/bin/python -m pytest tests/test_liss_0294_nested_freefn_args_red.py \
  tests/test_liss_0292_typefirst_freefn_args_red.py -q
python3 -m compiler.staqex run --seed 0 \
  examples/showcase/S01_quantum_disaster_response/main_disaster_response.sqx
python3 -m compiler.staqex run --seed 0 \
  examples/showcase/S01_quantum_disaster_response/main_morning_collect.sqx
python3 -m compiler.staqex run --seed 0 \
  examples/showcase/S01_quantum_disaster_response/main_day2_recovery.sqx
```
