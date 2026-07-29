# Trace: LISS-0114 Slice D complete

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0114 |
| Slice | D — DensityState linear carrier set (R4) |
| Phase | plan gate → Red → Green → Refactor **complete** |
| Branch | `feature/liss-0114-slice-a` |
| Approval | Adjudicator「Dへ。承認」 |

## Delivered

- `LINEAR_CARRIER_KINDS = {State, DensityState}`
- `is_linear_carrier_ty(ty)` — State **or** Object/DensityState env encoding
- `_is_state_binding` uses `is_linear_carrier_ty` (module-symbol widen)
- `tests/test_linear_hardening_slice_d_red.py` — discard / alias / measure

## Expected Red (before Green)

Missing `LINEAR_CARRIER_KINDS` / `is_linear_carrier_ty`

## Verification

```
PASS LISS-0114 Slice A–D
PASS LISS-0075 Slice A–D
```

## Note

`lindblad(rho, …)` still does **not** consume `rho` (B12 may report
`LINEAR_IMPLICIT_DISCARD` on unused sources). Expanding consume for channel
calls is out of Slice D (possible follow-up on consume-set / Slice E–F).

## Next safe action

Adjudicator **Slice E plan gate** (R6 control-flow lifetime), or commit/PR.
