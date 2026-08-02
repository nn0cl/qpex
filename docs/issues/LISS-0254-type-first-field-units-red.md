# LISS-0254: Kernel Type-First field unit retention — Red (ADR 0174)

## Metadata

- Local issue ID: LISS-0254
- Status: **open** (awaiting Plan / Phase 1 Red approval)
- Type: Feature Path
- Priority: P1
- Planning size: M
- Design ADR: [0174](../architecture/adr/0174-type-first-field-units.md)
  (**Accepted**)
- Depends on: [LISS-0253](LISS-0253-adr-0174-type-first-field-units.md) (**complete**)
- Branch: `feature/liss-0254-type-first-field-units` (create after Phase approval)
- Approval: architecture Accept only so far — **no Phase 1 yet**

## Intent

Ship ADR 0174 in the Shipping Kernel:

1. Dimful Classical fields on `class` / `struct` retain unit-suffix evidence
   (same contract as ADR 0155 locals).
2. Field write stores magnitude + unit; field read restores unit for
   `expr to unit` and mixed `+`/`-` promote.
3. Acceptance: `this.m to g` after `Mass` field init succeeds; Float fields
   still do not invent SI units.
4. Tests assert fail-closed when source unit is unknown / incompatible.

## Exit

- [ ] Phase 1 Red: failing tests only
- [ ] Phase 2 Green: minimal implementation; no test edits to force pass
- [ ] Phase 3 Refactor + reviewer empathy
- [ ] Follow-on sample heal (S01 `quantities.sqx`) — may split

## Non-goals

- Meter-class OOP unit hierarchies (ADR 0037)
- Auto-unit for bare Float stock fields
- QPU classical packing of units
- Failure glossary ADR
- Lifting dialect D5 before sample heal

## Notes

Do not start Red until the Adjudicator names Phase 1 (or Plan approval).
ADR Accept alone is not implementation authorization.
