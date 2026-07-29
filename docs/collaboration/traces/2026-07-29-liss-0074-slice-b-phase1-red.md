# Trace: LISS-0074 Slice B Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0074 |
| Slice | B — ket/bra label vs local dimension |
| Phase | phase-1-red |
| Branch | `feature/liss-0074-slice-b-red` |
| Implementation | **forbidden** until Red approval → Green |

## [DESIGN CHECK]

- Scope: Red for `0 ≤ k < D` on `State<Qutrit>` / `State<Qudit<D>>`; alone ket
  unchanged; exclude C/D/E.
- Specs: Slice B plan approval; probe `|3⟩` on Qutrit still ok.
- Verification: suite must fail before Green.

## Delivered

- `tests/test_qudit_slice_b_red.py`

## Expected Red

Out-of-range `|3⟩` / `|4⟩` / bra `⟨3|` accepted without
`LOCAL_DIMENSION_TYPE_ERROR`.

## Next safe action

Adjudicator Red approval → Slice B Phase 2 Green.
