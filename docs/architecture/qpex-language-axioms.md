# QPex Language Axioms

These axioms are **immutable product law** for QPex (Quantum-Probabilistic
Executable). Agents and humans must not reintroduce deterministic scalar
programming as the default mental model.

Normative decisions: ADR 0013 (axioms), ADR 0014 (MVP Discrete PMF).

## Axiom 1 — Every value is a probability distribution

There is no classical “certain scalar” as a first-class runtime value.
Literals such as `10` denote a distribution (in MVP: a Dirac Discrete PMF
concentrated on `10`), not a bare integer.

## Axiom 2 — Every operation is a probabilistic operation

`A + B`, `A - B`, and `A * B` are operations on distributions (convolution or
pushforward), never plain numeric ALU ops on collapsed scalars.

## Axiom 3 — Branching is probabilistic superposition

`if` evaluates a condition as a probability in `[0, 1]` and continues both
branches with weighted merge. **MVP scope A does not implement `if`**, but
implementations must not invent classical branching later without an accepted
spec that preserves this axiom.

## Axiom 4 — Loops are probabilistic enumeration

Loop bounds and continuation are themselves distributions. **MVP scope A does
not implement loops**, under the same deferral rule as Axiom 3.

## Axiom 5 — Collapse only at observation

Distributions remain uncollapsed through pure computation. Sampling /
collapse to a single outcome occurs only at an observation boundary
(`observe` in MVP). Side-effecting report of an observed outcome uses
`ObserveSinkPort`; it must not silently collapse earlier expressions.

## MVP enforcement scope (Adjudicator-approved)

| Topic | Status |
|-------|--------|
| Discrete PMF values | In scope (ADR 0014) |
| Arithmetic `+`, `-`, `*` | In scope |
| `observe` collapse | In scope |
| `if` / `while` / `for` | Out of scope for MVP A |
| Continuous / sample bags | Non-decision |
| QPU backend | Non-decision |

## Forbidden reasoning patterns

- Treating `let x = 10;` as binding a classical `i64`.
- Implementing `+` as integer addition of collapsed samples unless the
  specification explicitly describes an observe-then-operate path (MVP does
  not).
- Collapsing inside arithmetic “for convenience”.
- Classical short-circuit `if` that discards the other branch’s mass.
