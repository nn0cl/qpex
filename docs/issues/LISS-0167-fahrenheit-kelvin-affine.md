# LISS-0167: Affine °F ↔ K

## Metadata

- Local issue ID: LISS-0167
- Status: **complete**
- ADR: [0135](../architecture/adr/0135-fahrenheit-kelvin-affine.md)
- Program: [WP-0042](../work-plans/WP-0042-fahrenheit-gram.md)
- Tests: `tests/test_fahrenheit_kelvin_affine_red.py`

## Exit

- [x] `32.0.F to K` → 273.15; bare `.F` stays raw
- [x] `32.0.F to C` → 0.0
