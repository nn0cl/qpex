# AI work trace: LISS-0299 residual selective import

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `feature/liss-0299-residual-selective-import` |
| Issue | [LISS-0299](../../issues/LISS-0299-residual-selective-import.md) |

## Done

- B09 + S01 bare imports → selective braces
- `compose.sqx` free-fns `pub`
- `modules._collect_free_call_names`: bare `Pipe` unary stages
- Test: `test_selective_import_bare_pipe_stage_transitive`

## Verification

```bash
.venv/bin/python -m pytest tests/test_liss_0295_selective_import_transitive_freefn_red.py -q
python3 -m compiler.staqex run --seed 0 \
  examples/basics/B09_multi_file_modules/main_multi_file_modules.sqx
python3 -m compiler.staqex run --seed 0 \
  examples/showcase/S01_quantum_disaster_response/main_disaster_response.sqx
```
