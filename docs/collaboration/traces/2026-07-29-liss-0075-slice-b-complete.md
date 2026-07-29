# Trace: LISS-0075 Slice B complete

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0075 |
| Slice | B — `LINEAR_IMPLICIT_DISCARD` + ancilla lifetime |
| Phase | Red → Green → Refactor **complete** |
| Branch | `feature/liss-0075-linear-quantum-usage` |

## Delivered

- `tests/test_linear_usage_slice_b_red.py`
- `compiler/staqex/hir.py` — track introduced State roots; emit
  `LINEAR_IMPLICIT_DISCARD` for roots unconsumed at block exit

## Expected Red (before Green)

Assertion failure: `LINEAR_IMPLICIT_DISCARD` absent (`got []`)

## Verification after Refactor

```
PASS Slice A (3)
PASS Slice B (3)
```

## Next safe action

Slice C plan approval — uncomputation witness + `HirDecl.effects` `"Uncompute"`.
