# ADR 0135: Affine °F ↔ K (Fahrenheit family)

## Status

**Accepted** (2026-07-31) — unlocks LISS-0167 under WP-0042.
Extends [ADR 0134](0134-celsius-kelvin-affine.md).

## Decisions

1. ASCII suffix `.F` denotes **Fahrenheit** magnitude on Dim Temperature.
2. Affine relation to Kelvin (same family as °C):
   \(T_\mathrm{K} = (t_\mathrm{F} + 459.67)\times\frac{5}{9}\)
   equivalently \(T_\mathrm{K} = t_\mathrm{F}\times\frac{5}{9} + \bigl(273.15 - 32\times\frac{5}{9}\bigr)\).
3. Conversions among `.F` / `.C` / `.K` share the Kelvin affine canonical.
4. Bare `.F` stays raw; no implicit mixed arithmetic.

## Deferred

Imperial mass beyond `g`/`kg`; implicit Temperature arithmetic auto-rescale.
(Rankine: [ADR 0144](0144-rankine-kelvin-affine.md).)
