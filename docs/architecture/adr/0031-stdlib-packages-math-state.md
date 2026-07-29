# ADR 0031: Stdlib packages — Math as State→State operators

## Status

Accepted as **design baseline** (2026-07-23).

Canonical: `docs/architecture/staqex-stdlib-packages.md`.
Combinators remain ADR 0021 (`map` / `project` / `interfer`).

Implementation Hold except Kernel surface prep already specified.

## Context

Classical `Math.sin(double)` clashes with universal `State<T>`. Researchers
still need textbook spellings (`sin`, `exp`) that act on entire mixtures.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. Stdlib is organized under `staqex.math`, `staqex.io`, `staqex.state`,
   `staqex.collection`, `staqex.debug` as in the packages note.
2. **`staqex.math.Math`** functions have type `State<T> → State<U>` (typically
   `State<Float> → State<Float>`) implemented as **pointwise `map` /
   pushforward**, not scalar islands.
3. Extension methods (`x.sin()`) desugar to the same operators.
4. **`staqex.state.Distribution`** owns preparation helpers; surface `coin` /
   `dirac` are aliases.
5. **`staqex.io`** obeys ADR 0029; **`staqex.debug.Inspector`** obeys ADR 0030.
6. **`staqex.collection`** provides immutable collections whose indices/values
   may be `State<_>`.
7. Kernel PoC A/B does not require Math/Float/collections/io/debug modules.

## Consequences

Positive:

- Paper formulas transfer as `Math.sin(phase)` on superpositions.
- Clear package map for agents.

Negative:

- Float / continuous / unitary APIs still open under ADR 0016.

## Enforcement

Reject stdlib designs that expose mid-program classical `Float` APIs as the
primary surface, or mid-pure `File.write` of live states.

## See also

- **[ADR 0062](0062-prelude-pi-constant.md)** — prelude classical constant `pi`
  (thin follow-on; full Math Float APIs still later-phase).
