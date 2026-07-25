# QPex function signatures and measure-free returns

## Status

Accepted acceptance specification for LISS-0021 after Phase 2 Green. Phase 3
refactoring and future language extensions remain separate work.

## Invariants

1. `State<T>` may pass through any ordinary function or method without
   classical collapse.
2. Only `main` may own the terminal `measure`.
3. Ordinary functions and methods end with an explicit terminal `return`.
4. `init` constructs an object and has no result value.
5. `main` has the explicit host-lifecycle result type `Unit`; terminal
   `measure` is an effect, not the `Unit` value.
6. Omitted return annotations are errors for ordinary functions, class
   methods, and `main`; `init` is the only untyped declaration exception.

## Scenarios

### Scenario A — zero-argument function returns a typed value

Given a measure-free function with an explicit return type and no arguments

```qpex
fn origin() -> State<Int> {
    return dirac(0)
}
```

When `main` calls `origin()` and then measures the result

Then the result is `0`, and the function itself performs no measurement.

### Scenario B — multi-argument state function preserves the joint state

Given a function with two State inputs and a State return type

```qpex
fn add(a: State<Int>, b: State<Int>) -> State<Int> {
    return a + b
}
```

When the caller invokes it with two correlated or independent state
coordinates

Then the returned state contains the specified pushforward result and remains
uncollapsed until `main` measures it.

### Scenario C — class method returns a new value

Given an immutable class method with an explicit return type

```qpex
class Counter {
    val value: Int

    fn next() -> State<Int> {
        return dirac(this.value + 1)
    }
}
```

When the caller invokes `counter.next()`

Then the method result has the declared type and the receiver is not measured
or implicitly replaced.

### Scenario D — arbitrary supported input arity is checked

Given functions with zero, one, and multiple parameters

When a call supplies too few or too many arguments

Then compilation or deterministic runtime binding reports an arity diagnostic;
it must not silently project unrelated parameter coordinates.

### Scenario E — return type mismatch is rejected

Given a function declared as `-> State<Int>`

When its terminal return expression has an incompatible carrier, product arity, or
dimension

Then compilation fails with a type diagnostic before evaluation.

### Scenario F — observation remains terminal

Given an ordinary function or class method containing `measure`

When the source is checked or run

Then compilation/evaluation rejects the function as a non-terminal observation
boundary.

### Scenario G — `main` has an explicit Unit result

Given `pub fn main() -> Unit`

When it reaches its terminal `measure`

Then the host lifecycle completes with `Unit`, and `main` is not a general
State-returning function.

### Scenario H — bare main signatures are rejected

Given `pub fn main()` without a return annotation

When the source is checked

Then compilation rejects the entry point because `main -> Unit` is required.

### Scenario I — legacy untyped helper is rejected

Given `fn build_link_witness() { Float ideal_correlation = 1.0 }`

When the source is checked

Then compilation reports `MISSING_RETURN_TYPE`.

### Scenario J — constructor remains untyped

Given a class constructor declared as `fn init(...) { ... }`

When the source is checked

Then the declaration is accepted without a return annotation.

## Out of scope

- Early exits and branch-local returns. A terminal `return expression` is in
  scope and required for ordinary functions and methods.
- Currying and partial application.
- Trait `impl` dispatch.
- Mid-program classical extraction from `State<T>`.
- Provider-specific QPU submission.
