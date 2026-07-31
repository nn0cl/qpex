# LISS-0166: Affine °C ↔ K

## Metadata

- Local issue ID: LISS-0166
- Status: **complete**
- ADR: [0134](../architecture/adr/0134-celsius-kelvin-affine.md)
- Program: [WP-0041](../work-plans/WP-0041-pipe-hole-celsius.md)
- Tests: `tests/test_celsius_kelvin_affine_red.py`

## Exit

- [x] `0.0.C to K` → 273.15; bare `.C` stays raw
- [x] `273.15.K to C` → 0.0
