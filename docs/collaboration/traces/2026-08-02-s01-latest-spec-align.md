# AI work trace — S01 align to latest Kernel / ports / CI

| Field | Value |
|---|---|
| Date | 2026-08-02 |
| Branch | `fix/s01-latest-spec-align` |

## Change

- `main_tri_register.sqx`: `state (c,t) = cnot(c,t)` for linear discipline.
- Evaluator: multi-wire in-place `cnot` bind.
- README / scorecard / LISS-0222 / WP-0070 honesty sync (ports, CI, fidelity run).

## Verification

S01 mains seed 0 clean; pytest 1089; SV 161/161.
