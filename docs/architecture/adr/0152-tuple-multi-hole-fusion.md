# ADR 0152: Tuple simultaneous multi-hole pipe / Fusion fill

## Status

**Accepted** (2026-07-31) — unlocks LISS-0184 under WP-0058.
Extends [ADR 0143](0143-call-partial-pipe-fusion-mvp.md) /
[ADR 0149](0149-multi-hole-partial-pipe.md).

## Decisions

1. When the pipe LHS is a `TupleExpr` of arity \(N\) and the RHS is a `Call`
   with exactly \(N\) `_` holes, fill **all** holes left-to-right from the
   tuple items (simultaneous multi-hole fill).
2. The same applies when the RHS is a bound Partial with exactly \(N\)
   remaining holes: `(a, b) |> p`.
3. Fusion peels a leading `tuple |> multi-hole Call` into a fully applied
   Call base so subsequent pure stages may still fuse (ADR 0137/0143).
4. Mismatched tuple vs hole arity → `FUNCTION_ARITY_ERROR`.
5. Single-value leftmost fill (ADR 0133 / 0149) is unchanged when the LHS is
   not a matching-arity tuple.

## Non-goals

Product-typed wires without `TupleExpr`; filling holes from more than one
non-tuple pipe value; polynomial≥2 Fusion.

## Consequences

- `(1, 2) |> add(_, _)` ≡ `add(1, 2)`.
- `(10, 3) |> add(_, _) |> dbl |> inc` may fuse after peeling the tuple stage.
