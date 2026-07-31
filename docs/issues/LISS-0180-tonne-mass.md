# LISS-0180: Metric tonne mass `t`

## Metadata

- Local issue ID: LISS-0180
- Status: **complete**
- ADR: [0148](../architecture/adr/0148-tonne-mass.md)
- Program: [WP-0054](../work-plans/WP-0054-tonne-mass.md)
- Tests: `tests/test_tonne_mass_red.py`

## Exit

- [x] `.t` in UNIT_TABLE / scale table
- [x] `1.0.t to kg` = 1000; `to g` = 1e6
- [x] `1000.0.kg to t` = 1
