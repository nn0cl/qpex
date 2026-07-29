# Staqex specification: `pub`-only public visibility

## Normative rules

1. `pub` marks a declaration as visible across module boundaries.
2. An omitted modifier is module-private.
3. A leading `_` (or the existing permitted `private` spelling) retains its
   class-private meaning.
4. `public` is retired. It is not equivalent to `pub` and must produce a
   `RETIRED_KEYWORD` diagnostic whose replacement is `pub`.
5. No compatibility alias, automatic rewrite, warning-only mode, or fail-safe
   fallback accepts `public`; invalid source fails immediately.
6. The entry point is `pub fn main(...) -> Unit`.

## Acceptance scenarios

### Scenario A — canonical public function

Given:

```staqex
pub fn advance() -> State<Float> {
    value
}
```

The declaration is accepted and remains exportable under the existing module
linking rules.

### Scenario B — retired long spelling

Given:

```staqex
pub fn advance() -> State<Float> {
    value
}
```

Compilation fails with `RETIRED_KEYWORD` and recommends `pub`.

### Scenario C — entry point

```staqex
pub fn main() -> Unit {
    State<Int> answer = coin()
    measure answer
}
```

The program remains runnable and terminal measurement semantics are unchanged.
