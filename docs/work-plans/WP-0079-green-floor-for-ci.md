# WP-0079: Green test floor for LISS-0209 CI

| Field | Value |
|---|---|
| Status | **complete** (awaiting PR merge) |
| Branch | `batch/wp-0079-green-floor-for-ci` |
| Batch | [execution-batch-wp-0079.json](../collaboration/reviews/execution-batch-wp-0079.json) |
| Parent | After WP-0078; Adjudicator option 1 for LISS-0209 |

## Locked rulings

- **LISS-0209 blocking CI stays deferred** until `pytest tests/` is **0 fail**.
- This batch: **suite-first** green-up (measure / uncompute / explicit `return`).
- Kernel changes: stop and ask; do not invent behavior.
- Spec-verification / advisory CI: out of this batch.

## Issues

| ID | Status |
|---|---|
| LISS-0233 | **complete** (residual suite green floor) |
| LISS-0209 | unblocked for WP-0080 (blocking CI) |

## Baseline → exit

| When | Result |
|---|---|
| 2026-08-02 start (`main` @ `53b3222`) | 996 passed / **65 failed** |
| 2026-08-02 exit | **1062 passed / 0 failed** |

## Kernel delta (narrow)

`compiler/staqex/parser.py`: bare-block `{ let … }` detection uses
`TokenKind.LET` (ADR 0153), restoring BlockExpr after the WP-0075 anticommutator
guard mistakenly required `IDENT` `"let"`.

## Follow-on

WP-0080 / LISS-0209 — enable blocking `pytest tests/` in CI.
