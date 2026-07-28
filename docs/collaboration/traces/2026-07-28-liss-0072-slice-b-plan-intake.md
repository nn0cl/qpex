# Trace: LISS-0072 Slice B plan intake

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0072 |
| Slice | B — formatter + round-trip + migration parity |
| Phase | phase-0-design |
| Branch | `feature/liss-0072-slice-a-red` |
| Implementation | **forbidden** until Slice B plan approval |

## [DESIGN CHECK]

- Scope and expected behavior: propose Slice B only — canonical formatter emit,
  parse-format-parse structural AST equality, migration parity, and a minimal
  `qpex format` CLI.
- Specifications and files inspected: `docs/issues/LISS-0072-lossless-cst-formatter-and-source-versioning.md`;
  `docs/specs/qpex-v1-cst-formatter-plan.md`; `compiler/qpex/migrate_unicode_math.py`;
  `tests/fixtures/migration/`; `tests/test_unicode_math_migrator_red.py`.
- Component boundaries: formatter module is separate from parser/semantic code;
  migration corpus is the initial oracle; `qpex_version` and EBNF remain out.
- Applicable constraints: no byte-identical reproduction requirement; no parser
  rewrite beyond what formatter entry needs.
- Decisions, assumptions, and unresolved ambiguities: spacing policy stays
  minimal and stable; selected extra snippets are allowed only if fixtures leave
  a proven gap.
- Included and omitted AI context: included CST plan, migrator behavior, and
  golden fixtures; omitted runtime/backends/versioning/EBNF.
- Task routing: docs-only plan update.
- Verification plan: review slice boundaries and corpus choices; no compiler or
  test mutations in this step.

## Requested approval

**Plan approval** for Slice B only:

- formatter core in `compiler/qpex/format.py`;
- canonical Unicode emit for M-P02–M-P04;
- structural AST round-trip oracle;
- migration corpus parity;
- minimal `qpex format` CLI (`stdout`, `--write`, `--check`, `-o`).

Green is not implied unless later authorized.

## Next safe action

Adjudicator plan approval → Slice B Phase 1 Red.
