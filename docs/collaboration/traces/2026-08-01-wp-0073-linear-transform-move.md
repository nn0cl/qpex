# Trace: WP-0073 Wave 1 — type-driven linear Call move

| Field | Value |
|---|---|
| Date | 2026-08-01 |
| Program | WP-0073 |
| Issues | LISS-0221, LISS-0202 (residual) |
| Branch | `batch/wp-0073-linear-transform-move` |
| Contract touch | `docs/collaboration/local-issue-planning.md`, reviews/ |

## Reason

Adjudicator selected Wave 1 («1») after S01 residuals closed: implement
LISS-0221 and finish LISS-0202. ADR 0168 records the type-driven move rule.
Batch record bounds Kernel HIR linear verifier + named residual suites.

## Post-execution

Green on LISS-0221 Red + density/Lindblad residual + slice_b. Suite floor
**207 pass / 25 fail** (better than 193/32 intake floor). Batch moved to
`awaiting_post_review`.
