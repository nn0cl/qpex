# LISS-0177: Imperial pound mass `lb` ↔ `kg`

## Metadata

- Local issue ID: LISS-0177
- Status: **complete**
- ADR: [0145](../architecture/adr/0145-imperial-pound-mass.md)
- Program: [WP-0051](../work-plans/WP-0051-imperial-pound-mass.md)
- Tests: `tests/test_imperial_pound_mass_red.py`

## Exit

- [x] `.lb` in UNIT_TABLE / scale table
- [x] `1.0.lb to kg` = 0.45359237
- [x] Round-trip via kg; `lb to g` consistent
