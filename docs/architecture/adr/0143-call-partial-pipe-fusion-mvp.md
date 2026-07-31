# ADR 0143: Call / Partial pipe Fusion MVP

## Status

**Accepted** (2026-07-31) — unlocks LISS-0175 under WP-0049.
Extends [ADR 0137](0137-pipeline-operator-fusion-mvp.md) Operator Fusion.
Companions: [ADR 0123](0123-function-partial-holes.md),
[ADR 0141](0141-algebraic-operator-fusion-mvp.md).

## Context

ADR 0137 fused only bare unary `fn` pipe stages and excluded Call-with-holes
and Partial stages. Adjudicator unseals a thin extension: one-hole Call /
Partial stages may participate in the same measure-free Fusion pass.

## Decisions

1. **Eligibility.** Left-associative pipe chains of length ≥ 2 where each stage
   is one of:
   - bare `Var` naming a measure-free unary `fn` (ADR 0137);
   - `Call` with **exactly one** `_` hole to a measure-free `fn` of matching
     arity;
   - bare `Var` naming a bound `PartialValue` with **exactly one** remaining
     hole.
2. **Mechanism.** Materialize the pipe base once; for each stage, evaluate the
   `fn` return with closed slots filled and the pipe value in the hole slot —
   still one Joint worlds pass per stage (no intermediate pipeline bind names).
3. **Algebraic affine collapse (ADR 0141)** remains limited to all-unary-bare
   stages; Call/Partial stages use the multi-pass fused eval above.
4. **Denotation.** ≡ sequential desugared Calls under the same RNG stream.
5. **Fallback.** Multi-hole Partial, effectful `fn`, or ineligible stages use
   sequential `_piped_call` / `_bind_call`.

## Non-goals

Multi-hole simultaneous fill in one fused stage; Operator fusion; polynomial≥2.

## Consequences

- `x |> add(10, _) |> dbl` and `x |> p |> dbl` (with `p = add(10, _)`) may fuse.
- Agents must not invent broader Partial rewriting without a new ADR.
