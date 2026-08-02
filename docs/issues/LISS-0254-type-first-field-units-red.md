# LISS-0254: Kernel Type-First field unit retention — Red (ADR 0174)

## Metadata

- Local issue ID: LISS-0254
- Status: **complete** — Phase 3 Refactor 2026-08-02
- Phase: phase-3-refactor
- Type: Feature Path
- Priority: P1
- Planning size: M
- Design ADR: [0174](../architecture/adr/0174-type-first-field-units.md)
  (**Accepted**)
- Depends on: [LISS-0253](LISS-0253-adr-0174-type-first-field-units.md) (**complete**)
- Branch: `feature/liss-0254-type-first-field-units`
- Approval: Adjudicator「承認」Phase 1 Red, Phase 2 Green, Phase 3 Refactor
  (2026-08-02); sample heal「修復もして」

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

- [x] Phase 1 Red: `tests/test_liss0254_type_first_field_units_red.py`
- [x] Phase 2 Green: typecheck struct fields + canonical `to` for dimful heads;
  evaluator `field_units` on class/struct; init/method frame units; mixed `+`
  promote on field Attrs
- [x] Phase 3 Refactor + reviewer empathy
- [x] Sample heal: S01 `domain/quantities.sqx` + tonight spine ctor
  (`12.0.km` / `800.0.kg` / …); dialect D5 demotion lifted

## Non-goals

- Meter-class OOP unit hierarchies (ADR 0037)
- Auto-unit for bare Float stock fields
- QPU classical packing of units
- Failure glossary ADR

## Notes

Green evidence: `.venv/bin/pytest tests/test_liss0254_type_first_field_units_red.py
tests/test_mixed_unit_canonical_promote_red.py -q` → **9 passed**.

Heal evidence (2026-08-02):
`python3 -m compiler.staqex …/main_disaster_response.sqx --seed 0` → `0`.
`scale_tag` is a dimensionless Host mark (`1.0`) — unlike SI dims are not
summed into Float (pre-heal theater removed).

Phase 3: `_put_unit` / `_attr_host` readability helpers; typecheck import hoist.
Traces: `docs/collaboration/traces/2026-08-02-liss-0254-phase*.md` and
`…-s01-quantities-heal.md`.
