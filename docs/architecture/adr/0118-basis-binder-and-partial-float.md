# ADR 0118: `Basis<N>` binder expansion and partial Float indexing

## Status

**Accepted** (2026-07-31) — unlocks LISS-0148 / LISS-0149 under WP-0035.

Companions: [ADR 0096](0096-indexed-operator-and-binder-surface.md);
[ADR 0088](0088-finite-binder-lowering.md); [ADR 0117](0117-binder-index-endpoints-and-rev.md);
[LISS-0038](../../issues/LISS-0038-semantic-discrete-carriers.md).

## Context

ADR 0096 deferred `Basis<N>` domain expansion (honesty-only `BINDER_DOMAIN_ERROR`
after LISS-0140) and partial Float tensor indexing. Kernel ND literals
(LISS-0144) already require full-rank chains inside Operator binders. North-star
sources that write `sum (n in Basis<N>)` and row slices `Float[M] row = h[i]`
remain unexecutable without this contract.

## Decisions

### D1 — `Basis<N>` binder domain

`sum` / `product` may use `Basis<N>` when `N` is a static positive integer
literal.

Enumeration is the computational-basis label order `0, 1, …, N-1` (ascending),
matching ADR 0096 D10 unless wrapped in `rev` (ADR 0117 D5).

Using the binder variable as a Pauli / site index (`Z[n]`) is allowed when the
acting register length is at least `N`. This is **label-as-site** on the same
finite Hilbert space, not an implicit `Basis` → `Index` type coercion elsewhere
in the language (LISS-0038 rule 2 remains).

`Basis` and `Index` remain distinct carriers. Other discrete carriers
(`EnergyLevel`, `Bit`, `SpinProjection`, …) stay deferred as binder domains.

### D2 — Emptiness, budget, register fit

- `N == 0` → empty domain (ADR 0096 D9 warning + fold identity).
- Expansion size respects the existing binder resource budget.
- If a static register shape `R` is known and `N > R`, emit
  `BINDER_DOMAIN_ERROR` (same capacity rule as inclusive Index ranges).

### D3 — `rev(Basis<N>)`

`rev(Basis<N>)` is accepted and enumerates `N-1, …, 0` when `N > 0`.

### D4 — Partial Float indexing (classical)

Given `Float[N0][N1]…[Nk-1] a = […]` (Kernel literal), a **prefix** index chain
with `0 < r < k` static literal indices yields a classical tensor value of type
`Float[Nr]…[Nk-1]`.

Surface (type-first bind):

```staqex
Float[2][3] h = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]];
Float[3] row = h[1];   // [4.0, 5.0, 6.0]
```

Rules:

1. Indices in a classical partial bind RHS are **static non-negative integer
   literals** (elaboration-time). Binder variables and `Param` are out of scope.
2. Declared remaining shape must match the sliced axes exactly.
3. The bound name is registered as a Kernel float tensor alias (same budget /
   lookup path as literal `Float[…]` binds).
4. Inside an Operator binder body, a coefficient used as a **scalar** still
   requires a **full-rank** index chain to a float leaf. Partial `h[p] * Z[p]`
   remains `BINDER_LOWERING_UNSUPPORTED` (or type mismatch). Completing the
   chain (`h[p][q]` or `row[q]` after a classical partial bind) is required.

Host / Param tensor inject remains deferred (ADR 0090).

## Consequences

- Typecheck accepts `Basis<N>` binder domains; lowering expands like
  `Index<0..N-1>`.
- Honesty tests that expected `Basis` → `BINDER_DOMAIN_ERROR` move to other
  deferred carriers.
- `Float[…]` type-first RHS may parse OpDSL indexed forms for partial aliases.
- LISS-0144’s full-rank rule for **scalar** binder coefficients is unchanged.

## Deferred

- Host / Param coefficient tensors beyond ADR 0119 in-memory inject
  (file adapters, geometry);
- Classical partial indices that are non-literal (binder vars, arithmetic);
- Prefix length `r == 0` (whole alias) and suffix/slice ranges (`h[i..j]`);
- `EnergyLevel` / `Bit` / `SpinProjection` binder domains;
- controlled / approximate QFT beyond ADR 0120 exact `cqft`/`ciqft`;
- permanent-out topics.
