# Trace: LISS-0117 Slice C + Issue closeout

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0117 |
| Slice | C — Equation/Unit assertions + catalog evidence |
| Branch | `feature/liss-0117-slice-c` |
| Approval | Adjudicator “承認” |

## Delivered

- `verify_golden_against_lowered` calls `verify_physics_equation` for nested
  Coefficient/Unit
- Catalog: oscillator row **lowered-IR evidence**; global oracle still gated
- Issue marked **complete**

## Verification

`test_physics_ir_goldens_slice_{a,b,c}_red.py` PASS

## Next

Adjudicator コミット／PR／merge.
