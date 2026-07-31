# ADR 0133: Pipeline fills leftmost `_` hole in Call stages

## Status

**Accepted** (2026-07-31) — unlocks LISS-0165 under WP-0041.
Extends [ADR 0080](0080-pipeline-currying-surface.md) / [ADR 0122](0122-pipeline-unary-bare-stage.md) /
[ADR 0123](0123-function-partial-holes.md).

## Decisions

1. When the pipe RHS is a `Call` **without** `_` holes, keep prepend semantics:
   `lhs |> f(a…)` ≡ `f(lhs, a…)`.
2. When the RHS `Call` contains one or more `_` holes, the pipeline value fills
   the **leftmost** hole (not prepended):
   `lhs |> f(a, _)` ≡ `f(a, lhs)`;
   `lhs |> f(_, b)` ≡ `f(lhs, b)`;
   `lhs |> f(_, _)` ≡ `f(lhs, _)` (Partial with one hole remaining).
3. Bare `Var` / bare Partial stages unchanged (ADR 0122 / 0123).
4. Fusion remains out.

## Deferred

Filling a non-leftmost hole by position syntax; method Partials; fusion.
