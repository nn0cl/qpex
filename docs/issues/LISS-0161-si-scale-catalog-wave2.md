# LISS-0161: SI scale catalog wave-2

## Metadata

- Local issue ID: LISS-0161
- Status: **complete**
- ADR: [0129](../architecture/adr/0129-si-scale-catalog-wave2.md)
- Program: [WP-0039](../work-plans/WP-0039-si-catalog-ketlit-fn-args.md)
- Tests: `tests/test_si_scale_catalog_wave2_red.py`

## Exit

- [x] `ps`/`us`/`km`/`kHz`/`MHz` convert via `to`; bare suffixes stay raw
- [x] `eV` still not silently converted
