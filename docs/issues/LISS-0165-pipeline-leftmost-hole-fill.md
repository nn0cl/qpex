# LISS-0165: Pipeline leftmost hole fill

## Metadata

- Local issue ID: LISS-0165
- Status: **complete**
- ADR: [0133](../architecture/adr/0133-pipeline-leftmost-hole-fill.md)
- Program: [WP-0041](../work-plans/WP-0041-pipe-hole-celsius.md)
- Tests: `tests/test_pipeline_leftmost_hole_red.py`

## Exit

- [x] `w |> second(z, _)` ≡ `second(z, w)`
- [x] `x |> f(_, _)` yields unary Partial
