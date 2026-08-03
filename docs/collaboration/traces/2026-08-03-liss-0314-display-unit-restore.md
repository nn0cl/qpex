# AI work trace: LISS-0314 display-unit restore

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `feature/liss-0314-display-unit-restore` |
| Issue | [LISS-0314](../../architecture/documentation-compression-map.md) |
| ADR | [0186](../../architecture/adr/0186-display-unit-restore.md) |

## Done

- `from_canonical_magnitude` (scale + affine inverse)
- Evaluator mixed `+`/`-`: canonical arithmetic then LHS unit restore
- Typecheck result unit = LHS for shared-family mixed promote
- Tests: LISS-0314 + updated ADR 0155 affine expectation
- Supersede LISS-0197

## Verification

```bash
.venv/bin/python -m pytest \
  tests/test_liss_0314_display_unit_restore_red.py \
  tests/test_mixed_unit_canonical_promote_red.py \
  tests/test_mixed_unit_reject_red.py -q
# 11 passed
```
