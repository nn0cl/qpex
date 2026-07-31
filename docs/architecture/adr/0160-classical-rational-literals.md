# ADR 0160: Classical-only rational literals (amends ADR 0125)

## Status

**Accepted** (2026-07-31) — unlocks LISS-0193 under WP-0066.
Amends [ADR 0125](0125-exact-rational-design-boundary.md) for the **classical**
path only. Companions: ADR 0076 Decision 1; ADR 0097.

## Decisions

1. Type-First / classical scalar evaluation of `p/q` over integer (or
   `Fraction`) operands uses `fractions.Fraction`.
2. When a value enters a Joint / `State` coordinate, coerce with `float()` —
   Joint amplitudes and PMF masses remain `f64` (ADR 0076 Decision 1).
3. Float operands keep IEEE division. $1/\sqrt{2}$-class amplitudes stay out
   (ADR 0097).
4. ADR 0125 remains the boundary for **Joint rational mode**; this ADR does
   not unseal rational Joint masses.

## Non-goals

Joint/PMF `Fraction` masses; exact amplitude algebra; generic coefficient type
parameters.

## Consequences

- Classical `Float x = 1/3` may retain `Fraction(1, 3)` in `Evaluator.scalars`.
- Agents must not invent a Joint rational runtime without a new ADR.
