# ADR 0155: Mixed-unit `+`/`-` promote to canonical

## Status

**Accepted** (2026-07-31) — unlocks LISS-0187 under WP-0061.
**Supersedes** [ADR 0154](0154-mixed-unit-reject.md) reject-only policy.
Amends [ADR 0124](0124-si-scale-conversion-explicit.md) Decision 5.

## Decisions

1. When both operands of `+`/`-` (and relational checks) have **known** unit
   suffixes that share a **canonical family** (same entry in
   `UNIT_SCALE_TO_CANONICAL` or `UNIT_AFFINE_TO_CANONICAL`), automatically
   convert both magnitudes to that canonical unit, then apply the operator.
2. **Result unit** is the canonical unit (e.g. `kg`, `s`, `m`, `Hz`, `J`, `K`).
3. Same-unit operands stay raw in that unit (no forced canonicalization).
4. Explicit `expr to unit` remains available and sets the result unit to the
   target (unchanged).
5. Incompatible pairs (no shared canonical) still →
   `UNIT_MIXED_ARITHMETIC_ERROR`. Dim mismatch remains
   `DIMENSION_MISMATCH_ERROR`.
6. Type-First classical scalars track unit suffixes at runtime so `a + b`
   with mixed units promotes correctly.

## Non-goals

Choosing LHS/RHS display unit after promote; auto-rescale on `*`/`/` beyond
existing Dim algebra; inventing units for bare dimensionless numerics.

## Consequences

- `1.kg + 1.g` → `1.001` with unit `kg`.
- `0.C + 32.F` → `546.3` with unit `K`.
- ADR 0154 reject-for-all-mixed is withdrawn for shared-family pairs.
