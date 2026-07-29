# LISS-0113: PalQuantum rename — project name + file extension

## Metadata

- Local issue ID: LISS-0113
- GitHub issue: not created
- Status: **plan** (2026-07-29)
- Phase: design-intake
- Type: project-wide refactor / branding
- Priority: P1
- Planning size: L
- Owner/agent: —
- Related branch: `feature/liss-0113-palquantum-rename`
- Parent: [WP-0025](../work-plans/WP-0025-qpex-v1-north-star.md)
- Depends on: LISS-0080 **complete** (timing gate — rename after HIR closeout)
- Does not block: LISS-0075 (can proceed in parallel or after)

## Summary

Rename the project from **QPex** to **PalQuantum** and change the source
file extension from `.qpex` to `.pq`.

Timing rationale: LISS-0080 (HIR, the last major structural Issue before
LISS-0075) is now complete. This is the smallest rename window before
Physics IR / linear analysis add further references. Post-rename, all
subsequent Issues use PalQuantum / `.pq` vocabulary.

## Scope

### Rename targets

| Category | From | To | Count |
|---|---|---|---|
| Source file extension | `.qpex` | `.pq` | 43 files |
| Python package directory | `compiler/qpex/` | `compiler/palquantum/` | — |
| Python import paths | `compiler.qpex` | `compiler.palquantum` | ~136 files |
| CLI entry point | `python3 -m compiler.qpex` | `python3 -m compiler.palquantum` | docs / QUICKSTART |
| Project name string | `QPex` | `PalQuantum` | ~340 doc files |
| GitHub repo name | `qpex` | `palquantum` | Adjudicator action |
| Agent instruction files | `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*.mdc`, `.github/copilot-instructions.md`, `.grok/rules/*.md` | updated project name | all |

### Out of scope

- Language semantics changes.
- ADR numbering or content (ADRs reference the language, not the package path).
- Test logic or assertions.
- QPex language axioms content (rename the label, not the meaning).

## Slices

| Slice | Scope |
|---|---|
| **A** | Rename `compiler/qpex/` → `compiler/palquantum/`; update all Python imports; update CLI entry; update `QUICKSTART.md` |
| **B** | Rename `.qpex` → `.pq` in all `examples/`; update parser / file-loading references if any |
| **C** | Update all `docs/` text references (`QPex` → `PalQuantum`, `.qpex` → `.pq`); update agent instruction files |

All slices land in one PR on this branch (mechanical rename — no AT-TDD
phase gate required; verification = test suite stays green after each slice).

## Adjudicator Decision Points

- [ ] Confirm new project name: **PalQuantum** (capitalisation / spacing).
- [ ] Confirm new extension: **`.pq`**.
- [ ] Confirm GitHub repo rename is Adjudicator action (not agent action).
- [ ] Approve Slice A (Python package rename) to begin.
- [ ] Approve Slice B (extension rename).
- [ ] Approve Slice C (docs + agent instructions).

## Non-goals

- Changing language semantics or axioms.
- Renaming ADR numbers.
- GitHub Actions / CI workflow changes beyond path references.

## Verification

After each slice: all existing test suites pass without modification.
