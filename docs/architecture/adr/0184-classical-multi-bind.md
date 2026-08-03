# ADR 0184: Classical multi-name bind (`J, h = 1.0, 0.5`)

## Status

**Accepted** (2026-08-03) — Adjudicator「続行」on language re-review P1-1
after LISS-0303/0304. Kernel ship via LISS-0305.

Companions: [minimal dialect](../physicist-minimal-dialect.md),
[re-review](../2026-08-03-language-design-rereview.md) P1-1, ADR 0180 inference,
ADR 0095 ideal form first.

## Context

The ideal experiment face writes:

```text
J, h = 1.0, 0.5
H = -J * (Z[0] * Z[1]) - h * (X[0] + X[1])
```

ADR 0180 already allows `J = 1.0` and `h = 0.5` as separate lines. Parenthesized
tuple binds `(s0, s1) = …` already exist for evolve results. Bare multi-name
classical bind was still a parse gap.

## Decision

1. **Surface:** `name1, name2[, …] = expr1, expr2[, …]` with matching arity,
   as an inferred local bind (no type head required).
2. **Desugar:** LHS names + RHS `TupleExpr` of the same length.
3. **Semantics (MVP):** when every RHS item is a **closed classical** scalar
   (literals / pure classical trees), bind each name as a classical scalar
   (same path as single inferred classical bind). Values feed Operator coeffs
   and classical arithmetic.
4. **Arity mismatch:** hard parse/runtime error.
5. **Non-goals (this ADR):**
   - Unifying with full Hindley–Milner
   - Replacing `state (a, b) = evolve …` product binds
   - Classical control sugar

6. **Follow-on (LISS-0309):** linear multi-ket multi-bind
   `s0, s1 = |+>, |+>` is **shipped** — HIR introduces linear roots for
   state-forming tuple items; evaluator binds each item via `_bind`.

## Consequences

Positive: chalk multi-bind matches modern notebooks and the Accepted dialect
sketch. Negative: another bind form — documented in
[bind-decision-tree](../bind-decision-tree.md).

## Acceptance checklist

- [x] Adjudicator Accept (2026-08-03 continue batch)
- [x] Parser + classical evaluator path
- [x] Red tests
- [x] B08 teaching face optional use
