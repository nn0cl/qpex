# ADR 0129: SI scale catalog wave-2

## Status

**Accepted** (2026-07-31) — unlocks LISS-0161 under WP-0039.
Amends [ADR 0124](0124-si-scale-conversion-explicit.md) MVP pairs only.

## Decisions

1. Bare suffixes remain **raw** magnitude + Dim (ADR 0124 Decision 1).
2. Explicit `expr to unit` gains these additive scale rows (factor → canonical):

   | Source | Canonical | Factor |
   |---|---|---|
   | `ps` | `s` | 10⁻¹² |
   | `us` | `s` | 10⁻⁶ |
   | `km` | `m` | 10³ |
   | `kHz` | `Hz` | 10³ |
   | `MHz` | `Hz` | 10⁶ |

3. ASCII `us` is the Kernel spelling for microsecond (no `µ` requirement).
4. `eV`↔`J`, °C↔K, and implicit mixed-unit arithmetic remain deferred.
5. Unsupported pairs stay hard-fail (no silent identity).

## Consequences

- Extend `UNIT_SCALE_TO_CANONICAL` (and `UNIT_TABLE` where missing: `us`, `km`,
  `kHz`, `MHz`).
- Tests cover convert + bare-raw honesty.

## Deferred

Energy/`eV` (see ADR 0132), temperature offsets, imperial units, auto-rescale
arithmetic.
