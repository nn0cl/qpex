# LISS-0267: ADR — pure classical Call as expression operand

## Metadata

- Local issue ID: LISS-0267
- GitHub issue: https://github.com/nn0cl/staqex/issues/277
- Status: **complete** — ADR 0179 **Accepted** (2026-08-02「承認」); Kernel Red LISS-0273
- ADR: [0179-classical-call-in-expr.md](../architecture/adr/0179-classical-call-in-expr.md)
- Type: Architecture Path (ADR)
- Priority: P1
- Program: [WP-0088](../work-plans/WP-0088-surface-modernization.md)
- Evidence: S01 LISS-0256 note — `f() * 0.2` fails; must bind first

## Intent

Align classical expression rules with modern languages: **pure classical**
method/function results may appear in classical arithmetic without mandatory
temps, when the callee is known classical (Float/Int/Bool/unit quantity heads
as applicable).

**Must not** weaken LINEAR or allow State-forming calls to collapse early.

## Exit

- [x] ADR **Proposed**: [`docs/architecture/adr/0179-classical-call-in-expr.md`](../architecture/adr/0179-classical-call-in-expr.md)
- [ ] Invalid cases listed (State/Joint returning calls)
- [ ] Accept / reject
- [x] Kernel Red: LISS-0273

## Non-goals

- Allowing classical `if`
- Changing Joint pushforward of `+` on State
