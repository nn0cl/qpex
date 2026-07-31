# ADR 0145: Imperial mass scale `lb` ↔ `kg`

## Status

**Accepted** (2026-07-31) — unlocks LISS-0177 under WP-0051.
Extends [ADR 0136](0136-gram-kilogram-scale.md).
Companions: [ADR 0124](0124-si-scale-conversion-explicit.md).

## Decisions

1. ASCII suffix `.lb` denotes the international **avoirdupois pound** on Dim
   Mass.
2. Explicit `expr to unit` converts with the exact factor
   \(1\,\mathrm{lb} = 0.45359237\,\mathrm{kg}\) (1959 international yard and
   pound agreement).
3. Conversions among `.lb` / `.g` / `.kg` share the kilogram scale canonical.
4. Bare `.lb` stays raw; no stone or implicit mixed Mass arithmetic.
   (Ounce: [ADR 0146](0146-imperial-ounce-mass.md).)

## Deferred

Stone; tonne; atomic mass unit; implicit mixed-unit arithmetic.
