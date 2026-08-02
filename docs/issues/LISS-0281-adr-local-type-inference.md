# LISS-0281: ADR — local type inference (classical + safe state)

## Metadata

- Local issue ID: LISS-0281
- GitHub issue: _(none yet)_
- Status: **proposed** (ADR 0180 draft filed 2026-08-03)
- Phase: Architecture Path (ADR draft → Accept)
- Type: Architecture ADR
- Priority: P2 (modern notebook face)
- Program: [WP-0089](../work-plans/WP-0089-surface-adoption-and-sugar.md)
- Depends: [LISS-0274](LISS-0274-wp-0089-program-lock.md)
- Blocks: [LISS-0282](LISS-0282-kernel-local-type-inference.md)
- Proposed ADR: `docs/architecture/adr/0180-local-type-inference.md` (number
  final at draft time if 0180 taken)

## Summary

Architecture decision for **local** type inference so teaching samples may write
`J = 1.0`, `H = -J * (Z[0]*Z[1])`, `s0 = |+>` without mandatory `Float` /
`Operator` / `state` noise — without weakening Classical vs State discipline.

## Decision questions (ADR must answer)

1. Which bindings infer? (literals, pure classical expr, ket literals, evolve RHS)
2. When is annotation still required? (ambiguous Joint width, overload, public API)
3. Fail-closed rules when Classical vs State could both fit
4. Interaction with Type-First dims (`12.0.km` already carries unit)
5. Explicit non-goals: no global Hindley-Milner redesign; no silent measure

## Exit

- [ ] ADR drafted under `docs/architecture/adr/`
- [ ] Adjudicator **Accept** or amend
- [ ] Kernel child LISS-0282 unblocked only after Accept

## Non-goals

- Implementation in this Issue
- Restoring classical `if` via “inferred control”

## Policy guard

- ADR 0095: inference must not force ugly chalk; it removes annotation ceremony
- Axioms 1–5 unchanged
