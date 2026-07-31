# ADR 0150: US short ton / UK long ton mass scales

## Status

**Accepted** (2026-07-31) — unlocks LISS-0182 under WP-0056.
Extends [ADR 0145](0145-imperial-pound-mass.md) /
[ADR 0148](0148-tonne-mass.md).

## Decisions

1. ASCII suffix `.ton_us` denotes the US customary **short ton** on Dim Mass.
2. ASCII suffix `.ton_uk` denotes the UK **long ton** on Dim Mass.
3. Exact relations via the international avoirdupois pound:
   \(1\,\mathrm{ton\_us} = 2000\,\mathrm{lb}\),
   \(1\,\mathrm{ton\_uk} = 2240\,\mathrm{lb}\).
4. Conversions among `.ton_us` / `.ton_uk` / `.t` / `.st` / `.lb` / `.oz` /
   `.g` / `.kg` share the kilogram scale canonical.
5. Metric tonne remains `.t` only ([ADR 0148](0148-tonne-mass.md)). Bare
   suffixes stay raw; no bare `.ton` alias; no troy; no implicit mixed Mass
   arithmetic.

## Deferred

Troy ounce; atomic mass unit; bare `.ton` disambiguation; implicit mixed-unit
arithmetic. (Troy shipped: [ADR 0151](0151-troy-ounce-mass.md).)
