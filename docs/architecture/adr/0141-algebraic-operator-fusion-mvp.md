# ADR 0141: Algebraic Operator Fusion MVP (affine carriers)

## Status

**Accepted** (2026-07-31) — unlocks LISS-0173 under WP-0047.
Extends [ADR 0137](0137-pipeline-operator-fusion-mvp.md) Operator Fusion.
Companion: [`staqex-compiler-optimizations.md`](../staqex-compiler-optimizations.md) §1.

## Context

ADR 0137 fused unary `fn` pipe chains into one Joint pass but still applied
each return expression separately. ADR 0022 / opts note also describe algebraic
collapse such as `(s+10)*2-5 → 2·s+15`. Adjudicator unseals that thin rewrite.

## Decisions

1. **Scope.** When every fused unary return is an **affine** expression in its
   parameter over `+`, `-`, `*` and numeric literals, compose
   `scale·param + bias` maps left-to-right and apply **one** pushforward.
2. **Composition.** For `f(x)=s₁x+b₁` then `g(y)=s₂y+b₂`:
   `g∘f = (s₂s₁)·x + (s₂b₁+b₂)`.
3. **Fallback.** Non-affine returns (e.g. `when`) keep ADR 0137 multi-pass
   fused evaluation; Call/Partial pipe stages remain unfused.
4. **Denotation.** Algebraic result ≡ sequential `fn` application under the
   same RNG stream.

## Non-goals

Polynomial degree ≥ 2; division; Call/Partial fusion; Operator matrix multiply.

## Consequences

- `Evaluator.last_algebraic_fusion` may record `(scale, bias)` for the last
  algebraic pipe bind.
- Agents must not invent broader rewrite families without a new ADR.
