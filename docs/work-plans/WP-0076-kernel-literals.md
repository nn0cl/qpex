# WP-0076: Kernel literals single definition (LISS-0210)

| Field | Value |
|---|---|
| Status | **complete** (2026-08-01) |
| Branch | `batch/wp-0076-kernel-literals` |
| Batch | [execution-batch-wp-0076.json](../collaboration/reviews/execution-batch-wp-0076.json) |
| Parent | WP-0069; Adjudicator top-down after WP-0075 |

## Locked ruling

Shared vocabularies live in a **new leaf** module
`compiler/staqex/kernel_literals.py` (frozensets only; no imports of
typecheck / runtime / backend). Consumers import from it.

## Issues

| ID | Status |
|---|---|
| LISS-0210 | **complete** |

## Verification

- Identity: all consumers share the same frozenset objects from
  `kernel_literals`
- Full `tests/`: **996 passed / 65 failed** (unchanged floor vs pre-change)

