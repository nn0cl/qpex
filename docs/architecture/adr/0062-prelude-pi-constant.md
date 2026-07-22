# ADR 0062: Prelude classical constant `pi`

## Status

**Accepted** (2026-07-23). Thin follow-on to ADR 0031 (stdlib / Math).

Follow-up Issue: [LISS-0007](../../issues/LISS-0007-prelude-pi-constant.md).

## Context

Examples and READMEs spell angles as $e^{i\pi}$ / `π`, but sources used the
magic float `3.141592653589793`. Full `qpex.math.Math` Float surface remains
later-phase (ADR 0031); a classical constant unblocks blackboard DX.

## Dependency Adoption Evidence

Not applicable (stdlib constant; no new package dependency).

## Decision

1. Prelude registers classical scalar **`pi: Float`** (= IEEE `math.pi`) in
   `compiler/qpex/stdlib/prelude.py` (`PRELUDE_CONSTANTS`).
2. Evaluator seeds `scalars["pi"]`; typechecker seeds `env["pi"]` as
   `Classical<Float>` (dimensionless).
3. `pi` may appear in classical arithmetic and as parameters
   (`phase(s, pi)`, `phase(s, pi / 2.0)`, `2 * pi`).
4. Mixing `pi` / `Math.pi` (or any `Classical`) with a quantum `State` wire via
   `+`/`-`/`*`/`/` is a static error (`TYPE_MISMATCH` + legacy
   `EXPECT_CLASSICAL_ONLY_ERROR`).
5. Numeric **literals** beside `pi` (`pi / 2.0`) remain Allowed as classical
   sugar; real State coordinates are not.
6. **`Math.pi`** is an Attr alias of the same classical constant (not a
   State→State Math operator). Broader `qpex.math` Float APIs remain later-phase.

## Consequences

Positive: examples read like chalkboard formulas; `Math.pi` matches textbook spelling.  
Negative: still not a full Math package.

## Enforcement

Reject designs that lift `pi` into a `State` carrier mid-program without
`dirac` / explicit lift.

## Verification

- `tests/test_prelude_pi.py` (incl. `Math.pi`)
- Examples use `pi`; SV suite green
