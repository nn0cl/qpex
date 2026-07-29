# ADR 0062: Prelude classical constants (`pi`, `sqrt2`, `inv_sqrt2`)

## Status

**Accepted** (2026-07-23; amended same day for √2). Thin follow-on to ADR 0031
(stdlib / Math).

Follow-up Issues: [LISS-0007](../../issues/LISS-0007-prelude-pi-constant.md),
[LISS-0009](../../issues/LISS-0009-chalkboard-dx.md).

## Context

Examples and READMEs spell angles as $e^{i\pi}$ / `π` and Hadamard coins as
$(X+Z)/\sqrt{2}$, but sources used magic floats `3.1415…` / `0.7071…`. Full
`staqex.math.Math` Float surface remains later-phase (ADR 0031); classical
constants unblock blackboard DX.

## Dependency Adoption Evidence

Not applicable (stdlib constants; no new package dependency).

## Decision

1. Prelude registers classical scalars in
   `compiler/staqex/stdlib/prelude.py` (`PRELUDE_CONSTANTS`):
   - **`pi: Float`** (= IEEE `math.pi`)
   - **`sqrt2: Float`** (= `√2`)
   - **`inv_sqrt2: Float`** (= `1/√2`)
2. Evaluator seeds `scalars[...]`; typechecker seeds `env[...]` as
   `Classical<Float>` (dimensionless).
3. Constants may appear in classical arithmetic, Operator coefficients, and
   parameters (`phase(s, pi)`, `phase(s, pi / 2.0)`, `(X+Z)*inv_sqrt2`).
4. Mixing prelude / `Math.*` classicals with a quantum `State` wire via
   `+`/`-`/`*`/`/` is a static error (`TYPE_MISMATCH` + legacy
   `EXPECT_CLASSICAL_ONLY_ERROR`).
5. Numeric **literals** beside constants (`pi / 2.0`) remain Allowed as classical
   sugar; real State coordinates are not.
6. **`Math.pi` / `Math.sqrt2` / `Math.inv_sqrt2`** are Attr aliases of the same
   classical constants (not State→State Math operators). Broader `staqex.math`
   Float APIs remain later-phase.
7. **Deferred (LISS-0009):** Operator-position bare `H` sugar for Hadamard.

## Consequences

Positive: examples read like chalkboard formulas.  
Negative: still not a full Math package (`sqrt` of arbitrary expr deferred).

## Enforcement

Reject designs that lift these into a `State` carrier mid-program without
`dirac` / explicit lift. Ban new magic `π` / `√2` decimals in official examples
([examples-catalog-conventions](../../collaboration/examples-catalog-conventions.md)
chalkboard test).

## Verification

- `tests/test_prelude_pi.py` (incl. `Math.*` aliases + Coin via `inv_sqrt2`)
- Examples use prelude spelling; SV suite green
