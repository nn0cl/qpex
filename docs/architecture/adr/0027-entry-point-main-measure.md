# ADR 0027: Entry point — `pub fn main` + terminal `measure`

## Status

Accepted (2026-07-23).

Design: `qpex-language-spec.md` §4 Entry Point & Execution Lifecycle.

## Context

Runnable PoC / CLI needs a defined start and end. Never Leave the State
requires collapse only at the end; the callable surface uses `fn` (ADR 0066).

## Dependency Adoption Evidence

Not applicable.

## Decision

1. Entry point is top-level **`pub fn main() -> Unit`** or
   **`pub fn main(args: State<List<String>>) -> Unit`**.
2. `main` does **not** return classical `Int` exit codes in the object
   language; termination is via final **`measure`**, with classical output
   through `MeasureSinkPort`. Host exit status is adapter-level.
3. CLI `args` are **`State<List<String>>`** (lifted).
4. **`measure` is allowed only as the last statement of `main`**.
   Mid-body measure → Early Collapse Error (`EARLY_COLLAPSE_ERROR`).
5. AST: `MainDecl` / `EntryPoint` binds the entry `fn`; body ends with
   `Measure`.
6. **Implicit-main / script-style top-level executables are retired**
   (ADR **0037**). Top-level `state` / Type-First / `measure` /
   `evolve` → **`TOPLEVEL_EXECUTION_ERROR`**. Runnable units must use
   an explicit `pub fn main() -> Unit { … }`. Library-only packages without
   `main` remain valid.

## Consequences

Positive:

- Familiar DX; lifecycle matches Language Law end-to-end.
- Entry and scope are lexically obvious (ADR 0037).

Negative:

- Multi-measure / REPL / library-only packages need separate modes later.
- Legacy script snippets must wrap in `main`.

## Enforcement

Reject normative examples with mid-`main` `measure`, classical `int main`
returns, raw `String[]` args without `State`, or top-level executable
statements outside `main` (ADR 0037).
