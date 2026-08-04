# AI work trace: LISS-0313 finiteize surface

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `feature/liss-0313-finiteize-surface` |
| Issue | [LISS-0313](../../architecture/documentation-compression-map.md) |
| ADR | [0185](../../architecture/decision-themes/dec-0004-type-first-scientific-model.md) Lane A |

## Done

- Prelude `finiteize` combinator
- Evaluator `_bind_finiteize` → Host equal-width histogram (uniform on `[lo,hi)`)
- Typecheck: Call returns State
- Tests: `tests/test_liss_0313_finiteize_surface_red.py`
- Example: `examples/basics/B18_finiteize/`

## Surface

```text
state psi = finiteize(lo, hi, n_bins, n_samples[, seed])
```

## Verification

```bash
.venv/bin/python -m pytest tests/test_liss_0313_finiteize_surface_red.py -q
# 4 passed

python3 -m compiler.staqex run --seed 0 \
  examples/basics/B18_finiteize/finiteize_surface.sqx
```
