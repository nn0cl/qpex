# AI work trace: LISS-0304 soft QSEM + exhaustive when

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `feature/liss-0304-soft-qsem-exhaustive-when` |
| Issue | [LISS-0304](../../issues/LISS-0304-soft-qsem-exhaustive-when.md) |

## Done

- QUICKSTART: soft QSEM vs hard diagnostics
- `typecheck._check_when_enum_exhaustive` + enum Ty heads
- `WHEN_NONEXHAUSTIVE` in HARD_CODES
- Tests: `tests/test_liss_0304_when_nonexhaustive_red.py`

## Verification

```bash
.venv/bin/python -m pytest tests/test_liss_0304_when_nonexhaustive_red.py -q
python3 -m compiler.staqex run --seed 0 \
  examples/showcase/S01_quantum_disaster_response/main_disaster_response.sqx
```
