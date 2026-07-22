# ADR 0027: Entry point — `public fun main` + terminal `measure`

## Status

Accepted (2026-07-23).

Design: `qpex-language-spec.md` §4 Entry Point & Execution Lifecycle.

## Context

Runnable PoC / CLI needs a defined start and end. Never Leave the State
requires collapse only at the end; Kotlin DX prefers `fun main()`.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. Entry point is top-level **`public fun main()`** or
   **`public fun main(args: State<List<String>>)`**.
2. `main` does **not** return classical `Int` exit codes in the object
   language; termination is via final **`measure`**, with classical output
   through `MeasureSinkPort`. Host exit status is adapter-level.
3. CLI `args` are **`State<List<String>>`** (lifted).
4. **`measure` is allowed only as the last statement of `main`** (or of a
   Kernel script desugared to implicit `main`). Mid-body measure → Early
   Collapse Error.
5. AST: `MainDecl` / `EntryPoint` binds the entry `fun`; body ends with
   `Measure`.
6. Kernel PoC A/B scripts without explicit `main` are sugar for implicit
   `main` until the entry fixture wave.

## Consequences

Positive:

- Familiar DX; lifecycle matches Language Law end-to-end.

Negative:

- Multi-measure / REPL / library-only packages need separate modes later.

## Enforcement

Reject normative examples with mid-`main` `measure`, classical `int main`
returns, or raw `String[]` args without `State`.
