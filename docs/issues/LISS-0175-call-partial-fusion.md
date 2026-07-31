# LISS-0175: Call / Partial pipe Fusion MVP

## Metadata

- Local issue ID: LISS-0175
- Status: **complete**
- ADR: [0143](../architecture/adr/0143-call-partial-pipe-fusion-mvp.md)
- Program: [WP-0049](../work-plans/WP-0049-call-partial-fusion.md)
- Tests: `tests/test_call_partial_fusion_red.py`

## Exit

- [x] `z |> add(10, _) |> dbl` matches sequential Calls
- [x] Partial var `z |> p |> dbl` matches the same denotation
- [x] Bare unary Fusion (ADR 0137/0141) still works
