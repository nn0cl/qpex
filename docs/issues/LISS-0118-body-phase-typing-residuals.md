# LISS-0118: Body-level phase typing residuals

## Metadata

- Local issue ID: LISS-0118
- Status: **proposed** — deferred residuals from LISS-0076
- Phase: Feature Path / plan intake gated
- Type: language feature / type system / scientific scopes
- Priority: P2
- Planning size: M
- Parent: [LISS-0076](LISS-0076-body-level-scientific-phase-typing.md) **complete**
- Related: [staqex-scientific-scopes.md](../specs/staqex-scientific-scopes.md)

## Claim notice

**Do not reuse `LISS-0115`–`LISS-0117` for this work.** Those IDs are claimed
by the Physics IR track. This Issue owns 0076 residuals only.

## Motivation

LISS-0076 A–E shipped Execution-symbol visibility for Theory/Experiment/Workflow
bodies, imports, and one-hop call/method taint. Deferred items remain as
explicit Non-goals in the scientific-scopes spec.

## In scope (proposed)

- Report-phase body visibility matrix
- Transitive helper taint (call graph deeper than one hop)
- Tighten unqualified method-name taint / short-name collision policy

## Out of scope

- Dynamic QPU (LISS-0077)
- Physics IR (LISS-0081 / LISS-0115–0117)
- ADR unless an irreversible taint policy must be locked first

## Adjudicator Decision Points

- [ ] Approve plan intake / slices for LISS-0118
- [ ] Confirm no ADR required (default: Issue + spec Non-goals sufficient)
