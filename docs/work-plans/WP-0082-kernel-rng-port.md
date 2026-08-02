# WP-0082: Kernel `RngPort` (LISS-0235 / ADR 0170)

| Field | Value |
|---|---|
| Status | **complete** (awaiting post-review) |
| Branch | `batch/wp-0082-kernel-rng-port` |
| Batch | [execution-batch-wp-0082.json](../collaboration/reviews/execution-batch-wp-0082.json) |
| Parent | Adjudicator「はい」after WP-0081 post-review |

## Locked rulings

- ADR 0170 Accepted; this batch executes **LISS-0235 only**.
- Bit-identical seeded outputs; `HostRngPort` stays separate.
- No MeasureSink / SourcePort.

## Issues

| ID | Status |
|---|---|
| LISS-0235 | **complete** |

## Verification

`.venv/bin/pytest tests/` → 1073 passed / 0 failed.
