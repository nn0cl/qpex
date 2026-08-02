# AI work trace — WP-0081 LISS-0234 Dirac paper Var sugar

| Field | Value |
|---|---|
| Date | 2026-08-02 |
| Branch | `batch/wp-0081-dirac-sugar-red` |
| Issue | LISS-0234 |
| Ship ADR | 0169 |

## Change

- Parser: identifier-shaped Dirac interiors in `inner`/`outer`/`projector`
  Calls desugar to `Var`; numeric/`+`/`-` stay BraLit/KetLit.
- Red suite `tests/test_liss0234_dirac_paper_var_sugar_red.py`.
- Friction ledger F-04 updated to sugar-shipped.

## Verification

`.venv/bin/pytest tests/` → 1068 passed / 0 failed.
