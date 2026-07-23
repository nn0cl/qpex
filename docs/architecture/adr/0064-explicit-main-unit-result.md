# ADR 0064: Explicit `main` result type

## Status

Accepted (2026-07-23). Follow-up design for ADR 0027 and LISS-0021.

## Context

QPex currently treats `main` as a special no-result entry point written as
`public fun main(...)`. Ordinary functions are being given explicit return
types, but leaving `main` without a signature preserves an implicit result
contract and makes examples inconsistent with the language's function model.

Terminal `measure` is an observation effect. It is not the ordinary return
value of a function and must remain owned by the entry-point lifecycle.

## Decision proposal

1. `main` must declare an explicit host-lifecycle result type:

   ```qpex
   public fun main() -> Unit {
       State<Int> result = coin()
       measure result
   }
   ```

2. `Unit` is not a quantum carrier and cannot be measured. It describes the
   host lifecycle result after terminal observation has completed.
3. `main` still may not have a final expression. Its terminal executable is
   exactly one final `measure` statement.
4. `measure` remains forbidden in ordinary functions and methods.
5. Implicit `main` result behavior and bare `public fun main(...)` examples are
   removed from normative examples and official examples.
6. `main(args: State<List<String>>)` remains supported, with `-> Unit`.

## Consequences

Positive:

- Every function-like declaration has an explicit result contract.
- The observation boundary remains visibly separate from the host lifecycle
  result.
- Examples teach one consistent signature rule.

Negative:

- Grammar, AST, parser, typechecker, CLI entry handling, tests, fixtures, and
  all official examples require migration.
- `Unit` must be represented in the type system without becoming a State
  payload or a measurable value.

## Scope boundary

This ADR does not make `measure` return a `T` from `main`, does not add classical
mid-program extraction, and does not define provider-specific process exit
codes. Host exit status remains an adapter concern.

## Verification

- Phase 1 Red: explicit-`Unit` main acceptance tests and example inventory.
- Phase 2 Green: `MainDecl` result metadata, parser/typechecker enforcement,
  then example/fixture migration.
- Full SV, QASM, CLI, and official-example verification after migration.
