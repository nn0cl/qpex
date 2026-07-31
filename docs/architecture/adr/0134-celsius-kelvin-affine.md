# ADR 0134: Affine °C ↔ K conversion

## Status

**Accepted** (2026-07-31) — unlocks LISS-0166 under WP-0041.
Companions: [ADR 0121](0121-si-base-dims-current-temperature.md),
[ADR 0124](0124-si-scale-conversion-explicit.md).

## Decisions

1. ASCII unit suffix `.C` denotes **Celsius** magnitude on Dim Temperature
   (same Dim as `.K`).
2. Explicit conversion is affine, not a pure scale:
   \(T_\mathrm{K} = t_\mathrm{C} + 273.15\),
   \(t_\mathrm{C} = T_\mathrm{K} - 273.15\).
3. Bare `.C` / `.K` stay raw magnitudes (ADR 0124 honesty).
4. No Fahrenheit; no implicit mixed arithmetic.

## Consequences

- `UNIT_TABLE["C"]`; `UNIT_AFFINE_TO_CANONICAL` for the Kelvin family.
- Typecheck/evaluator accept affine `to` when scale table does not apply.

## Deferred

Rankine; implicit auto-rescale of mixed Temperature arithmetic. (°F: ADR 0135.)
