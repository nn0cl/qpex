# ADR 0153: Bare-block Trace-Out GC

## Status

**Accepted** (2026-07-31) — unlocks LISS-0185 under WP-0059.
Extends [ADR 0138](0138-trace-out-gc-fn-scope.md) /
[ADR 0142](0142-evolve-trace-out-gc.md).

## Decisions

1. Surface `BlockExpr`: `{ let name = expr; …; result }` as an expression.
2. After evaluating a `BlockExpr` bind, drop Joint coordinates that were not
   live before the block and are not the result bind name — same
   `_trace_out_dead_fn_locals` rule as ADR 0138/0142.
3. Grammar of lets/result matches evolve body lets (no nested `fn` / `measure`
   in this MVP).
4. Interprocedural Trace-Out is unsealed by
   [ADR 0158](0158-interprocedural-trace-out.md).

## Non-goals

Statement-only blocks; mid-block GC; density-matrix CPTP GC.

## Consequences

- `state w = { let t = …; t }` ships; `t` is absent from the joint after exit.
- Agents must not invent broader block statement forms without a new ADR.
