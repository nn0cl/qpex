# LISS-0186: Mixed-unit arithmetic reject

## Metadata

- Local issue ID: LISS-0186
- Status: **complete**
- ADR: [0154](../architecture/adr/0154-mixed-unit-reject.md)
- Program: [WP-0060](../work-plans/WP-0060-mixed-unit-reject.md)
- Tests: `tests/test_mixed_unit_reject_red.py`

## Exit

- [x] `1.kg + 1.g` → `UNIT_MIXED_ARITHMETIC_ERROR`
- [x] Same-unit `+` ok; explicit `to` then same-unit ok
- [x] Type-First mixed vars rejected
- [x] No automatic rescale
