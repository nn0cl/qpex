# LISS-0024: Make `pub` the only public visibility spelling

## Metadata

- Local issue ID: LISS-0024
- Status: Complete
- Phase: Architecture Path → Feature Path
- Type: language surface migration
- Priority: P1
- Related: ADR-0058, ADR-0067, LISS-0023

## Acceptance specification

- [x] `pub` remains accepted for every currently supported public declaration.
- [x] `public` produces `RETIRED_KEYWORD` with replacement `pub`.
- [x] No compatibility alias, warning-only mode, automatic rewrite, or
  fail-safe fallback accepts `public`; invalid source fails immediately.
- [x] `pub fn main() -> Unit` is the only runnable public entry spelling.
- [x] Semantic visibility remains unchanged: public, module-private, and
  leading-underscore/private access checks behave as before.
- [x] Official examples, fixtures, grammar, normative specifications, and
  current documentation contain no active `public` declaration.
- [x] No `pub(crate)`, `pub(super)`, or other Rust-only visibility syntax is
  introduced.
- [x] Full SV, QASM, CLI, example, and unit test suites pass.

## Non-goals

- Changing module linking or access policy.
- Adding visibility effects, ownership, inheritance, or package exports.
- Maintaining a source compatibility alias for `public`.

## AT-TDD sequence

1. Phase 1 Red: tests for `pub` acceptance and `public` rejection, plus a
   source inventory of active declarations.
2. Phase 2 Green: token/parser migration and source/document migration.
3. Phase 3 Refactor: terminology, diagnostics, and reviewer-empathy cleanup.

## Ambiguity boundary

The AST semantic value may remain `public` for compatibility with internal
implementation names. Only the source-level token spelling is changing.

## Verification record

- Phase 1 Red: `tests/test_pub_visibility_red.py` failed against the previous
  `pub`/`public` alias behavior.
- Phase 2 Green: `pub` active, `public` retired, all official source migrated;
  SV 164/164, QASM 3, and all `tests/test_*.py` pass.
- Phase 3 Refactor: diagnostics, current documentation, examples, and
  reviewer-facing terminology aligned with the `pub`-only surface.
