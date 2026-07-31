# WP-0069 — bounded execution batch proposal (BATCH-0001)

| Field | Value |
|---|---|
| Date | 2026-08-01 |
| Work plan | [WP-0069](../../work-plans/WP-0069-operations-review-intake.md) |
| Requested approval type | **investigation approval**, then **batch approval** |
| Current phase | investigation (documents only) |
| Implementation permission | **none** |

## Why this is a Markdown proposal and not a `.json` record

`scripts/check-execution-batch-reviews.py` validates every
`docs/collaboration/reviews/execution-batch-*.json` on every CI run. It requires
`approval_commit` to be a real 40-character SHA that is an ancestor of `HEAD`,
and it accepts only the statuses `approved_for_execution`, `in_progress`,
`awaiting_post_review`, `post_reviewed`, `rejected`, `expired` — there is no
draft state.

A proposed record therefore cannot exist as a `.json` file without either
fabricating an approval commit or mislabelling its status. Only the Adjudicator
may set `approved_for_execution` (`CLAUDE.md` §Approval Model), so this file
carries the proposed record as text. On approval, paste the JSON below to
`docs/collaboration/reviews/execution-batch-BATCH-0001.json` with
`approval_commit` set to the approving commit.

This also matches existing practice: the three records already in this
directory are Markdown, and no `execution-batch-*.json` has ever existed in the
repository.

## Scope proposed for BATCH-0001

The five **documentation-only** Issues from the independent track. They have no
phase gates, no code, and no cross-dependencies:

| Issue | Topic |
|---|---|
| [LISS-0212](../../issues/LISS-0212-dangling-liss-0070-reference.md) | dangling `LISS-0070` reference |
| [LISS-0213](../../issues/LISS-0213-proposed-adrs-with-shipped-issues.md) | Proposed ADRs with shipped Issues |
| [LISS-0214](../../issues/LISS-0214-broken-documented-commands-and-names.md) | broken documented commands and names |
| [LISS-0215](../../issues/LISS-0215-settled-decisions-documented-as-open.md) | settled decisions documented as open |
| [LISS-0216](../../issues/LISS-0216-issue-planning-doc-drift.md) | Issue-planning document drift |

## Deliberately excluded from this batch

- **LISS-0211** (`schema_version` contradiction) — edits `CLAUDE.md`, an agent
  operating contract. ADR 0006 / ADR 0112 require Adjudicator review, a stated
  reason, and a trace; that is not batch material even though the diff is one
  line. It is first in the work plan's order and needs its own approval.
- **LISS-0208** (test harness) — contains an unresolved technology selection
  (adopt `pytest` or rewrite five suites). Technology selection is a distinct
  approval type.
- **LISS-0202…LISS-0207** — each carries an unresolved semantic ruling
  ("is the test stale or is the Kernel wrong"). A batch grant would let those
  rulings be made unilaterally, which `CLAUDE.md` §Hard stop forbids.
- **LISS-0199 / 0200 / 0201 / 0209 / 0210** — code changes with ordering
  constraints against the regression work.
- **LISS-0217 / 0218 / 0219** — Architecture Path; blocked on ADR 0165 / 0166
  acceptance.

## Proposed record

```json
{
  "schema_version": 1,
  "batch_id": "BATCH-0001",
  "work_plan_id": "WP-0069",
  "status": "approved_for_execution",
  "approval_type": "bounded-batch",
  "approved_by": "Adjudicator",
  "approved_at": "<set at approval>",
  "expires_at": "<set at approval; must be after approved_at>",
  "execution_branch": "batch/BATCH-0001",
  "approval_commit": "<40-character SHA of the approving commit>",
  "issue_ids": [
    "LISS-0212",
    "LISS-0213",
    "LISS-0214",
    "LISS-0215",
    "LISS-0216"
  ],
  "approved_scope": "Documentation-accuracy repairs only: dangling Issue reference, Proposed-ADR status gap, broken documented commands and names, settled decisions shown as open, Issue-planning document drift. No Kernel change, no test change, no status promotion for unrelated Issues.",
  "allowed_paths": [
    "docs/architecture/README.md",
    "docs/architecture/open-work-register.md",
    "docs/architecture/physicist-source-friction-ledger.md",
    "docs/architecture/adr/*.md",
    "docs/collaboration/local-issue-planning.md",
    "docs/collaboration/traces/*.md",
    "docs/issues/*.md",
    "docs/issues/inbox/*.md",
    "docs/specs/staqex-examples-catalog-v2.md",
    "docs/specs/staqex-v1-conformance-plan.md",
    "docs/specs/staqex-v1-conformance-scenario-catalog.md",
    "docs/specs/staqex-v1-cst-formatter-plan.md",
    "docs/specs/staqex-v1-migration-matrix.md",
    "docs/work-plans/WP-0069-operations-review-intake.md",
    "examples/README.md",
    "examples/showcase/quantum_matter_discovery/README.md",
    "compiler/README.md"
  ],
  "allowed_phases": ["docs-only", "process-only"],
  "allowed_operations": ["edit-documentation"],
  "invalidating_triggers": [
    "new subsystem",
    "new language, framework, or datastore",
    "architecture or deployment boundary change",
    "authentication or authorization boundary change",
    "data concurrency or transaction boundary change",
    "any change under compiler/ other than compiler/README.md",
    "any change under tests/",
    "any edit to CLAUDE.md, AGENTS.md, .github/copilot-instructions.md, .grok/rules/, or .cursor/rules/"
  ],
  "post_review_required": true,
  "post_reviewed_by": null,
  "post_reviewed_at": null,
  "post_review_notes": null
}
```

## Notes on the proposed fields

- `schema_version` is **1**, not the `2` that `CLAUDE.md` §Claude Code
  Issue-Level and Work-Plan Autonomy specifies. A record with `2` fails
  `scripts/check-execution-batch-reviews.py` today. The contradiction itself is
  [LISS-0211](../../issues/LISS-0211-batch-record-schema-version-contradiction.md);
  until it is resolved, `1` is the only value that passes CI.
- `work_plan_id` is set because `CLAUDE.md` requires it of Claude Code, even
  though the shared schema treats it as optional.
- `compiler/README.md` is in `allowed_paths` because LISS-0214 fixes a broken
  command there. The `invalidating_triggers` entry immediately below it makes
  any other `compiler/` change invalidate the batch.
- The batch base at proposal time is `15c7ef09feff9d40ed9c22566de6d543cdc951f6`
  (`feat(wp-0066): classical Fraction + CredentialPort`). Recorded for reference
  only — the real `approval_commit` is the approving commit.

## What approval of this proposal does and does not grant

Grants: execution of the five named Issues, on `batch/BATCH-0001`, within the
listed paths, at `docs-only` / `process-only` phases, with post-review required.

Does not grant: any other Issue in WP-0069; acceptance of ADR 0165 or 0165; any
phase, architecture, or technology-selection approval; permission to promote an
Issue status outside the five named. CI success is not Adjudicator approval.
