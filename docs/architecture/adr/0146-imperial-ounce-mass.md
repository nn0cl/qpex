# ADR 0146: Imperial mass scale `oz` ↔ `kg` / `lb`

## Status

**Accepted** (2026-07-31) — unlocks LISS-0178 under WP-0052.
Extends [ADR 0145](0145-imperial-pound-mass.md).

## Decisions

1. ASCII suffix `.oz` denotes the international **avoirdupois ounce** on Dim
   Mass.
2. Exact relation \(1\,\mathrm{lb} = 16\,\mathrm{oz}\), hence
   \(1\,\mathrm{oz} = 0.45359237/16\,\mathrm{kg}\).
3. Conversions among `.oz` / `.lb` / `.g` / `.kg` share the kilogram scale
   canonical.
4. Bare `.oz` stays raw; no stone, troy ounce, or implicit mixed Mass
   arithmetic.

## Deferred

Stone; tonne; troy ounce; atomic mass unit; implicit mixed-unit arithmetic.
