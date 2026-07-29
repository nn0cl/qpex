# Feature: Staqex MVP — Discrete PMF arithmetic and measure

> **Historical / superseded surface note:** Filename and older prose may
> say `observe`. Current collapse keyword is **`measure`**. Normative
> language surface: [`docs/architecture/staqex-language-spec.md`](../architecture/staqex-language-spec.md)
> (ADRs 0021–0026). Kernel laws in this file remain valid under `measure`.


Canonical behavioral slice for MVP scope A. Normative joint / pushforward /
measure laws: `docs/specs/staqex-formal-semantics-sketch.md`.
Surface lexicon: `docs/architecture/staqex-syntax-vocabulary.md` (ADR 0017).
Implements ADR 0013 / 0014 / 0015 / 0016 / 0017.
Language axioms: `docs/architecture/staqex-language-axioms.md`.
Positioning: `docs/architecture/staqex-positioning.md` (Accepted).

**Process:** Feature Path Phase 1 Red is HOLD until Kernel PoC A/B fixtures are
green; then Phase 1 is unsealed (still needs an explicit phase request).

## EARS

When a numeric literal appears in an expression, the system shall treat it as
a Dirac Discrete PMF on that `i64` atom with mass `1.0`.

When two distribution-valued subexpressions are combined with `+`, `-`, or
`*`, the system shall compute the result as a Discrete PMF via pushforward
over the joint support, without collapsing either operand.

When the same bound name appears more than once in one expression
(e.g. `x + x`), the system shall treat those occurrences as the same random
variable (correlated pushforward), not as independent copies.

When distinct bindings are combined (e.g. `x + y`), the system shall treat
them as independent Discrete PMFs and combine masses by multiplication on
the Cartesian product of supports, merging equal atoms by summing masses.

When `measure` is applied to a Discrete PMF, the system shall sample exactly
one atom according to the PMF masses via `RngPort`, yield a Dirac PMF on that
atom as the expression result, and may report the measured atom through
`MeasureSinkPort`.

While evaluating pure arithmetic (no `measure`), the system shall not sample
or otherwise collapse any intermediate distribution.

## Gherkin

```gherkin
Feature: Discrete PMF arithmetic and measure

  Scenario: Numeric literal is a Dirac PMF
    Given an expression "10"
    When the expression is evaluated
    Then the result PMF support is exactly {10}
    And the mass at 10 is 1.0 within tolerance

  Scenario: Independent sum convolves supports
    Given binding x = Dirac(1)
    And binding y = Dirac(2)
    When the expression "x + y" is evaluated
    Then the result PMF support is exactly {3}
    And the mass at 3 is 1.0 within tolerance

  Scenario: Sum of non-Dirac independent PMFs
    Given binding x with PMF {(0, 0.5), (1, 0.5)}
    And binding y with PMF {(0, 0.5), (10, 0.5)}
    When the expression "x + y" is evaluated
    Then the result PMF equals
      {(0, 0.25), (1, 0.25), (10, 0.25), (11, 0.25)} within tolerance

  Scenario: Correlated self-sum uses one random variable
    Given binding x with PMF {(0, 0.5), (1, 0.5)}
    When the expression "x + x" is evaluated
    Then the result PMF equals {(0, 0.5), (2, 0.5)} within tolerance
    And the result PMF does not place mass on 1

  Scenario: Product of independent Diracs
    Given binding x = Dirac(3)
    And binding y = Dirac(4)
    When the expression "x * y" is evaluated
    Then the result PMF support is exactly {12}

  Scenario: Subtraction of independent Diracs
    Given binding x = Dirac(5)
    And binding y = Dirac(2)
    When the expression "x - y" is evaluated
    Then the result PMF support is exactly {3}

  Scenario: measure collapses by sampling
    Given binding x with PMF {(0, 0.25), (1, 0.75)}
    And a deterministic RngPort that draws according to the PMF CDF
    When "measure x" is evaluated
    Then the result PMF is Dirac on the sampled atom
    And exactly one sample request was made to RngPort

  Scenario: pure arithmetic does not call RngPort
    Given binding x with PMF {(0, 0.5), (1, 0.5)}
    When the expression "x + 1" is evaluated
    Then RngPort was not called
    And the result remains a non-collapsed PMF {(1, 0.5), (2, 0.5)}
```

## Surface grammar (Kernel / MVP arith + measure)

Authoritative lexicon: `docs/architecture/staqex-syntax-vocabulary.md` (ADR 0017).

```text
program  ::= stmt*
stmt     ::= "state" (ident | "(" ident ("," ident)* ")") "=" expr
           | "measure" expr
expr     ::= "coin" "(" ")"
           | "dirac" "(" integer ")"
           | integer
           | ident
           | expr binop expr
           | "(" expr ")"
binop    ::= "+" | "-" | "*"
```

`span` / `evolve` are accepted baseline forms but **out of scope** for Kernel
PoC A/B and for the first Phase 1 Red slice unless the Adjudicator widens
scope.

Operator precedence (conventional): `*` over `+`/`-`; left-associative.

## Representation rules

- Support atoms: `i64`.
- Masses: non-negative; sum to `1.0` within tolerance `1e-9` after each
  normalizing operation (tolerance is MVP provisional until an exact-mass ADR).
- Empty support is a domain error.
- Negative or NaN masses are a domain error.

## External Dependencies

- `RngPort` — sampling for `measure` only.
- `MeasureSinkPort` — optional reporting of measured atoms.
- `SourcePort` — loading program text (when running full programs).

## Out of Scope

- Classical `if` / `else` / `while` / `for` / `return`.
- `span` / `evolve` bodies in the first Kernel Phase 1 slice (syntax reserved).
- `print` as a distinct keyword (use `measure` + sink).
- Division, modulo, comparisons, booleans.
- Continuous PDF, Monte Carlo bags, quantum amplitudes (stance a lift later).
- Parallelism, persistence, network I/O.

## Ambiguities (resolved for MVP)

- Same-name reuse in one expression → correlated (single RV). Adjudicator
  approved via ADR 0014.
- Distinct names → dependence only as encoded in the joint (ADR 0014 / sketch).
- Surface collapse keyword → `measure` (ADR 0017).

## Ambiguities (still open)

- Exact rational masses vs `f64`.
- `evolve` repetition grammar (`times` / `until`).
- Exact `span` denotation under amplitude lift vs MVP convex mixture.
- Whether `measure` may bind a new `state` name or only sinks.