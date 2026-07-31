# LISS-0181: Multi-hole Partial pipe fill

## Metadata

- Local issue ID: LISS-0181
- Status: **complete**
- ADR: [0149](../architecture/adr/0149-multi-hole-partial-pipe.md)
- Program: [WP-0055](../work-plans/WP-0055-multi-hole-partial-pipe.md)
- Tests: `tests/test_multi_hole_partial_pipe_red.py`

## Exit

- [x] Bare Partial with \(n>1\) holes accepted as pipe stage
- [x] One fill → Partial `#n-1`; final fill → State
- [x] Inline `x |> f(a,_,_)` then `y |> q` evaluates
- [x] One-hole Partial pipe regression still green
- [x] Fusion eligibility unchanged (one-hole only)
