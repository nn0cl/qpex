# WP-0075: Regression clusters LISS-0204..0207

| Field | Value |
|---|---|
| Status | **complete** (2026-08-01) |
| Branch | `batch/wp-0075-regression-clusters-0204-0207` |
| Batch | [execution-batch-wp-0075.json](../collaboration/reviews/execution-batch-wp-0075.json) |
| Parent | WP-0069; Adjudicator top-down after WP-0074 |

## Locked rulings

- **0204**: ADR 0116 Type-First `Float` is Classical. Methods that return pure
  classical quantities declare `-> Float`, not `-> State<Float>`. Never Leave
  the State is preserved (these were never quantum carriers).
- **0205**: `{X, Y}` anticommutator sugar remains legal (parser restore).
- **0206**: Unknown target units hard-fail (`TYPE_MISMATCH`); suites must not
  use shipped `lb` as "unknown".
- **0207**: Fix root causes / suite drift per suite (adjoint domain; unused
  `coin` LINEAR; QASM foreach comment regex).

## Issues

| ID | Status |
|---|---|
| LISS-0204 | **complete** |
| LISS-0205 | **complete** |
| LISS-0206 | **complete** |
| LISS-0207 | **complete** |

## Verification

- Named suites for 0204–0207 + Dirac F/G: **60 passed**
- Full `tests/`: residual failures remain outside this batch (same LINEAR /
  suite-drift family as later backlog Issues); batch scope green

## Out

LISS-0209–0210, 0212–0219 (later in the same top-down sequence).
