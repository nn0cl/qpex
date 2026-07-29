# Agent sync: token specification (ADR 0035)

Date: 2026-07-23. Step 2 Lexer / Parser contract.

Canonical: `docs/architecture/staqex-token-specification.md`.

## Active

`class` `interface` `package` `import` `fn` `state` `let` `when`
`coin` `dirac` `vacuum` `evolve` `measure` `snapshot` `inspect`

## Forbidden → hard error

`if` `switch` `while` `for` `break` `return` `new` `null`
`try` `catch` `throw` `Thread` `async` `await`

## Retired → linter fix-it

`observe`→`measure` · `span`→`when` · `fun`→`fn` · `trait`→`interface`

## Reserved op

`|>` → `PipeOp` / AST `Pipe`
