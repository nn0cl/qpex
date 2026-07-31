# LISS-0164: Exact SI `eV` ↔ `J`

## Metadata

- Local issue ID: LISS-0164
- Status: **complete**
- ADR: [0132](../architecture/adr/0132-ev-joule-si-conversion.md)
- Program: [WP-0040](../work-plans/WP-0040-stepwise-partial-ev.md)
- Tests: `tests/test_ev_joule_conversion_red.py`

## Exit

- [x] `1.0.eV to J` uses exact SI factor; bare `.eV` stays raw
- [x] `J to eV` reciprocal works
