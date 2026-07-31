# LISS-0178: Imperial ounce mass `oz`

## Metadata

- Local issue ID: LISS-0178
- Status: **complete**
- ADR: [0146](../architecture/adr/0146-imperial-ounce-mass.md)
- Program: [WP-0052](../work-plans/WP-0052-imperial-ounce-mass.md)
- Tests: `tests/test_imperial_ounce_mass_red.py`

## Exit

- [x] `.oz` in UNIT_TABLE / scale table
- [x] `16.0.oz to lb` = 1; `16.0.oz to kg` = 0.45359237
- [x] `1.0.lb to oz` = 16
