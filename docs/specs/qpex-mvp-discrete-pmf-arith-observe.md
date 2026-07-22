# Feature: QPex MVP — Discrete PMF arithmetic and observe

Canonical spec for MVP scope A. Implements ADR 0013 / 0014 / 0015.
Language axioms: `docs/architecture/qpex-language-axioms.md`.

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

When `observe` is applied to a Discrete PMF, the system shall sample exactly
one atom according to the PMF masses via `RngPort`, yield a Dirac PMF on that
atom as the expression result, and may report the observed atom through
`ObserveSinkPort`.

While evaluating pure arithmetic (no `observe`), the system shall not sample
or otherwise collapse any intermediate distribution.

## Gherkin

```gherkin
Feature: Discrete PMF arithmetic and observe

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

  Scenario: observe collapses by sampling
    Given binding x with PMF {(0, 0.25), (1, 0.75)}
    And a deterministic RngPort that draws according to the PMF CDF
    When "observe x" is evaluated
    Then the result PMF is Dirac on the sampled atom
    And exactly one sample request was made to RngPort

  Scenario: pure arithmetic does not call RngPort
    Given binding x with PMF {(0, 0.5), (1, 0.5)}
    When the expression "x + 1" is evaluated
    Then RngPort was not called
    And the result remains a non-collapsed PMF {(1, 0.5), (2, 0.5)}
```

## Surface grammar (MVP A)

```text
program  ::= stmt*
stmt     ::= "let" ident "=" expr ";" | "observe" expr ";"
expr     ::= literal | ident | expr binop expr | "(" expr ")"
binop    ::= "+" | "-" | "*"
literal  ::= integer   # denotes Dirac Discrete PMF
```

Operator precedence (conventional): `*` over `+`/`-`; left-associative.
Parentheses allowed.

## Representation rules

- Support atoms: `i64`.
- Masses: non-negative; sum to `1.0` within tolerance `1e-9` after each
  normalizing operation (tolerance is MVP provisional until an exact-mass ADR).
- Empty support is a domain error.
- Negative or NaN masses are a domain error.

## External Dependencies

- `RngPort` — sampling for `observe` only.
- `ObserveSinkPort` — optional reporting of observed atoms.
- `SourcePort` — loading program text (when running full programs).

## Out of Scope

- `if` / `else`, `while`, `for`, and any classical or probabilistic control
  flow beyond sequencing of `let` / `observe`.
- `print` as a distinct keyword (use `observe` + sink).
- Division, modulo, comparisons, booleans.
- Continuous PDF, Monte Carlo bags, quantum amplitudes.
- Parallelism, persistence, network I/O.

## Ambiguities (resolved for MVP)

- Same-name reuse in one expression → correlated (single RV). Adjudicator
  approved via ADR 0014.
- Distinct names → independent. Adjudicator approved via ADR 0014.

## Ambiguities (still open)

- Exact rational masses vs `f64`.
- Whether `observe` statements bind a new name or only sink the sample
  (Phase 1 design intake may pick a binding form; default proposal:
  `observe` is a statement that samples and sinks, and optionally
  `let x = observe e;` if the grammar is extended — **not** in the grammar
  above until Adjudicator confirms).
