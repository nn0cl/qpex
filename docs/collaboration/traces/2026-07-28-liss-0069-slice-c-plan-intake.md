# Trace: LISS-0069 Slice C plan intake

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0069 |
| Path | Feature Path — documentation / plan only |
| Phase | phase-0-design (Slice C) |
| Branch | `docs/liss-0069-slice-c-cli-plan` |
| Implementation | **forbidden** until plan approval |

## [DESIGN CHECK]

- Scope and expected behavior: Propose CLI `qpex migrate` wrapping
  `migrate_unicode_math_source` with stdout preview, `--write`, `--check`,
  optional `-o`; one file only; no rewrite-rule changes.
- Specifications and files inspected: LISS-0069 Issue; Slice B migrator
  companion; `cli.py` subcommand allowlist; migration matrix M-P02–M-P04.
- Component boundaries: Adapter = CLI I/O; UseCase/library = Slice B pure
  function; no new Domain policy.
- Applicable constraints: Clean Architecture ports for I/O; formatter emit
  deferred to LISS-0072; no work on `main` without PR.
- Decisions, assumptions, and unresolved ambiguities: Subcommand name locked
  as `migrate` pending Adjudicator confirm; stdin/`-e` deferred; recursive
  walk out of Slice C.
- Included and omitted AI context: Included Issue + CLI companion draft;
  omitted full lexer/parser, SV corpus, unrelated ADRs.
- Task routing: documentation / plan intake (this agent); Red later after
  approval.
- Input/output evidence contract: N/A (no model output in runtime).
- Verification plan: Docs-only PR; Adjudicator plan checklist on Issue;
  no tests until Phase 1 Red authorized.

## Artifacts

- `docs/specs/qpex-unicode-math-migrate-cli.md` (new)
- Issue / open-work-register / migration matrix / migrator pointer updates

## Next safe action

Adjudicator plan approval → Phase 1 Red (CLI tests only).
