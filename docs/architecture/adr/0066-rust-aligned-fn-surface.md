# ADR 0066: Rust-aligned `fn` function declaration surface

## Status

Accepted (2026-07-23). Supersedes the function-keyword portion of ADR 0026,
ADR 0024, and the retired-keyword entries that declared `fn` abolished.

## Context

QPex's long-term implementation target is a Rust VM/compiler workspace. The
language currently combines `pub`, `fun`, and `->` even though `fun` and `fn`
have comparable learning cost for readers unfamiliar with either spelling.
Keeping `fun` solely for Kotlin resemblance does not materially reduce that
cost, while it makes the source surface less consistent with the intended VM
and future `impl`/trait vocabulary.

## Decision

1. The canonical function declaration keyword is `fn`:

   ```qpex
   pub fn advance() -> State<Float> {
       this._tick
   }
   ```

2. `fun` is removed from the language. It is not an alias and is not accepted
   during a compatibility period.
3. `fn init(...)` remains the constructor-only declaration exception that may
   omit a return annotation.
4. `pub fn main(...) -> Unit` is the canonical entry point.
5. The lexer/parser must report a deterministic retired/forbidden keyword
   diagnostic for `fun` and accept `fn` in top-level and class declarations.
6. All official examples, fixtures, tests, grammar, ADRs, and normative specs
   migrate in the same change. No source rewrite adapter is provided.

## Consequences

Positive:

- `pub fn`, `->`, and the Rust implementation target form a coherent surface.
- Future `impl` and trait syntax can use one callable vocabulary.
- There is no ambiguous two-keyword compatibility state.

Negative:

- Existing QPex source using `fun` requires a mechanical migration.
- Historical ADRs and teaching documentation need explicit status updates.

## Scope boundary

This ADR changes only the callable keyword. It does not introduce Rust-only
ownership, lifetimes, macros, or a Rust type system into QPex. `fn` is the
QPex language spelling in both the Python Kernel and the future Rust VM.

## Verification

- Phase 1 Red: `fn` acceptance, `fun` rejection, and no official `fun`
  declarations.
- Phase 2 Green: token/lexer/parser migration and source migration.
- Phase 3: documentation and reviewer-empathy cleanup.
