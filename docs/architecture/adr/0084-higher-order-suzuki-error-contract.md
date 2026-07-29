# ADR 0084: Higher-order Suzuki and explicit QASM error contracts

## Status

Accepted (2026-07-24). The Adjudicator approved S2-only MVP, explicit
`using Suzuki(...)` syntax, exclusive `steps`/`tolerance` policies, and
explicit `Bound`/`EmpiricalEstimate` modes.

Companion: [LISS-0017](../../issues/LISS-0017-higher-order-suzuki.md).

## Context

ADR 0063 defines first-order Lie-Trotter lowering with a fixed step policy.
Higher-order formulas change gate count, approximation behavior, and the
meaning of any user-visible tolerance. The compiler must not silently select a
formula or present an empirical estimate as a mathematical bound.

## Proposed decision

1. Preserve first-order Lie-Trotter as the compatibility default.
2. Make second-order symmetric Suzuki `S2` the first higher-order candidate;
   higher orders remain separate issues.
3. Require an explicit lowering policy containing order, step count or an
   accepted step policy, and an error-contract mode. A tolerance alone cannot
   silently select order or cost.
4. Distinguish `A Priori Bound` from `Empirical Estimate` in diagnostics and
   lowering provenance. If a method cannot provide a bound, it must say so.
5. Preserve order, steps, tolerance, estimate/bound mode, and provenance in the
   provider-neutral QPU IR metadata.

## Resolved decisions

- The MVP supports only order `2`; orders `1`, `3`, and `4` are hard rejected in
  this slice and S4 remains deferred.
- `EmpiricalEstimate` is accepted as an explicit non-guaranteeing mode beside
  `Bound`.
- Tolerance is a static planning target, not a runtime guarantee.
- `steps` and `tolerance` are mutually exclusive. `steps` is direct; tolerance
  causes static step derivation and requires an explicit error mode.
- Existing target-profile/static-Hilbert resource limits govern resource errors;
  no new Suzuki-specific limit is introduced.

## Accepted numerical contract

For `H = sum_j c_j P_j`, let `alpha = sum_j abs(c_j)` and `dt = t / r`.
The accepted static step derivations are:

```text
Bound:             r = ceil(sqrt(alpha^3 * abs(t)^3 / (12 * epsilon)))
EmpiricalEstimate: r = ceil(sqrt(alpha^3 * abs(t)^3 / (120 * epsilon)))
```

`epsilon` must be positive. The result is a fixed integer selected at compile
time; adaptive runtime selection is not part of this slice.

The S2 QASM sequence is, for each step, the forward half sequence over all
terms except the last term, the last term at full `dt`, and the reverse half
sequence. Provider-neutral provenance records the algorithm, order, resolved
steps, error mode, and tolerance target. For direct `steps`, the last two
fields are `null`.

## Surface syntax

```staqex
evolve psi under H for 1.0.s
    using Suzuki(order = 2, steps = 8)

evolve psi under H for 1.0.s
    using Suzuki(order = 2, tolerance = 1e-4, error = EmpiricalEstimate)
```

The `steps` and `tolerance` forms are exclusive. `error` is required with
`tolerance` and forbidden with direct `steps`.

## Consequences

Positive:

- Approximation claims remain honest and inspectable.
- Existing first-order programs remain stable.
- QASM lowering remains vendor-neutral and deterministic.

Deferred:

- S4 and higher-order coefficient tables;
- commutator-norm-derived bounds beyond the accepted alpha contract;
- adaptive step selection and backend-specific resource planning.
