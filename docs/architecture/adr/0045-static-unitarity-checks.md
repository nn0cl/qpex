# ADR 0045: Static unitarity checks (NON_UNITARY_TRANSFORM_ERROR)

## Status

Accepted (2026-07-23).

Companions: ADR 0039 (nested `when`), ADR 0040 (physical axioms).
Verification: **SV-23**.

## Context

Nested-`when` ban was the v0.1 unitarity gate. With `apply` / `capply` /
Operator $H$ in place, the compiler can reject additional clear non-isometric
remaps on coherent quantum lineages and non-unitary matrices.

## Decision

Hard diagnostic **`NON_UNITARY_TRANSFORM_ERROR`** when:

| Pattern | Rationale |
|---------|-----------|
| `project` on strict quantum lineage (ket / `apply` / `capply` / `hadamard` / `cnot` / `interfer` / `shift`) | Mass filter |
| `map` with constant λ on strict quantum | Support collapse |
| `when` on strict quantum with identical arm literals | Non-injective |
| `apply`/`capply` Operator with $U^\dagger U\not\approx I$ | Non-unitary gate |
| `evolve under H` with non-Hermitian Operator | $e^{-iHt}$ not unitary |

**Not banned (MVP):** `project` / identity `map` after `phase` on a classical
`coin()` site (U(1) gauge pedagogy); `project` on bare coin PMF (Ising).

Full static proof of every pushforward remains Deferred (ADR 0052 extends
clear-case coverage).

## Consequences

Positive: fake “quantum” collapse patterns fail at compile time.
Negative: completeness is intentional MVP — exotic remaps may still slip.

## Verification

SV-23 — reject/accept cases above; `gauge_symmetry.staqex` still green.
