# ADR 0136: Mass scale `g` ↔ `kg`

## Status

**Accepted** (2026-07-31) — unlocks LISS-0168 under WP-0042.
Companions: [ADR 0124](0124-si-scale-conversion-explicit.md),
[ADR 0129](0129-si-scale-catalog-wave2.md).

## Decisions

1. Add unit suffix `.g` (gram) on Dim Mass.
2. Explicit `expr to unit` converts with \(1\,\mathrm{g} = 10^{-3}\,\mathrm{kg}\).
3. Bare `.g` / `.kg` stay raw magnitudes.
4. No ounce / stone / tonne in this ADR.

## Deferred

Ounce; stone; tonne; atomic mass unit.
(Imperial pound: [ADR 0145](0145-imperial-pound-mass.md).)
