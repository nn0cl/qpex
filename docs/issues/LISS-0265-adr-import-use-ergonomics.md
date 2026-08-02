# LISS-0265: ADR — selective import / use ergonomics

## Metadata

- Local issue ID: LISS-0265
- GitHub issue: https://github.com/nn0cl/staqex/issues/275
- Status: **open** — ADR **drafting authorized** (承認・起票); Accept still separate
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

- [ ] ADR **Proposed** with grammar sketch + examples
- [ ] Compatibility: old imports remain valid
- [ ] Accept / reject recorded
- [ ] Kernel follow-up via LISS-0269 if Accepted

## Non-goals

- Global namespace flatten that breaks multi-package demos
