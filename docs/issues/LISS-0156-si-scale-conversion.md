# LISS-0156: Explicit SI scale `to`

## Metadata

- Local issue ID: LISS-0156
- Status: **complete**
- ADR: [0124](../architecture/adr/0124-si-scale-conversion-explicit.md)
- Program: [WP-0038](../work-plans/WP-0038-partial-si-scale-design.md)
- Tests: `tests/test_si_scale_conversion_red.py`

## Exit

- [x] `5.0.ms to s` converts magnitude; bare `.ms` stays raw
- [x] Dim mismatch / unknown pair diagnosed
