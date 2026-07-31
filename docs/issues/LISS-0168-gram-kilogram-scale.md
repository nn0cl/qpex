# LISS-0168: Mass `g` ↔ `kg`

## Metadata

- Local issue ID: LISS-0168
- Status: **complete**
- ADR: [0136](../architecture/adr/0136-gram-kilogram-scale.md)
- Program: [WP-0042](../work-plans/WP-0042-fahrenheit-gram.md)
- Tests: `tests/test_gram_kilogram_scale_red.py`

## Exit

- [x] `1000.0.g to kg` → 1.0; bare `.g` stays raw
- [x] `1.0.kg to g` → 1000.0
