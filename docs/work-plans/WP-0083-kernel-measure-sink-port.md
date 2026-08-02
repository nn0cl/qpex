# WP-0083: Kernel `MeasureSinkPort` (LISS-0236 / ADR 0171)

| Field | Value |
|---|---|
| Status | **complete** (post-reviewed) |
| Branch | `batch/wp-0083-kernel-measure-sink-port` |
| Batch | [execution-batch-wp-0083.json](../collaboration/reviews/execution-batch-wp-0083.json) |
| Parent | Adjudicator「はい」after WP-0082 post-review |

## Locked rulings

- ADR 0171 Accepted; this batch executes **LISS-0236 only**.
- Bit-identical seeded stdout; Host JobResult unchanged.
- No SourcePort.

## Issues

| ID | Status |
|---|---|
| LISS-0236 | **complete** |

## Verification

`.venv/bin/pytest tests/` → 1078 passed / 0 failed.
