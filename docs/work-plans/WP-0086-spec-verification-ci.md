# WP-0086: Spec-verification CI + observe-sink `to` fix

| Field | Value |
|---|---|
| Status | **complete** (post-reviewed) |
| Branch | `batch/wp-0086-spec-verification-ci` |
| Batch | [execution-batch-wp-0086.json](../collaboration/reviews/execution-batch-wp-0086.json) |
| Parent | Adjudicator「上から順番に開始」→「続行して」after WP-0085 |

## Locked rulings

- Blocking CI job for `python3 tests/spec_verification/run_all.py`.
- Do **not** commit SV reports from CI.
- Fix ADR 0029 `to <sink>` vs ADR 0124 `to unit` conflict for measure/snapshot.
- Refresh stale open-work-register CI health text.

## Issues

| ID | Status |
|---|---|
| LISS-0240 | **complete** — observe sink `to` vs unit convert |
| LISS-0241 | **complete** — blocking SV CI job |
| LISS-0242 | **complete** — open-work-register health refresh |

## Verification

- `.venv/bin/pytest tests/` green
- `python3 tests/spec_verification/run_all.py` → 161/161
