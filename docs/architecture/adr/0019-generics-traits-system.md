# ADR 0019: Generics, traits, and `system` — pure abstractions only

## Status

Accepted (2026-07-22). **Surface updated by ADR 0024 and ADR 0066:** prefer
`class` / `interface` / `fn` over keyword `system` / `trait` / `fun`. Capsule and
purity **laws** in this ADR remain in force.
Design note: `docs/architecture/staqex-abstraction-model.md`,
`staqex-language-spec.md`.

## Context

Engineers need generics and interfaces; physicists need algebraic and
composite-system abstraction. Naïve OOP (mutable objects, inheritance,
methods that measure mid-call) would reintroduce classical islands and break
Never Leave the State.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. **Generics** parameterize carriers and packages (`State<T>`,
   `system Foo<T>`, `fn f<T>(…) -> State<T>`).
2. **Traits** define pure operator interfaces (algebraic / physical). They are
   the primary polymorphism mechanism.
3. **`system`** packages compound joint coordinates with **immutable** methods
   that return new system values (pure transformers).
4. **Inheritance (`extends`)** is not adopted for state types; use trait bounds
   and system composition.
5. Default callable bodies (`fn`, trait defaults, `system` methods) are
   **measure-free**. Any `measure`-capable API must be explicitly effectful and
   is outside Kernel / default abstraction style.
6. Collection metaphors: `map` ≈ pushforward is welcome later; `filter` that
   implies Bayesian conditioning is **not** introduced without a dedicated ADR
   (distinct from terminal `measure`).
7. Kernel PoC A/B and first harness do **not** require implementing generics /
   traits / `system`.

## Consequences

Positive:

- Extensible stdlib and user physics models without classical control creep.
- Clear engineer ↔ physicist vocabulary bridge.

Negative:

- Larger language surface before first executable Kernel.
- Need careful effect/purity checking in a future typechecker.

## Enforcement

Design / code review should reject:

- Mutable `self` updates that classicalize identity mid-superposition.
- Inheritance hierarchies as the main reuse story for `State` / `system`.
- Silent `measure` inside generic helpers.
- `filter`/`observe`-style stdlib that collapses or conditions without ADR.
