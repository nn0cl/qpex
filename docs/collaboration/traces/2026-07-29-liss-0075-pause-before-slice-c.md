# Trace / handoff: LISS-0075 pause before Slice C

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0075 |
| Phase | **paused** after Slice B; Slice C not started |
| Branch | `feature/liss-0075-linear-quantum-usage` |

## Current State

- Current phase: Feature Path paused — Adjudicator will re-read A/B source
  before Slice C.
- Scope completed: Slice A (`LINEAR_DUPLICATE_USE`), Slice B
  (`LINEAR_IMPLICIT_DISCARD`).
- Out of scope until risk review: Slice C uncomputation / evaluator coupling;
  Slice D pipeline wiring.

## Completed

- `compiler/staqex/hir.py` — `HirLinearVerifier`
- `tests/test_linear_usage_slice_a_red.py`
- `tests/test_linear_usage_slice_b_red.py`
- Issue Open risks table **R1–R8** parked for review

## Changed Files (this pause)

- `docs/issues/LISS-0075-linear-quantum-usage.md` — paused + R1–R8
- `docs/architecture/open-work-register.md` — status **paused**
- this trace

## Next Safe Action

1. Adjudicator reads `compiler/staqex/hir.py` (+ Slice A/B tests) with fresh eyes.
2. Mark each of R1–R8: accept as-is / change before C / split to follow-up LISS.
3. Only then grant Slice C plan approval.

## Blockers

- Slice C/D intentionally blocked on risk review (not a technical failure).
