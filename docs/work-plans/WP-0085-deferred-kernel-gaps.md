# WP-0085: WP-0079 deferred Kernel gaps

| Field | Value |
|---|---|
| Status | **complete** (awaiting post-review) |
| Branch | `batch/wp-0085-deferred-kernel-gaps` |
| Batch | [execution-batch-wp-0085.json](../collaboration/reviews/execution-batch-wp-0085.json) |
| Parent | Adjudicator「上から順番に開始」(post WP-0084) |

## Locked rulings

- Close the two Kernel gaps recorded on [LISS-0233](../issues/LISS-0233-green-floor-residual-suites.md).
- No new ADR: ADR 0149 + LISS-0112 Slice B already authorize the behaviors.
- No non-Identity D=3 apply; no Qudit&lt;4&gt; / QASM lift.

## Issues

| ID | Status |
|---|---|
| LISS-0238 | **complete** — multi-hole Partial pipe lhs move |
| LISS-0239 | **complete** — Qutrit `apply(I)` Identity SV no-op |

## Verification

`.venv/bin/pytest tests/` → 1084 passed / 0 failed.
