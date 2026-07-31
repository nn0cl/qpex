# ADR 0122: Pipeline unary bare stage `lhs |> f`

## Status

**Accepted** (2026-07-31) — unlocks LISS-0154 under WP-0037.
Amends deferred grammar of [ADR 0080](0080-pipeline-currying-surface.md)
Decision 1 for bare named `fn` stages.

## Context

ADR 0080 Decision 1 states `lhs |> f` → `f(lhs)`, but the Kernel only accepted
`Call` RHS stages. Permanent-out blocked further `|>` expansion; reopen allows
this thin lock.

## Decisions

1. Pipeline RHS may be a bare `Var` naming a **unary** pure `fn`. Expansion is
   `f(lhs)` (same denotation as Decision 1).
2. Operator values remain rejected (`PIPE_CALLABLE_ERROR`).
3. Effectful `fn` stages remain rejected (`PIPE_EFFECT_ERROR`).
4. Non-unary bare `Var` is a hard `FUNCTION_ARITY_ERROR` / `PIPE_CALLABLE_ERROR`
   (partial-application values remain a follow-up Issue, not this ADR).
5. Fusion and Operator→fn coercion stay out.

## Consequences

- Typecheck and evaluator accept `Pipe` with `Var` RHS via synthetic `Call`.
- Existing `lhs |> f(args…)` Call stages unchanged.

## Deferred

First-class partial-application values; `curry` keyword; method values; fusion.
