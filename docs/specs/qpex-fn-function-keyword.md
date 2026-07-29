# Staqex `fn` function keyword specification

## Status

Accepted with ADR-0066; implementation begins at LISS-0023 Phase 1 Red.

## Invariants

1. `fn` declares functions, methods, constructors, and `main`.
2. `fun` is not a valid alias and produces a retired-keyword diagnostic.
3. Return annotations and terminal-expression rules are those of LISS-0021.
4. `fn init(...)` is the only unannotated declaration exception.

## Scenarios

### Scenario A — `fn` is accepted

Given `pub fn advance() -> State<Float> { value }`

When the source is checked

Then compilation accepts the declaration.

### Scenario B — `fun` is rejected

Given `pub fun advance() -> State<Float> { value }`

When the source is checked

Then compilation rejects it with a retired/forbidden keyword diagnostic.

### Scenario C — constructors use `fn`

Given `fn init(value: Int) { this.value = value }`

When the class is checked

Then the constructor is accepted without a return annotation.
