# ADR 0137: Thin pipeline Operator Fusion MVP (Hold partial unseal)

## Status

**Accepted** (2026-07-31) — unlocks LISS-0169 under WP-0043.
Amends [ADR 0022](0022-quantum-native-optimizations.md) Hold for this MVP only.
Companions: [ADR 0080](0080-pipeline-currying-surface.md);
[`staqex-compiler-optimizations.md`](../staqex-compiler-optimizations.md) §1.

## Context

ADR 0022 documented Operator Fusion as a future IR/engine family and held
implementation. Adjudicator unseals a **Kernel-local** thin slice: denotation-
preserving collapse of pure unary `fn` pipe chains.

## Decisions

1. **Hold partial unseal.** Trace-Out GC, Interference prune, and Deferred
   Pushforward remain Hold. Only pipeline Operator Fusion MVP below is
   authorized for Kernel shipping.
2. **Eligibility.** Left-associative `base |> f1 |> … |> fn` where each `fi`
   is a bare `Var` naming a measure-free **unary** `fn`. Call-with-holes,
   Partial stages, Operators, and effectful `fn` are never fused (fallback to
   sequential evaluation).
3. **Denotation.** Fused evaluation ≡ sequential `fn(…f2(f1(base))…)`. Same
   terminal `measure` / marginal under the same RNG stream.
4. **Mechanism.** Flatten the pipe AST; apply each eligible `fn` return
   expression in one Joint worlds pass without materializing intermediate
   pipeline bind names. Bodies with multiple `StateBind` statements or without
   an explicit `return`/`result` fall back to sequential `_bind_call`.
5. **Algebraic rewrite** of affine/polynomial carriers (e.g. collapse
   `(s+10)*2-5`) is **not** required in this MVP.

## Non-goals

DAG IR opcodes; multi-wire correlation fusion beyond unary pushforward;
Operator matrix multiply fusion; Host/QPU passes.

## Consequences

- Evaluator may take a fused path; typecheck denotation unchanged.
- Agents must not treat this ADR as unsealing the full ADR 0022 quartet.
