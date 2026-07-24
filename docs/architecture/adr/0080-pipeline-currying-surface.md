# ADR 0080: State-preserving pipeline and function-only partial application

## Status

Accepted (2026-07-24). The pipeline MVP boundary has completed its AT-TDD
implementation and refactor slice. General partial-application representation
and richer callable forms remain deferred.

Companion: [LISS-0013](../../issues/LISS-0013-pipeline-currying.md).

## Decision

1. `lhs |> f` expands to `f(lhs)` and is left-associative. Thus
   `x |> f |> g` means `g(f(x))`.
2. The MVP pipeline accepts named `fn` values and compatible calls. It does not
   introduce a runtime loop, classical escape, or provider operation.
3. Currying/partial application is function-only in the MVP and produces an
   immutable first-class function value with remaining parameter types.
   Operators are not implicitly converted to functions.
4. State transformers preserve `State<T>`/Joint semantics. Pipeline stages may
   not measure, consume RNG, mutate outer bindings, or access Host/Job/provider
   APIs.
5. Arity, type, effect, and missing-argument violations are hard diagnostics
   before lowering. Operator Fusion is an optimization concern and does not
   alter pipeline denotation.

## Consequences

Positive:

- Pipeline order is visually and semantically deterministic.
- Partial application does not create a second Operator semantics.
- Pure composition remains compatible with `Never Leave the State`.

Deferred:

- exact grammar and `let`/`curry` spelling;
- closure capture and callable type representation;
- method values and generic function compatibility;
- fusion/lowering implementation.

## Enforcement

- Reject pipeline stages with measurement, RNG, mutation, Host, Job, or
  provider effects.
- Reject implicit Operator-to-function conversion.
- Preserve source order and function application order in any later IR.
