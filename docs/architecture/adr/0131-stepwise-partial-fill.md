# ADR 0131: Stepwise Partial fill (left-to-right)

## Status

**Accepted** (2026-07-31) — unlocks LISS-0163 under WP-0040.
Extends [ADR 0123](0123-function-partial-holes.md).

## Decisions

1. Calling a bound Partial with **fewer** arguments than remaining holes
   (and at least one) fills holes **left-to-right** and yields a new
   immutable Partial with the reduced hole count.
2. Calling with **exactly** the remaining hole count completes to the
   underlying `fn` result (ADR 0123 Decision 4 unchanged).
3. Calling with **more** args than remaining holes → `FUNCTION_ARITY_ERROR`.
4. Nested `_` holes inside a Call on a Partial remain out (no
   `p(_, x)` in this ADR).
5. Bare pipe stages still require exactly one remaining hole.
6. Fusion remains out.

## Example

```text
state p2 = f(a, _, _)
state p1 = p2(b)      // Partial with one hole
state r  = c |> p1    // completes
```

## Deferred

Multi-hole bare pipe stages; method Partials; `p(_, x)` hole re-introduction.
