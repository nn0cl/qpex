# AI work trace — LISS-0270 experiment surface profile

| Field | Value |
|---|---|
| Date | 2026-08-02 |
| ADR | 0176 Accepted |
| Issue | LISS-0270 / #283 |

## Change

- Detect `// staqex-profile: experiment`
- Default package `staqex.experiment` when omitted
- Bare top-level statements desugar to synthetic `main`
- B08 converted to short experiment face

## Verification

- `pytest tests/test_liss_0270_experiment_surface_profile_red.py` — 3 passed
- `run` B08 seed 0 OK
