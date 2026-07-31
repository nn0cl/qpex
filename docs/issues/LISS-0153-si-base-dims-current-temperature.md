# LISS-0153: SI base dims Current and Temperature

## Metadata

- Local issue ID: LISS-0153
- Status: **complete** — 2026-07-31
- Depends on: [ADR 0121](../architecture/adr/0121-si-base-dims-current-temperature.md)
- Program: [WP-0037](../work-plans/WP-0037-permanent-out-reopen.md)
- Tests: `tests/test_si_base_dims_current_temperature_red.py`

## Summary

Extend `Dim` to $(L,M,T,I,\Theta)$ with Type-First `Current` / `Temperature`
and unit suffixes `.A` / `.K`. No SI scale conversion.

## Exit

- [x] Red/Green: Current/Temperature typecheck + unit literals
- [x] Existing Length/Mass/Time programs remain compatible
