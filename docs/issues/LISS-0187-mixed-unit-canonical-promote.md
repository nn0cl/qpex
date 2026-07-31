# LISS-0187: Mixed-unit canonical promote

## Metadata

- Local issue ID: LISS-0187
- Status: **complete**
- ADR: [0155](../architecture/adr/0155-mixed-unit-canonical-promote.md)
- Program: [WP-0061](../work-plans/WP-0061-mixed-unit-canonical-promote.md)
- Tests: `tests/test_mixed_unit_canonical_promote_red.py`
- Supersedes: LISS-0186 reject-only behavior

## Exit

- [x] `1.kg + 1.g` → 1.001 kg (no reject)
- [x] Type-First mixed vars promote
- [x] Affine °C+°F → K
- [x] Same-unit and explicit `to` regressions green
