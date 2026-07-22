# ADR 0025: Failure as superposition — no exceptions

## Status

Accepted (2026-07-23).

Companions: `qpex-language-spec.md` §1.3, ADR 0021 (`project`), ADR 0024
(no null / exceptions bullet, expanded here).

## Context

Engineers expect `try`/`catch`. In a joint / amplitude language, non-local
escape destroys norm preservation and forces early decoherence — contradicting
Never Leave the State.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. **No** `Exception` type, `throw`, `try`, `catch`, or resume-via-handler
   control transfer in the object language.
2. Fallible outcomes are encoded as **carrier labels** (e.g. `Success` /
   `Error`, sum types, or `Symbol` atoms) inside `State<T>`, introduced via
   `when` / constructors, transformed via `map` and nested `when`.
3. To discard failure arms and renormalize, use **`project`** — never an
   exception edge.
4. `project` with $Z=0$ yields **`Vacuum`** inside the joint (ADR 0026), not
   a thrown fault. Host diagnostics may still log the event.
5. AST must **reject** `Throw` / `Try` / `Catch` nodes (see `qpex-ast-design.md`).
6. Canonical fallible carrier is **`Result<T, E>`** (ADR 0026).

## Consequences

Positive:

- Norm and superposition stay intact through fallible pipelines.
- Clear story: error = world-line, not crash.

Negative:

- Callers must thread `Success`/`Error` (or project) explicitly.
- Domain-fault UX for null `project` still open.

## Enforcement

Reject designs or examples that use `throw`/`catch` for QPex business logic,
or that treat uncaught exceptions as a supported failure mode.
