# ADR 0084: Higher-order Suzuki and explicit QASM error contracts

## Status

Accepted (2026-07-24). Amended (2026-07-31) to accept order `4` (S4) beside
order `2` (S2); explicit `using Suzuki(...)` syntax, exclusive
`steps`/`tolerance` policies, and explicit `Bound`/`EmpiricalEstimate` modes
remain.

Companions: [LISS-0017](../../issues/LISS-0017-higher-order-suzuki.md) (S2);
[LISS-0142](../../issues/LISS-0142-suzuki-s4.md) (S4).

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

- Accepted orders are `2` and `4`. Orders `1`, `3`, and any value other than
  `{2, 4}` are hard rejected (`SUZUKI_ORDER_ERROR`).
- `EmpiricalEstimate` is accepted as an explicit non-guaranteeing mode beside
  `Bound`.
- Tolerance is a static planning target, not a runtime guarantee.
- `steps` and `tolerance` are mutually exclusive. `steps` is direct; tolerance
  causes static step derivation and requires an explicit error mode.
- Existing target-profile/static-Hilbert resource limits govern resource errors;
  no new Suzuki-specific limit is introduced.

## Accepted numerical contract

For `H = sum_j c_j P_j`, let `alpha = sum_j abs(c_j)` and `dt = t / r`.

### Order 2 (S2)

```text
Bound:             r = ceil(sqrt(alpha^3 * abs(t)^3 / (12 * epsilon)))
EmpiricalEstimate: r = ceil(sqrt(alpha^3 * abs(t)^3 / (120 * epsilon)))
```

### Order 4 (S4)

```text
Bound:             r = ceil((alpha^5 * abs(t)^5 / (360 * epsilon))^(1/4))
EmpiricalEstimate: r = ceil((alpha^5 * abs(t)^5 / (3600 * epsilon))^(1/4))
```

`epsilon` must be positive. The result is a fixed integer selected at compile
time; adaptive runtime selection is not part of this slice.

### Product formulas

Let \(S_2(\lambda)\) be the symmetric second-order product (forward half over
all terms except the last, last term at full \(\lambda\), reverse half).

\[
p = \frac{1}{4 - 4^{1/3}},\qquad
S_4(\lambda) = S_2(p\lambda)^2\, S_2((1-4p)\lambda)\, S_2(p\lambda)^2.
\]

Each outer Trotter step of duration \(dt = t/r\) emits \(S_4(dt)\).
Provider-neutral provenance records the algorithm, order, resolved steps,
error mode, and tolerance target. For direct `steps`, the last two fields are
`null`.

## Surface syntax

```staqex
evolve psi under H for 1.0.s
    using Suzuki(order = 2, steps = 8)

evolve psi under H for 1.0.s
    using Suzuki(order = 4, steps = 4)

evolve psi under H for 1.0.s
    using Suzuki(order = 2, tolerance = 1e-4, error = EmpiricalEstimate)
```

The `steps` and `tolerance` forms are exclusive. `error` is required with
`tolerance` and forbidden with direct `steps`.

## Consequences

Positive:

- Approximation claims remain honest and inspectable.
- Existing first-order and S2 programs remain stable.
- QASM lowering remains vendor-neutral and deterministic.
- S4 is available when users ask for a higher-order formula explicitly.

Deferred:

- Orders above 4 and further coefficient tables;
- commutator-norm-derived bounds beyond the accepted alpha contract;
- adaptive step selection and backend-specific resource planning.
