# Trace: docs brush-up + template alignment (product-owned)

- Date: 2026-07-23
- Path: Architecture / Fast (documentation)
- Agent: Cursor

## Intent

Brush up product docs for the modern OOP / visibility Kernel surface, and
align **target-owned** entry docs with `llm-project-template` adoption
expectations — without adding files the init/copy script marks unnecessary.

## Explicitly not added

Per `scripts/lib/collaboration-template-paths.sh`:

- Excluded from copy: `docs/collaboration/traces/*.md` (template history),
  `docs/issues/LISS-*.md`, `docs/specs/template-rollout.md`
- Not in `collaboration_template_paths`: template `README*`, template
  `QUICKSTART*`, `docs/research/**` essays, `.github/FUNDING.yml`

Those remain template-repo concerns. QPex keeps its **own** `README*` /
`QUICKSTART*` as product docs.

## Artifacts touched

- `README.md`, `README.ja.md`, `QUICKSTART.md`, `QUICKSTART.ja.md`
- `docs/architecture/README.md`, `physicist-dx-harmony.md`, ADR 0056
- `docs/specs/qpex-language-specification.md` §6.4–§6.5
- `docs/collaboration/agent-sync-modern-oop-visibility.md`
- `AGENTS.md`, `CLAUDE.md`, `compiler/README.md`, `examples/README.md`

## Verification

Documentation-only; Kernel suite unchanged expectation:
`python3 tests/spec_verification/run_all.py`.
