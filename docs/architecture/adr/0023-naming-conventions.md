# ADR 0023: QPex naming conventions (style)

## Status

Accepted as **style baseline** (2026-07-22).

Canonical guide: `docs/style-guide/naming-conventions.md`.

Does not change Language Law or Kernel PoC denotation. Linter enforcement
remains **Hold** until a tooling unseal.

## Context

Physicists need single-letter / Greek-transcribed state names that mirror
$\lvert\psi\rangle$; engineers need instant visual separation of `State`,
constants, types, and functions. General-purpose language habits (PascalCase
variables, camelCase methods) raise cognitive load and break paper ↔ code
sync.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. **`State` / superposition bindings**: lowercase `snake_case` or single
   lowercase letter (`psi`, `x`, `phi_0`).
2. **Classical scalar constants**: `ALL_CAPS` (`DT`, `MAX_STEPS`).
3. **`system` / types / `trait`**: `PascalCase` (`HarmonicOscillator`,
   `System`).
4. **Functions / methods**: `snake_case` (`step`, `run_simulation`).
5. **Leading `_name`**: style marker for ancilla / local axes expected to be
   traced out; `_` alone remains wildcard. Naming does not replace Trace-Out
   GC liveness (ADR 0022).
6. **Greek / subscripts / primes**: English transcription + `_` subscripts;
   `x_prime` or `x1` for $x'$. ASCII identifiers in MVP.
7. Prefer `state` keyword (and optional `s_` prefix) over silent inference for
   role clarity.
8. Future styler / linter IDs are listed in the style guide; parser accepts
   legal identifiers regardless.

## Consequences

Positive:

- Shared visual grammar for physicists and engineers.
- Clear hook for future `qpex fmt` / lint.

Negative / cost:

- Soft rules until tooling exists; docs/examples must lead by example.

## Enforcement

In normative examples and reviews, reject systematic violations of case roles
(e.g. `state MaxSteps`, `fn RunSim`) and leading `_` on escaping state
fields. Do not treat this ADR as unsealing a linter implementation.
