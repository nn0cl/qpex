# LISS-0271: Kernel Red — selective import / use (ADR 0177)

## Metadata

- Local issue ID: LISS-0271
- GitHub issue: https://github.com/nn0cl/staqex/issues/284
- Status: **open** — Phase 1 Red authorized (ADR 0177 Accepted)
- Type: Feature Path
- Priority: P1
- ADR: [0177](../architecture/adr/0177-import-use-ergonomics.md) (**Accepted**)
- Program: WP-0088
- Parent: LISS-0269

## Intent

Ship selective `import pkg.{A, B}` and narrow enum `use` for when-arm names.
Old imports remain valid.

## Exit

- [ ] Red → Green → Refactor
- [ ] Tests for selective import + use
- [ ] Non-goals: wildcard deep imports as required style
