# WP-0084: Kernel `SourcePort` (LISS-0237 / ADR 0172)

| Field | Value |
|---|---|
| Status | **complete** (post-reviewed) |
| Branch | `batch/wp-0084-kernel-source-port` |
| Batch | [execution-batch-wp-0084.json](../collaboration/reviews/execution-batch-wp-0084.json) |
| Parent | Adjudicator「はい」after WP-0083 post-review |

## Locked rulings

- ADR 0172 Accepted; this batch executes **LISS-0237 only**.
- `SourcePort` below `load_module_graph`; ADR 0054 logic unchanged.
- Bit-identical seeded CLI stdout.

## Issues

| ID | Status |
|---|---|
| LISS-0237 | **complete** |

## Verification

`.venv/bin/pytest tests/` → 1082 passed / 0 failed.
