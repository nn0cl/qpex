# ADR 0082: Explicit interface implementations and system declaration boundary

## Status

Accepted (2026-07-24). The Adjudicator approved inline generic bounds,
post-merge coherence checking, marker `System`, and prohibition of `pub` inside
`impl` blocks.

Companion: [LISS-0014](../../issues/LISS-0014-trait-impl-system.md).

## Context

ADR 0019 defines pure trait-like abstractions and immutable system methods.
ADR 0024 standardizes the surface vocabulary as `interface`, `class`, and
`fn`, but leaves explicit implementation syntax and the status of `system` as
an expression unresolved. LISS-0015 now provides the effect boundary required
to keep interface implementations pure by default.

## Proposed decision

1. The first implementation form is explicit `impl Interface for Type`.
   Existing class methods remain inherent methods; a separate inherent `impl
   Type` form is deferred.
2. Coherence is checked after the module graph is merged and before type
   checking/lowering. A linked program may contain at most one implementation
   for each `(Interface, Type)` pair. Duplicate or overlapping implementations
   are hard diagnostics.
3. Bounds are interface-only and explicit. Specialization, negative bounds,
   inheritance, and provider-specific dispatch are out of scope.
4. `system` is a declaration-level scientific contract, not a general
   constructible expression. Runtime values are `class` instances constructed
   as `SystemName(...)`; they implement the `System` interface and expose pure,
   immutable transformers returning new values.
5. The existing `system()` spelling remains valid only where the accepted
   static-Hilbert allocation contract uses it. It does not define the
   abstraction-layer system value model.

## Candidate surface

```staqex
interface Evolvable<T> {
    fn advance(x: State<T>) -> State<T>
}

class Oscillator : System {
    val frequency: State<Float>
}

impl Evolvable<Float> for Oscillator {
    fn advance(x: State<Float>) -> State<Float> {
        return x
    }
}

Oscillator system = Oscillator(frequency)
```

The exact generic-bound spelling and constructor/member rules remain subject
to review; this example is not implementation authorization.

## Resolved decisions

- Generic bounds use inline `<T: Interface>` syntax. `where` clauses, negative
  bounds, and multi-bound forms are deferred.
- Coherence is checked only after the module graph is merged; duplicate or
  overlapping `(Interface, Type)` pairs are hard errors.
- `System` is a marker interface. Behavior belongs to capability interfaces
  such as `Evolvable<T>`.
- `pub` is forbidden inside `impl Interface for Type`; visibility follows the
  interface contract.

## Consequences

Positive:

- Polymorphism is explicit and cannot be confused with mutable inheritance.
- The declaration/value boundary remains visible to physicists and engineers.
- Coherence is deterministic before executable lowering.

Deferred:

- generic trait dispatch and method lookup implementation;
- inherent impl blocks and specialization;
- dynamic dispatch or runtime trait objects.
