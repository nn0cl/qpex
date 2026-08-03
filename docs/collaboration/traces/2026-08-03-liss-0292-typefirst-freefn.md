# AI work trace: LISS-0292 Type-First free-fn args

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `feature/liss-0292-typefirst-freefn-args` |

## Fix

Classical Type-First-returning free functions no longer Joint-bind object
parameters; free-fn bodies execute intermediate classical binds; Attr field
units resolve from free-fn locals.

## Verification

tests/test_liss_0292_typefirst_freefn_args_red.py; sugar regression; B08 QASM
