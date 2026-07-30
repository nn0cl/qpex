# Bounded Execution Batch Review Record

Use one machine-readable JSON record under
`docs/collaboration/reviews/execution-batch-<id>.json` when the Adjudicator
pre-approves a named set of low-risk Issues for execution.

The record is an execution boundary, not a blanket approval. It must name the
Issue IDs, allowed paths, allowed phases and operations, expiry, invalidating
architecture triggers, and post-review requirement.

`work_plan_id` is an **optional** field naming the governing
`docs/work-plans/WP-*.md`. Records that omit it remain valid for every agent,
and `schema_version` stays `1`. It is validated only when present, so a
malformed or dangling work-plan reference still fails CI. Claude Code is
required to set it for work-plan batches by `CLAUDE.md` §Claude Code
Issue-Level and Work-Plan Autonomy (ADR 0113); that obligation is Claude-only
and is not imposed here.

`issue_ids` stays enumerated for every agent — a work plan may hold dozens of
Issues (the largest currently holds 56), so a record names the subset being
authorized rather than granting a whole plan. Completing a named Issue does not
authorize an Issue the record omits.

Required JSON shape:

```json
{
  "schema_version": 1,
  "batch_id": "BATCH-0001",
  "work_plan_id": "WP-0001",
  "status": "approved_for_execution",
  "approval_type": "bounded-batch",
  "approved_by": "Adjudicator",
  "approved_at": "2026-07-18T00:00:00Z",
  "expires_at": "2026-07-25T00:00:00Z",
  "execution_branch": "batch/BATCH-0001",
  "approval_commit": "<40-character git commit SHA>",
  "issue_ids": ["LISS-0001"],
  "approved_scope": "Named low-risk documentation work only",
  "allowed_paths": ["docs/collaboration/**"],
  "allowed_phases": ["docs-only", "process-only"],
  "allowed_operations": ["edit-documentation"],
  "invalidating_triggers": [
    "new subsystem",
    "new language, framework, or datastore",
    "architecture or deployment boundary change",
    "authentication or authorization boundary change",
    "data concurrency or transaction boundary change"
  ],
  "post_review_required": true,
  "post_reviewed_by": null,
  "post_reviewed_at": null,
  "post_review_notes": null
}
```

The agent may move the record to `awaiting_post_review` after execution. Only
the Adjudicator may move it to `post_reviewed`. CI validates the record but does
not manufacture human approval. When the current branch matches
`execution_branch`, CI checks the changed paths from `approval_commit` to the
current commit against `allowed_paths`. A batch branch must use the
`batch/<batch-id>` naming convention.
