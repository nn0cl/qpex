# ADR 0081: Explicit effect marking and propagation

## Status

Accepted (2026-07-24). The fixed effect vocabulary, `effects { ... }` surface,
and propagation boundary completed the AT-TDD implementation and refactor
slice. Effect rows and provider-specific effects remain deferred.

Companion: [LISS-0015](../../issues/LISS-0015-effect-marking.md).

## Context

Staqex keeps ordinary Kernel computation inside `State<T>`/Joint and reserves
`measure` for terminal collapse. Existing host boundaries also distinguish
non-collapsing diagnostics (`inspect`, `snapshot`) from measurement and port
operations. Without explicit function effects, a helper or pipeline stage can
hide those boundaries from callers and weaken the static guarantees.

## Proposed decision

1. Ordinary `fn` is pure by default. Effects must be declared at the function
   boundary and are propagated transitively through calls, methods, modules,
   and pipelines.
2. The initial effect vocabulary is fixed and intentionally small:
   `Measure`, `Snapshot`, `Inspect`, and `Host`.
   - `Measure` samples/collapses and is legal only at the terminal boundary.
   - `Snapshot` reports a non-collapsing state representation to a sink.
   - `Inspect` is a non-collapsing identity on the Kernel value with a host
     diagnostic effect.
   - `Host` denotes port-backed input/output or other host coordination.
3. A pure caller cannot call an effectful function. A declared effect cannot be
   erased by a wrapper, method dispatch, or `|>` stage.
4. Effects are compile-time metadata (`EffectSet`/`EffectSummary`); concrete
   sinks, RNG, Jobs, providers, and credentials remain outside the Kernel
   behind ports.
5. `measure` does not become an ordinary function return value. The language
   remains responsible for terminal observation, while the host obtains the
   emitted `JobResult`/sink data after execution completes.

## Syntax candidates for review

The exact spelling is intentionally unresolved. Candidates are:

```staqex
fn inspect_state(x: State<Float>) -> State<Float> effects { Inspect } { ... }
fn inspect_state(x: State<Float>) -> State<Float> !Inspect { ... }
```

The accepted spelling must be unambiguous, composable with existing `fn` and
`->` return syntax, and must not resemble a runtime value.

## Open decisions

- Fixed effect set versus extensible effect rows.
- Whether `Inspect` is visible in the function type or treated as a delivery
  annotation while remaining semantically identity.
- Whether `State<T>`-returning functions may declare `Measure` (recommended:
  no, because sampled data must not re-enter Staqex).
- Whether `Host` is a single broad capability or split into input/output
  capabilities in a later issue.

## Consequences

Positive:

- Helpers and pipeline stages cannot hide measurement or host boundaries.
- Type checking can reject effect misuse before lowering.
- Existing ports and Job boundaries remain intact.

Deferred:

- parser spelling and AST representation;
- effect inference details for generic functions and method dispatch;
- provider-specific effects and dynamic-circuit feedback.
