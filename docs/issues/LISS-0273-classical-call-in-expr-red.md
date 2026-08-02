# LISS-0273: Kernel Red — classical Call in expression (ADR 0179)

## Metadata

- Local issue ID: LISS-0273
- GitHub issue: https://github.com/nn0cl/staqex/issues/282
- Status: **open** — Phase 1 Red authorized (ADR 0179 Accepted)
- Type: Feature Path
- Priority: P1 (good first Kernel ship of Wave C — smallest surface)
- ADR: [0179](../architecture/adr/0179-classical-call-in-expr.md) (**Accepted**)
- Program: WP-0088
- Parent: LISS-0269

## Intent

Allow pure classical Calls/method results as operands in classical arithmetic
without mandatory temps. Reject State/Joint-forming Calls as classical operands.

## Exit

- [ ] Red failing on `f() * 0.2` classical pattern
- [ ] Green evaluator/typecheck
- [ ] Negative tests for State-forming misuse
- [ ] Refactor
