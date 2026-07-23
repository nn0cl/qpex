# WP-0009: `pub`-only visibility migration

## [DESIGN CHECK]

- Scope and expected behavior: retire source-level `public`; retain `pub` as
  the only public visibility spelling without changing access semantics.
- Specifications and files inspected: ADR 0058, ADR 0066, language
  specification §6.5, token specification, examples, fixtures, and linker
  tests.
- Component boundaries, ports/adapters, and VO/DTO candidates: lexer token
  table, parser diagnostics, source examples, and existing visibility/linker
  contracts; no new port or DTO.
- Applicable constraints: no implementation before the reviewed acceptance
  specification; no Rust-only visibility syntax; semantic AST value may remain
  `public`.
- Decisions, assumptions, unresolved ambiguities: `public` is a retired
  spelling with no compatibility or fail-safe path; `RETIRED_KEYWORD` is
  reused; `private`/`_` behavior is unchanged.
- Included and omitted AI context: included source visibility and module
  boundaries; omitted provider SDKs, QPU adapters, and unrelated language
  features.
- Task routing: deterministic repository inventory and tests; implementation
  only after Phase 1 review and explicit phase approval.
- Verification plan: Red tests, token/parser migration, source inventory,
  full SV/QASM/CLI/example/unit suites, and diff check.

## Approval gate

The initial work plan authorized design intake only. Phase 1 Red and Green
implementation were subsequently approved under `AGENTS.md`.

## Execution status

- Phase 1 Red: complete.
- Phase 2 Green: complete; `public` is retired and `pub` is canonical.
- Phase 3 Refactor: complete; current source and documentation use `pub`.
