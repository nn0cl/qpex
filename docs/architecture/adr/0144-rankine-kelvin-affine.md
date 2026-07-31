# ADR 0144: Affine °R ↔ K (Rankine family)

## Status

**Accepted** (2026-07-31) — unlocks LISS-0176 under WP-0050.
Extends [ADR 0134](0134-celsius-kelvin-affine.md) /
[ADR 0135](0135-fahrenheit-kelvin-affine.md).

## Decisions

1. ASCII suffix `.R` denotes **Rankine** magnitude on Dim Temperature.
2. Affine relation to Kelvin (absolute scale with Fahrenheit-sized degrees):
   \(T_\mathrm{K} = t_\mathrm{R}\times\frac{5}{9}\)
   (offset \(0\); equivalently \(t_\mathrm{R} = T_\mathrm{K}\times\frac{9}{5}\)).
3. Conversions among `.R` / `.F` / `.C` / `.K` share the Kelvin affine
   canonical (e.g. \(491.67\,\mathrm{°R} = 32\,\mathrm{°F} = 0\,\mathrm{°C}\)).
4. Bare `.R` stays raw; no implicit mixed Temperature arithmetic.

## Deferred

Imperial mass beyond `g`/`kg`; implicit Temperature auto-rescale.
