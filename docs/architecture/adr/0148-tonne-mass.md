# ADR 0148: Metric tonne mass scale `t` ↔ `kg`

## Status

**Accepted** (2026-07-31) — unlocks LISS-0180 under WP-0054.
Extends [ADR 0136](0136-gram-kilogram-scale.md).
Companions: [ADR 0124](0124-si-scale-conversion-explicit.md).

## Decisions

1. ASCII suffix `.t` denotes the SI **metric tonne** (tonne) on Dim Mass.
2. Explicit `expr to unit` converts with \(1\,\mathrm{t} = 10^{3}\,\mathrm{kg}\).
3. Conversions among `.t` / `.kg` / `.g` / imperial mass suffixes share the
   kilogram scale canonical.
4. Bare `.t` stays raw; no short ton / long ton in this ADR; no implicit
   mixed Mass arithmetic. (US/UK tons: [ADR 0150](0150-us-uk-ton-mass.md).)

## Deferred

Troy ounce; atomic mass unit; implicit mixed-unit arithmetic.
