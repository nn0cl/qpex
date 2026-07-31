# ADR 0151: Troy ounce mass scale `oz_t` ↔ `kg` / `g`

## Status

**Accepted** (2026-07-31) — unlocks LISS-0183 under WP-0057.
Extends [ADR 0146](0146-imperial-ounce-mass.md) (avoirdupois `.oz` unchanged).

## Decisions

1. ASCII suffix `.oz_t` denotes the **troy ounce** on Dim Mass.
2. Exact relation \(1\,\mathrm{oz\_t} = 31.1034768\,\mathrm{g}\)
   (\(31.1034768\times 10^{-3}\,\mathrm{kg}\)).
3. Conversions among `.oz_t` / `.oz` / `.lb` / `.g` / `.kg` / ton suffixes
   share the kilogram scale canonical.
4. Avoirdupois remains `.oz` only. Bare `.oz_t` stays raw; no implicit mixed
   Mass arithmetic.

## Deferred

Atomic mass unit; bare `.ozt` alias; implicit mixed-unit arithmetic.
