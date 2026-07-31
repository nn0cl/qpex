# LISS-0133: Accepted-surface expression residuals

## Metadata

- Local issue ID: LISS-0133
- Status: **complete** — 2026-07-31
- Phase: Feature Path Phase 3 (with LISS-0129 packet)
- Type: language residual close-out
- Priority: P0 (expression completeness before S1)
- Depends on: LISS-0129 typed surface
- ADR: [0116](../architecture/adr/0116-classical-quantity-state-arithmetic.md)
- Tests: `tests/test_expression_residuals_red.py`

## Summary

Close accepted-surface residuals from LISS-0122/0123 heals:

- consume-on-return / user-fn move + `apply` arg consume
- `Float` / classical function returns
- soft `MULTI_REGISTER_INDEX_AMBIGUOUS` false positive on qualified sites
- Classical Type-First quantities ⊕ State dimensional arithmetic

## Exit

- [x] Residuals fixed with Red suite green
- [x] ADR 0116 Accepted
- [x] B15 multi-register green without MULTI false positive
