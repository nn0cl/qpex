# Trace: LISS-0114 Slice B complete

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0114 |
| Slice | B — consume-set (R1) + measure-reuse (R3) |
| Phase | plan gate → Red → Green → Refactor **complete** |
| Branch | `feature/liss-0114-slice-a` |
| Approval | Adjudicator「承認」(Slice B plan gate) |

## Delivered

- `tests/test_linear_hardening_slice_b_red.py`
- `compiler/staqex/hir.py` — `LINEAR_CONSUME_KINDS` =
  `{measure, static_uncompute_zero_reset}`; docstring clarifies gate
  non-consume
- Issue consume-set policy table; R3 second-measure Red (coexists with
  `EARLY_COLLAPSE_ERROR`)

## Expected Red (before Green)

Missing `LINEAR_CONSUME_KINDS` export

## Verification

```
PASS LISS-0114 Slice A–B
PASS LISS-0075 Slice A–D
```

## Next safe action

Adjudicator **Slice C design gate** (R2: keep strict alias vs allow rename),
or commit/PR for A–B (+0075 residuals on branch).
