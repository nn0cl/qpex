# LISS-0254: Kernel Type-First field unit retention — Red (ADR 0174)

## Metadata

- Local issue ID: LISS-0254
- Status: **in progress** — Phase 1 Red complete (awaiting Phase 2 Green)
- Phase: phase-1-red
- Type: Feature Path
- Priority: P1
- Planning size: M
- Design ADR: [0174](../architecture/adr/0174-type-first-field-units.md)
  (**Accepted**)
- Depends on: [LISS-0253](LISS-0253-adr-0174-type-first-field-units.md) (**complete**)
- Branch: `feature/liss-0254-type-first-field-units`
- Approval: Adjudicator「承認」(2026-08-02) — Phase 1 Red

## Intent

Ship ADR 0174 in the Shipping Kernel:

1. Dimful Classical fields on `class` / `struct` retain unit-suffix evidence
   (same contract as ADR 0155 locals).
2. Field write stores magnitude + unit; field read restores unit for
   `expr to unit` and mixed `+`/`-` promote.
3. Acceptance: `this.stock to g` after `Mass` field init succeeds; Float fields
   still do not invent SI units.
4. Tests assert fail-closed when source unit is unknown / incompatible.

## Exit

- [x] Phase 1 Red: failing tests only —
  `tests/test_liss0254_type_first_field_units_red.py` (3 failed / 1 passed
  fail-closed guard; expected Red)
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

Red evidence (`.venv/bin/pytest tests/test_liss0254_type_first_field_units_red.py -q`):
class `to g` TYPE_MISMATCH (unknown source unit); mixed field `+` yields raw
501 not 1.5 kg; struct field `to g` DIMENSION_MISMATCH; Float→kg still
fail-closed.
