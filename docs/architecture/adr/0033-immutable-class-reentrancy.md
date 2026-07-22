# ADR 0033: Immutable `class` — structural reentrancy / race freedom

## Status

Accepted (2026-07-23).

Companions: `qpex-abstraction-model.md`, ADR 0019 (capsule laws), ADR 0024
(`class` surface), ADR 0028 (no threads), ADR 0032 (pure DAG eval).

## Context

Classical OOP objects are mutable memory + methods. Reentrancy, locks, and
data races dominate engineering cost. QPex keeps OOP *syntax* (`class`,
method calls) but must not import in-place mutation.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. A QPex `class` is an **immutable capsule** of `State<_>` (and nested
   capsules). Fields are not writable in place.
2. Instance methods are **pure transformers**: they return a **new** value
   (`Self` / other `State` / `class`) built from pushforwards / `when` /
   combinators. `this` / `self` is never mutated.
3. Therefore object-language code is **structurally reentrant**: overlapping
   or recursive calls cannot corrupt a shared mutable interior — there is none.
4. **No mutex / `synchronized` / `ReentrantLock` surface** for domain logic.
   Engine parallelism (ADR 0032) schedules immutable pushforwards only.
5. “Encapsulation” means **scope + immutability of joint coordinates**, not
   hiding a mutable buffer behind getters/setters.
6. Inheritance that implies mutable subclass state remains **rejected**
   (ADR 0019); prefer `interface` + composition.

## Consequences

Positive:

- Reentrancy / deadlock / shared-mutation races of classical OOP do not arise
  in the object language.
- Familiar `class` DX without OOP’s concurrency tax.

Negative:

- Allocation of new capsules is the default (engine may optimize / fuse);
  developers from mutable OOP must unlearn setters.

## Enforcement

Reject normative examples that assign to `this.field`, expose setters that
mutate in place, or teach locks as required for QPex domain classes.
