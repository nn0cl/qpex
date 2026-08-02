# AI work trace — WP-0086 spec-verification CI

| Field | Value |
|---|---|
| Date | 2026-08-02 |
| Branch | `batch/wp-0086-spec-verification-ci` |
| Issues | LISS-0240, LISS-0241, LISS-0242 |

## Change

- Parser: disable ADR 0124 unit-convert inside `measure`/`snapshot` so
  ADR 0029 `to <sink>` wins.
- B05 example: drop premature vacuum that emptied the interfered joint.
- CI: blocking `spec-verification` job (`run_all.py`, no report commit).
- open-work-register + testing-strategy health/docs sync.

## Verification

- `pytest tests/` → 1087 passed
- `python3 tests/spec_verification/run_all.py` → 161/161
