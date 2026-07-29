# Trace: LISS-0114 Slice E complete

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0114 |
| Slice | E — when / nested-block lifetime (R6) |
| Phase | plan gate → Red → Green → Refactor **complete** |
| Branch | `feature/liss-0114-slice-a` |
| Approval | Adjudicator「E 承認」 |

## Delivered

- Nested `forEach` / `dynamic qpu` bodies analyzed (inner discard surfaces)
- `when (ctrl)` consumes scrutinee + Vars in arm expressions
- `inspect(x)` counts as linear use of `x`
- `tests/test_linear_hardening_slice_e_red.py`
- Example B02 (`when_not_if`) compiles clean under linear hard-fail

## Expected Red (before Green)

`forEach` inner leftover → no `LINEAR_IMPLICIT_DISCARD` (`got []`)

## Verification

```
PASS LISS-0114 Slice A–E
PASS LISS-0075 Slice A–D
B02 ok True
```

## Next safe action

Adjudicator **Slice F plan gate** (runtime uncompute / tolerance ADR), or
commit/PR for A–E (+0075 on branch).
