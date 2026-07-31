# ADR 0147: Imperial mass scale `st` ↔ `kg` / `lb` / `oz`

## Status

**Accepted** (2026-07-31) — unlocks LISS-0179 under WP-0053.
Extends [ADR 0145](0145-imperial-pound-mass.md) /
[ADR 0146](0146-imperial-ounce-mass.md).

## Decisions

1. ASCII suffix `.st` denotes the British **stone** on Dim Mass.
2. Exact relation \(1\,\mathrm{st} = 14\,\mathrm{lb}\), hence
   \(1\,\mathrm{st} = 0.45359237\times 14\,\mathrm{kg}\) and
   \(1\,\mathrm{st} = 224\,\mathrm{oz}\).
3. Conversions among `.st` / `.lb` / `.oz` / `.g` / `.kg` share the kilogram
   scale canonical.
4. Bare `.st` stays raw; no troy or implicit mixed Mass arithmetic.
   (Tonne: [ADR 0148](0148-tonne-mass.md).)

## Deferred

Troy ounce; atomic mass unit; implicit mixed-unit arithmetic.
