# AI work trace: LISS-0295 selective import transitive free-fn

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `feature/liss-0295-selective-import-transitive-freefn` |
| Issue | [LISS-0295](../../architecture/documentation-compression-map.md) |

## Done

- `modules.py`: expand selective import sets with same-unit free-fn callees
  of selected free-fns (pub/module/package).
- S01 domain: restore nested free-fn composition (roads / shelters / hazards /
  requests / recovery) — undo LISS-0294 inlines.
- Tests: `tests/test_liss_0295_selective_import_transitive_freefn_red.py`
- seed-0 spine / morning / day2 green; `hazard_cell_pressure` linked when only
  `secondary_pressure` is imported.

## Verification

```bash
.venv/bin/python -m pytest \
  tests/test_liss_0295_selective_import_transitive_freefn_red.py \
  tests/test_liss_0294_nested_freefn_args_red.py \
  tests/test_liss_0271_0272_import_lane_red.py -q
python3 -m compiler.staqex run --seed 0 \
  examples/showcase/S01_quantum_disaster_response/main_disaster_response.sqx
```
