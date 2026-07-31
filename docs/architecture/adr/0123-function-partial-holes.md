# ADR 0123: Function-only partial application with `_` holes

## Status

**Accepted** (2026-07-31) — unlocks LISS-0155 under WP-0038.
Extends [ADR 0080](0080-pipeline-currying-surface.md) / [ADR 0122](0122-pipeline-unary-bare-stage.md).

## Decisions

1. Ordinary `Call` and bare `lhs |> f` remain **strict arity**.
2. A call may include one or more `_` hole arguments. Presence of any hole
   yields an immutable **Partial** value (not an immediate invoke).
3. Spelling: `fn_name(bound…, _, …)` only. No new `curry` keyword in this ADR.
4. Completing a Partial: call it with remaining args, or use as a unary pipe
   stage when exactly one hole remains (`psi |> shifted`).
5. Partial is **function-only**; Operator / effectful `fn` rejected.
6. Fusion remains out.

## Consequences

- Parser accepts `_` as a hole expression in call argument lists.
- Typecheck introduces a Partial callable typing for unfinished applications.
- Evaluator stores bound args and applies on completion.

## Deferred

Multi-hole bare pipe stages; method Partials; `p(_, x)` hole re-introduction;
fusion. (Stepwise Call fill: ADR 0131.)
