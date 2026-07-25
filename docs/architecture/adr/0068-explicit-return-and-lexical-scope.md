# ADR 0068: Explicit terminal returns and lexical function scope

## Status

**Accepted** (2026-07-25; design proposed 2026-07-23). Implemented in Kernel
and verified by LISS-0025's Phase 1 Red / Phase 2 Green / Phase 3 record
(SV 164/164). The Status field was not updated at the time of implementation;
this correction formally records the approval that the completed work already
reflects. No new decision or behavior change is introduced by this update.

Amends LISS-0021 and the function/module behavior in ADR 0054/0061. It does
not change the terminal observation rule.

## Context

QPex currently uses an implicit final expression as the return value of an
ordinary `fn`. In addition, module linking harvests `Operator` and closed
classical bindings from `pub fn` bodies into the entry environment. This makes
local names such as `WalkCoin` appear usable from another function even though
they were declared inside `build_observatory_coin`.

The result is executable but not lexically intuitive: a function appears to
be both a value-producing function and a configuration declaration, while its
local bindings can escape through a hidden linker path.

## Decision

1. Ordinary functions and methods return through an explicit terminal
   `return expression` statement.
2. `return` is permitted only as the final statement of an ordinary function
   or method. Early return and branch-local return are forbidden.
3. Implicit final-expression returns are removed. A non-`init` ordinary
   function must end with exactly one explicit return matching its annotation.
4. `main` cannot use `return`; it remains `-> Unit` and ends with terminal
   `measure`.
5. `fn init` cannot use `return`; it remains the constructor-only no-result
   declaration.
6. Name resolution is lexical:
   - module scope contains declarations and imports;
   - function scope contains parameters and local bindings;
   - nested `when` / `evolve` blocks cannot leak local bindings outward;
   - class fields are accessed through `this` and are not free module names;
   - a function cannot read a local declared in another function.
7. `Operator` bindings inside a function are ordinary locals. They are not
   harvested into the entry environment and cannot be referenced by sibling
   functions.
8. Cross-function values must use explicit parameters and return values.
   Cross-module declarations remain accessible only through the existing
   `pub` visibility and import/linking rules.
9. A future module-level constant/configuration declaration may be designed
   separately; this ADR does not introduce `const`.

## Scope boundary

This ADR does not add early classical control flow, mid-program measurement,
closures, captures, global mutable state, `const`, currying, or provider APIs.

## Consequences

- `return` makes value flow visible to students and physicists.
- `Operator` factories become ordinary functions rather than hidden config
  exporters.
- Existing examples using ADR 0054/0061 harvest require explicit migration.
- The linker becomes easier to reason about because function-local names do
  not enter the entry environment implicitly.

## Canonical example

```qpex
pub fn build_observatory_coin() -> Operator {
    Operator walk_coin = (X + Z) * inv_sqrt2
    return walk_coin
}

pub fn walk_observatory_step(
    coin: Operator,
    c: State<Qubit>,
    x: State<Position>
) -> State<(Qubit, Position)> {
    State<Qubit> next_c = apply(coin, c)
    State<Position> next_x = walk_shift(next_c, x)
    return next_c *|* next_x
}
```
