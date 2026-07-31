# ADR 0157: Polynomial Operator Fusion (≥2)

## Status

**Accepted** (2026-07-31) — unlocks LISS-0190 under WP-0063.
Extends [ADR 0141](0141-algebraic-operator-fusion-mvp.md) algebraic collapse.

## Context

ADR 0141 collapsed affine unary pipe returns into one pushforward. Quadratic
and higher polynomial returns (e.g. `s * s + 1`) still used multi-pass fusion.
Adjudicator unseals thin polynomial composition for the same unary bare-pipe
eligibility as ADR 0141.

## Decisions

1. **Scope.** When every fused unary return is a **polynomial** in its parameter
   over `+`, `-`, `*` and numeric literals, compose coefficient vectors
   left-to-right and apply **one** pushforward.
2. **Representation.** Coefficients are low-to-high:
   `[c₀, c₁, …, cₙ]` means `c₀ + c₁·x + … + cₙ·xⁿ`. Degree cap for composed
   results is 8; above that, fall back to ADR 0137 multi-pass fusion.
3. **Affine evidence.** Degree ≤ 1 (or degree-2 with vanishing quadratic term)
   still records `Evaluator.last_algebraic_fusion = (scale, bias)` for ADR 0141
   tests. Higher degree records `Evaluator.last_poly_fusion` as the coeff tuple.
4. **Fallback.** Non-polynomial returns (`when`, Calls, division, etc.) keep
   ADR 0137 multi-pass fused evaluation.
5. **Denotation.** Algebraic result ≡ sequential `fn` application under the
   same RNG stream.

## Non-goals

Division; rational powers; `when`/Call algebraic rewrite; Operator matrix
multiply; symbolic coefficient domains beyond f64.

## Consequences

- ADR 0141 non-goal “polynomial degree ≥ 2” is superseded for this thin MVP.
- Agents must not invent broader rewrite families without a new ADR.
