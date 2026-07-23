# QPex specification: explicit returns and lexical scope

## Normative proposal

An ordinary function has the shape:

```qpex
pub fn f(a: State<Int>) -> State<Int> {
    State<Int> doubled = a + a
    return doubled
}
```

The `return` statement is terminal. It is the only way for an ordinary
function or method to produce its declared result.

The following are invalid:

```qpex
fn implicit() -> State<Int> {
    dirac(1)
}

fn early(a: State<Int>) -> State<Int> {
    return a
    return dirac(0)
}
```

`main` remains:

```qpex
pub fn main() -> Unit {
    State<Int> answer = f(coin())
    measure answer
}
```

It cannot return a value. `init` also cannot return a value.

## Scope rules

- A parameter and every local Type-First binding belong to the current
  function scope.
- A local binding is not visible from a sibling function, another module, or
  `main` merely because its declaring function is `pub`.
- `Operator` is a normal classical/operator value in this respect.
- Passing an `Operator` as an argument or returning it is explicit value flow.
- Imports expose declarations, not another function's locals.
