# ADR 0067: Rust-aligned `pub`-only visibility surface

## Status

Accepted (2026-07-23).

Supersedes the `public` alias portion of ADR 0058. The semantic visibility
category remains public; this ADR changes only its QPex spelling.

## Context

QPex currently accepts both `pub` and `public` as contextual spellings for a
cross-module API. ADR 0066 selected Rust-aligned `fn` as the sole function
keyword. Keeping a Java-style `public` alias beside `pub fn` leaves the
surface with two spellings for the same access modifier and makes examples
less uniform.

## Decision proposal

1. The canonical QPex visibility modifier is `pub`.
2. `public` is retired and is not an alias or compatibility spelling.
3. No backward-compatibility path, automatic rewrite, warning-only mode, or
   fail-safe fallback accepts `public`; the compiler fails immediately.
4. The canonical entry point is `pub fn main(...) -> Unit`.
5. Default visibility remains module-private; leading `_` remains the
   class-private convention; `private` remains the existing legacy spelling
   where ADR 0058 permits it.
6. The AST and linker may continue to use the semantic value `public`; this
   is not a second source-level spelling.
7. The lexer/parser reports `RETIRED_KEYWORD` with replacement `pub` for
   source-level `public`.
8. All official examples, fixtures, grammar, normative specifications, and
   current teaching material use `pub`.

## Scope boundary

This ADR does not change access semantics, module linking, `private`/`_`,
class ownership, or the `fn` migration. It does not add Rust visibility
features such as `pub(crate)` or `pub(super)`.

## Consequences

- `pub fn` becomes the single concise public declaration form.
- Existing source containing `public` requires mechanical migration.
- The parser/tokenizer needs a retired-keyword diagnostic and fix-it.
- Historical ADRs may mention `public` only when describing the superseded
  spelling.

## Verification intent

- `pub` remains accepted for functions, classes, structs, enums, fields, and
  entry points where currently supported.
- `public` is rejected deterministically with replacement `pub`.
- Cross-module visibility behavior is unchanged after source migration.
- Full specification verification, examples, QASM, and test suites remain
  green.
