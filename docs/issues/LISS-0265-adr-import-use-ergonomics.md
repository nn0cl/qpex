# LISS-0265: ADR — selective import / use ergonomics

## Metadata

- Local issue ID: LISS-0265
- GitHub issue: https://github.com/nn0cl/staqex/issues/275
- Status: **complete** — ADR 0177 **Accepted** (2026-08-02「承認」); Kernel Red LISS-0271
- ADR: [0177-import-use-ergonomics.md](../architecture/adr/0177-import-use-ergonomics.md)
- Type: Architecture Path (ADR)
- Priority: P1
- Program: [WP-0088](../work-plans/WP-0088-surface-modernization.md)
- Related: ADR 0054 modules; FQN noise (L-03/L-04)

## Intent

Reduce `Disaster.Domain.CommandBoard` / long import lists without deleting
modules.

Candidates:

- selective import: `import pkg.{A, B}`
- re-export / prelude for experiment profile
- `use Enum.*` inside `when` arms only
- shorter relative imports for same package tree

## Exit

- [x] ADR **Proposed**: [`docs/architecture/adr/0177-import-use-ergonomics.md`](../architecture/adr/0177-import-use-ergonomics.md)
- [ ] Compatibility: old imports remain valid
- [x] Accept recorded
- [x] Kernel Red: LISS-0271

## Non-goals

- Global namespace flatten that breaks multi-package demos
