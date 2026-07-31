# LISS-0184: Tuple multi-hole pipe / Fusion fill

## Metadata

- Local issue ID: LISS-0184
- Status: **complete**
- ADR: [0152](../architecture/adr/0152-tuple-multi-hole-fusion.md)
- Program: [WP-0058](../work-plans/WP-0058-tuple-multi-hole-fusion.md)
- Tests: `tests/test_tuple_multi_hole_fusion_red.py`

## Exit

- [x] `(a,b) |> f(_, _)` completes
- [x] Tuple + multi-hole Partial completes
- [x] Peeled tuple head still fuses with later unary stages
- [x] One-hole Fusion regression green
