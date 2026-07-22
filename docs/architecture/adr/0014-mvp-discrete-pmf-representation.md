# ADR 0014: MVP value representation is Discrete PMF

## Status

Accepted

Adjudicator technology-selection approval: 2026-07-22 (chat decision).
Follow-up issue: `docs/issues/LISS-0001-language-axioms-mvp-spec.md`.
Accepted MVP specification: `docs/specs/qpex-mvp-discrete-pmf-arith-observe.md`.

## Context

QPex may eventually support continuous densities, Monte Carlo sample bags,
and quantum amplitudes. Starting with all representations at once obscures
exact discrete convolution semantics and slows AT-TDD.

The Adjudicator chose Discrete PMF first for MVP scope A (arithmetic +
`observe`).

## Dependency Adoption Evidence

Not applicable (no crate selected by this ADR). Future numeric crates remain
a non-decision.

## Decision

1. MVP runtime values are finite-support discrete probability mass functions
   over `i64` atoms.
2. A numeric literal `n` denotes the Dirac PMF `{(n, 1.0)}`.
3. Independent combination of distinct bindings uses convolution (for `+`,
   `-`) or the analogous product pushforward (for `*`) over the Cartesian
   product of supports, with masses multiplied and like atoms merged.
4. Reuse of the **same** bound name in one expression (e.g. `x + x`) is the
   pushforward of a **single** random variable (correlated), not an
   independent self-convolution.
5. Continuous, sampled, or quantum representations are out of MVP and require
   a future ADR before implementation.
6. Exact rational vs `f64` masses remains a non-decision; MVP specs may use
   `f64` with an explicit normalization / tolerance rule until superseded.

## Consequences

Positive:

- Exact, testable convolution tables for small supports.
- Clear Red tests for Dirac literals and binary ops.

Negative:

- Support size grows with convolution; large programs need later
  approximation strategy.
- `f64` mass error must be handled carefully in tests.

## Enforcement

Code review should reject:

- Introducing `Sampled` / continuous variants in MVP production code without
  a superseding ADR.
- Treating two mentions of the same binding as independent samples.
- Collapsing PMFs inside arithmetic.
