# ADR 0035: Token specification for Lexer / Parser (Active / Forbidden / Retired)

## Status

Accepted (2026-07-23).

Canonical: `docs/architecture/qpex-token-specification.md`.
Vocabulary triage confirmed against `qpex-syntax-vocabulary.md` §3.8 and AST design.

## Context

Step 2 (Lexer / Parser) needs a normative token map so agents do not invent
classical keywords or revive retired spellings.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. Adopt Active / Forbidden / Reserved-op / Retired triage as in the token
   specification document.
2. Forbidden keywords are **hard compile errors** with guidance messages
   (e.g. `if` → use `when`).
3. Retired keywords are **linter warnings + fix-its**, not Active grammar.
4. Reserve `\|>` as `PipeOp` / AST `Pipe` (semantics TBD).
5. Kernel PoC may implement a subset of Active keywords first, but must enforce
   the Forbidden set from day one.

## Consequences

Positive:

- Clear Step 2 contract; axiom-safe surface.

Negative:

- Contextual keywords (`else`, `to`, `public`) need careful Parser design.

## Enforcement

Reject PRs that parse `if`/`async`/`new` as identifiers or that treat `span`/
`fn` as Active without deprecation path.
