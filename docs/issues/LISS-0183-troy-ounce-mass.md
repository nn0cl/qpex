# LISS-0183: Troy ounce mass `oz_t`

## Metadata

- Local issue ID: LISS-0183
- Status: **complete**
- ADR: [0151](../architecture/adr/0151-troy-ounce-mass.md)
- Program: [WP-0057](../work-plans/WP-0057-troy-ounce-mass.md)
- Tests: `tests/test_troy_ounce_mass_red.py`

## Exit

- [x] `.oz_t` in UNIT_TABLE / scale table
- [x] `1.0.oz_t to g` = 31.1034768; to kg exact
- [x] Bridge to avoirdupois `.oz` via kg canonical
