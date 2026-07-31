# ADR 0158: Interprocedural Trace-Out GC (thin)

## Status

**Accepted** (2026-07-31) — unlocks LISS-0191 under WP-0064.
Extends [ADR 0138](0138-trace-out-gc-fn-scope.md) /
[ADR 0153](0153-bare-block-trace-out.md).

## Context

ADR 0138 drops fn-local axes after a library Call but keeps all caller
coordinates. After a Call in `main`, some caller axes are dead relative to the
remaining free-var live-out. Adjudicator unseals that thin post-Call GC.

## Decisions

1. **Scope.** In eligible `main` bodies, after each library `fn` Call
   `StateBind`, drop Joint coordinates that are absent from the free-var
   live-out of subsequent statements, while always retaining the Call result
   bind names.
2. **Eligibility.** Mains with `inspect` (any bind/measure expr) or `snapshot`
   are out of scope (same family as [ADR 0140](0140-deferred-pushforward-mvp.md)).
3. **Liveness.** Live-out is the union of `_expr_free_vars` over subsequent
   `StateBind` / `Measure` / `ExprStmt` expressions — not whole-program SSA.
4. **Surfaces.** Applies on the eager main loop and on the ADR 0140 deferred
   StateBind batch path. Pipe-only binds without a `Call` AST node are out.
5. **Denotation.** Kept coordinates and terminal `measure` are unchanged;
   only dead axes disappear from the in-memory joint.

## Non-goals

Full static interprocedural analysis; mid-fn GC beyond ADR 0138; density-matrix
CTPT GC; system-field liveness.

## Consequences

- Caller axes such as `x` in `state r = f(x); measure r` are traced out.
- ADR 0138 “caller coordinates remain” is narrowed for eligible mains.
- Agents must not invent broader GC without a new ADR.
