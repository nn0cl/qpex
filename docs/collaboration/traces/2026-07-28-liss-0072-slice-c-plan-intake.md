# Trace: LISS-0072 Slice C plan intake

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0072 |
| Slice | C — source versioning + fix-it surfacing |
| Phase | phase-0-design |
| Branch | `feature/liss-0072-slice-b-red` |
| Implementation | **forbidden** until Slice C plan approval |

## [DESIGN CHECK]

- Scope and expected behavior: propose Slice C only — package-level
  `staqex_version` validation and diagnostic fix-it surfacing.
- Specifications and files inspected: `docs/issues/LISS-0072-lossless-cst-formatter-and-source-versioning.md`;
  `docs/specs/staqex-v1-cst-formatter-plan.md`; `docs/specs/staqex-v1-normative-rebaseline-register.md`;
  `compiler/staqex/tokens.py`; `compiler/staqex/lexer.py`; `compiler/staqex/cli.py`.
- Component boundaries: parser/diagnostic work only; no formatter policy or
  EBNF updates in this slice.
- Applicable constraints: `staqex_version` is accept/reject metadata, not a full
  semantic version switch; fix-its remain advisory.
- Decisions, assumptions, and unresolved ambiguities: unsupported-version
  diagnostic code name remains to be fixed in Red; `FORBIDDEN_KEYWORD`
  replacements stay conservative.
- Included and omitted AI context: included version-marker and replacement
  payload evidence; omitted formatter/EBNF/runtime/backend paths.
- Task routing: docs-only plan update.
- Verification plan: review slice boundaries and diagnostic scope; no compiler
  or test mutations in this step.

## Requested approval

**Plan approval** for Slice C only:

- parse package-level `staqex_version = "1.0"` metadata;
- reject unsupported versions with a named diagnostic;
- surface fix-it payloads for `RETIRED_KEYWORD`;
- keep fix-its advisory only during compile.

Green is not implied unless later authorized.

## Next safe action

Adjudicator plan approval → Slice C Phase 1 Red.
