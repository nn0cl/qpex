# ADR 0130: User-fn Call arguments bind State-forming expressions

## Status

**Accepted** (2026-07-31) — unlocks LISS-0162 under WP-0039.

## Context

Library `fn` Calls already typecheck with `KetLit` / other State-forming
argument expressions, but the Joint evaluator only pushforwarded `Var` args
and attempted classical `_eval_value` on everything else — failing on `KetLit`
(`cannot evaluate KetLit as value`). That is incomplete ship of accepted Call
semantics, not a new language surface.

## Decisions

1. When binding user-fn parameters, non-`Var` / non-`Operator` arguments use
   the same `_bind` path as ordinary State binds (KetLit, Dirac, closed
   classicals, nested Calls that `_bind` already supports).
2. `Var` arguments keep name pushforward (existing behaviour).
3. No change to measure-free `fn` effects, arity, or Partial hole rules.

## Consequences

- `id(|1>)` and Partial slots holding KetLit become runnable.
- Does not invent method Partials, Operator→fn coercion, or fusion.

## Deferred

Richer classical Call value contexts; method Partial values.
