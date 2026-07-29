# Trace: LISS-0114 Slice C complete (R2 strict alias lock)

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0114 |
| Slice | C — alias rename design gate (R2) |
| Phase | design gate **complete** (no rename implementation) |
| Branch | `feature/liss-0114-slice-a` |
| Approval | Adjudicator「承認」— keep **strict** alias |

## Decision

`State alias = q` remains `LINEAR_DUPLICATE_USE`. Silent rename / move is
**not** authorized. Future rename would need an explicit override Issue.

## Delivered

- `compiler/staqex/hir.py` — `LINEAR_ALIAS_POLICY = "strict"`
- `tests/test_linear_hardening_slice_c_red.py` — policy lock + behavior lock
- Issue alias-policy section; R2 closed-accepted

## Verification

```
PASS LISS-0114 Slice A–C
```

## Next safe action

Adjudicator **Slice D plan gate** (DensityState module-symbol linear set),
or commit/PR for A–C (+0075 on branch).
