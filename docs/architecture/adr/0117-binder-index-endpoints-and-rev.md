# ADR 0117: Binder Index endpoints, dependent ranges, and `rev`

## Status

**Accepted** (2026-07-31) — unlocks LISS-0146 / LISS-0147 under WP-0034.

Companions: [ADR 0096](0096-indexed-operator-and-binder-surface.md) Deferred;
[ADR 0088](0088-finite-binder-lowering.md); [LISS-0146](../../issues/LISS-0146-dependent-index-endpoints.md);
[LISS-0147](../../issues/LISS-0147-rev-binder-domain.md).

## Context

ADR 0096 deferred dependent ranges (`Index<i+1..N-1>`) and `rev()` together with
the integer/overflow/evaluation-time questions for endpoints. Literal-only
`Index<0..3>` left north-star examples that write `N-1` unexecutable.

## Decisions

### D1 — Evaluation time

Endpoint expressions are evaluated at **elaboration / binder lowering** time as
static integers. `Param`, Host, measure, and runtime values are rejected
(`BINDER_DOMAIN_ERROR`).

### D2 — Endpoint grammar

An endpoint is a static additive expression:

- decimal integer literal;
- an enclosing binder variable already in scope;
- a `QubitRegister` / `QutritRegister` / `QuditRegister` binding name,
  denoting that register's static shape length;
- `+` / `-` combining the above (left-associative).

Unary minus on a primary is allowed. Multiplication and calls are out of
scope for this ADR.

### D3 — Arithmetic and emptiness

Arithmetic is unbounded mathematical integer (no wrap, no saturate).

- A fully evaluated endpoint that is **negative** → hard `BINDER_DOMAIN_ERROR`.
- After both endpoints are non-negative, `end < start` → empty domain per
  ADR 0096 D9 (`EMPTY_BINDER_DOMAIN_WARNING` + fold identity). Empty domains
  are **not** reinterpreted as descending ranges.

### D4 — Dependent starts

`Index<i+1..…>` may reference outer binder variables. A binder variable is
not visible in its **own** domain expression (same visibility as ADR 0098 D6).

### D5 — `rev(D)`

`rev(D)` is an additive domain form. For an ascending inclusive domain
`a..b` with `a ≤ b`, enumeration is `b, b-1, …, a`. If `a > b`, the domain
remains empty (D3); `rev` does not flip empty into descending. Expansion /
`product` order follows the **enumeration order** (overrides ascending-only
reading of D10 for `rev` domains).

Surface: `sum (i in rev(Index<0..3>)) { … }`.

### D6 — Equivalence

`sum (i in Index<0..N-1>, j in Index<i+1..N-1>) { body }` enumerates the same
pairs as `where j > i` on the full square, for the same static `N`.

## Consequences

- Parser grows static endpoint expressions and `rev(…)`.
- Lowering passes outer bindings into nested bound evaluation.
- Host tensors, partial Float slices, and Basis expansion remain separate.

## Deferred

- Endpoint `*` / function calls / `Param` sizes;
- `Basis<N>` domain expansion;
- Interpreting `Index<a..b>` with `a > b` as descending without `rev`.
