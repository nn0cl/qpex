# LISS-0182: US/UK ton mass scales

## Metadata

- Local issue ID: LISS-0182
- Status: **complete**
- ADR: [0150](../architecture/adr/0150-us-uk-ton-mass.md)
- Program: [WP-0056](../work-plans/WP-0056-us-uk-ton-mass.md)
- Tests: `tests/test_us_uk_ton_mass_red.py`

## Exit

- [x] `.ton_us` / `.ton_uk` in UNIT_TABLE / scale table
- [x] `1.0.ton_us to lb` = 2000; to kg via 2000 lb
- [x] `1.0.ton_uk to lb` = 2240; bridge to `.t` / `.ton_us`
- [x] Metric `.t` regression still green
