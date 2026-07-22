# ADR 0017: Surface vocabulary — state / span / evolve / measure

## Status

Accepted (2026-07-22). **Surface mixture spelling superseded by ADR 0024:**
use `when` instead of `span` in new normative text. Other decisions
(`state` / `coin` / `dirac` / `evolve` / `measure`) remain in force.

## Context

Provisional MVP text used `let`, `observe`, and `fair_bit()`, which read as
classical binding and collide with PPL conditioning vocabulary. Parallel design
work chose physics-narrative keywords aligned with the researcher persona and
keyboard constraints, and rejected `if` as early-collapse narrative.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. Top-level binder is `state`, not `let`.
2. Preparation helpers: `coin()`, `dirac(c)` (literal sugar optional later).
3. Superposition / mixture form was `span` (2026-07-22); **now `when`**
   (ADR 0024) — still **no** classical `if`.
4. Pure multi-step state update form is `evolve (… ) { … }` — **no** classical
   `while`/`for`/`return` at the language-law level.
5. Terminal collapse keyword is **`measure`** (sampling collapse). The former
   name `observe` in older docs denotes the same law but is **retired** as
   surface spelling to avoid PPL conditioning confusion.
6. `let` is allowed only as **local** binding inside `evolve` blocks.
7. Document the lexicon in `docs/architecture/qpex-syntax-vocabulary.md`.

## Consequences

Positive:

- Narrative alignment with Dirac / evolution / projective measurement.
- Clearer differentiation from Stan/Pyro `observe`.

Negative:

- Docs and fixtures must be migrated from `let`/`observe`.
- `measure` is 7 letters (slightly over the 4–6 ideal).

## Enforcement

Code review should reject:

- Top-level `let` / `if` / mid-program `measure` in accepted examples.
- Reintroducing `observe` as the preferred surface keyword without superseding
  this ADR.
- Treating `span` as classical short-circuit `if`.
