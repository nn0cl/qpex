# LISS-0304: Soft QSEM teaching + exhaustive closed-enum `when`

## Metadata

- Local issue ID: LISS-0304
- Status: **complete** (2026-08-03)
- Type: Feature Kernel residual + docs
- Priority: P1
- Depends: language re-review P1 follow-on after LISS-0303
- Branch: `feature/liss-0304-soft-qsem-exhaustive-when`
- Out: multi-bind sugar ADR (still pending separate Architecture Accept)

## Summary

1. **Docs:** teach soft `QSEM_*` vs hard `HARD_CODES` (re-review P2-4).
2. **Kernel:** closed-enum `when` without `else` must cover every variant
   (`WHEN_NONEXHAUSTIVE` hard). Incomplete arms previously measured **vacuum**
   silently — fail closed (re-review P1-4 honesty).

## Exit

- [x] QUICKSTART soft QSEM note
- [x] Typecheck + HARD_CODES
- [x] Tests (incomplete / exhaustive / else)
- [x] S01 seed-0 still green
