# LISS-0173: Algebraic Operator Fusion MVP (affine)

## Metadata

- Local issue ID: LISS-0173
- Status: **complete**
- ADR: [0141](../architecture/adr/0141-algebraic-operator-fusion-mvp.md)
- Program: [WP-0047](../work-plans/WP-0047-algebraic-operator-fusion.md)
- Tests: `tests/test_algebraic_operator_fusion_red.py`

## Exit

- [x] `(s+10)*2-5` parses as affine `(2, 15)`
- [x] `z |> add10 |> dbl |> sub5` measures like sequential calls
- [x] Non-affine `when` returns still fuse via ADR 0137 multi-pass
