# ADR 0132: Exact SI `eV` ↔ `J` conversion

## Status

**Accepted** (2026-07-31) — unlocks LISS-0164 under WP-0040.
Companions: [ADR 0124](0124-si-scale-conversion-explicit.md),
[ADR 0129](0129-si-scale-catalog-wave2.md).

## Decisions

1. Explicit `expr to unit` may convert between `eV` and `J` (same Energy Dim).
2. Factor is the **exact SI** elementary charge relation (2019 definition):
   \(1\,\mathrm{eV} = 1.602176634\times 10^{-19}\,\mathrm{J}\).
3. Bare `.eV` / `.J` suffixes remain raw magnitudes (ADR 0124 honesty).
4. °C↔K (affine offset) and implicit mixed-unit arithmetic remain deferred.

## Consequences

- Add `eV` / `J` rows to `UNIT_SCALE_TO_CANONICAL` with canonical head `J`.
- Reverse `J to eV` uses the reciprocal factor.

## Deferred

Temperature °C; imperial units; auto-rescale arithmetic.
