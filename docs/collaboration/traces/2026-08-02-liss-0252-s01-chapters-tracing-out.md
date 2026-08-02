# AI work trace — LISS-0252 S01 chapters tracing_out

| Field | Value |
|---|---|
| Date | 2026-08-02 |
| Branch | `feature/liss-0250-measure-tracing-out` |
| Issue | LISS-0252 |
| Approval | Adjudicator「続けて」 |

## Change

Migrated ritual leftover discharge → `tracing_out` on:

- `main_day2_recovery.sqx`, `main_morning_collect.sqx`
- `main_route_interference.sqx`, `main_lattice_four.sqx`
- `main_tri_register.sqx`, `main_burst_spectrum.sqx`
- `main_fidelity_inner_check.sqx`

Prep ket `|0>` binds retained. fuel / comms already clean.

## Verification

All `main_*.sqx` `--seed 0` green; no LINEAR hard diagnostics.
