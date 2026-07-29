# Trace: LISS-0114 Slice A complete

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0114 |
| Slice | A — pipeline hard-fail (R5) + Gherkin rebaseline (R8) |
| Phase | plan intake → Red → Green → Refactor **complete** |
| Branch | `feature/liss-0114-slice-a` |
| Approval | Adjudicator「承認」(plan intake + R5 hard-fail + R2 strict defaults) |

## Delivered

- `tests/test_linear_hardening_slice_a_red.py`
- `compiler/staqex/pipeline.py` — `build_hir` after analyze; extend diags with
  `linear_diagnostics`; hard codes `LINEAR_DUPLICATE_USE`,
  `LINEAR_IMPLICIT_DISCARD`, `UNCOMPUTE_WITNESS_MISSING`
- LISS-0075 regression scaffolds: `compiled.ok` → unit+checker for programs
  that intentionally emit linear errors (hard-fail coupling)

## Expected Red (before Green)

`LINEAR_IMPLICIT_DISCARD` absent from `compile_source` diagnostics (`got set()`)

## Verification

```
PASS LISS-0114 Slice A (3)
PASS LISS-0075 Slice A–D
```

## Next safe action

Adjudicator **Slice B plan gate** (consume-set + R3), or commit/PR for A (+0075).
