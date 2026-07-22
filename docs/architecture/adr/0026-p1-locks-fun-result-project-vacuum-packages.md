# ADR 0026: P1 locks — `fun`, `Result`, `project` Z=0 → Vacuum, packages required

## Status

Accepted (2026-07-23). Adjudicator reply to doc-audit 2026-07-23.

Companions: `qpex-language-spec.md`, `qpex-stdlib-combinators.md`,
`docs/collaboration/spelling-cheat-sheet.md`.

## Context

Doc audit scored ~8.5/10 with open P1 items blocking Hold-unseal judgment.
Adjudicator locked spellings and null-project UX without introducing
exceptions.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. **Function keyword:** surface spelling is **`fun` only**. Keyword `fn` is
   **abolished** (not an alias). Styler/parser reject `fn` in new code.
2. **Fallible carrier:** canonical type name is **`Result<T, E>`** (short
   `Result` when `E` is default/`String`). `Success` / `Error` (or equivalent
   constructors) are basis labels inside `State<Result<T, E>>` — not
   exceptions (ADR 0025).
3. **`project` when $Z=0$:** must **not** throw / `catch` / crash the joint
   narrative. Normative vacuum behavior is finalized in **ADR 0034**: `State.vacuum()`
   with norm 0, absorbing under pure ops, safe empty `measure`.  
   **Rejected:** domain exception; silent identity.
4. **Packages:** `package` / `import` declarations are **required** for
   compilation units that define `class` / `interface` / top-level `fun`
   (subsystem / namespace borders). Bare Kernel PoC A/B scripts without
   packages remain allowed until the package fixture wave (exemption only).

## Consequences

Positive:

- DX and failure model fully Kotlin-aligned and exception-free.
- Null projection no longer contradicts “never crash” + ADR 0025.

Negative:

- Vacuum representation needs a short follow-up mini-spec.
- Docs/examples still using `fn` must migrate.

## Enforcement

Reject `fn`, exception-based $Z=0`, and new library modules without `package`
in normative examples. Prefer `Result<T, E>` in fallible narratives.
