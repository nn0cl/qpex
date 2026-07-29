# AI Work Trace

## Request

- Date: 2026-07-25
- User request: Reduce PR-merge frequency by making branch creation and
  merging happen at local-Issue granularity instead of per incremental step;
  and require that any such policy change be operated through the actual
  branch-strategy document, not left as informal session memory only.
- Current phase: process contract update (branch/PR discipline)
- Canonical issue or work plan: Process change; no LISS created (applies to
  `docs/collaboration/branch-commit-pr-discipline.md` directly)
- AI planning record: Current conversation design intake

## Context Ledger

- Included: `docs/collaboration/branch-commit-pr-discipline.md`,
  `docs/collaboration/prompt-instruction-change-control.md`, this session's
  LISS-0048/LISS-0049 branch/PR history (PR #10, #11, #12) as the concrete
  trigger example.
- Omitted: application source, tests, unrelated ADRs and specs.
- Assumptions: this document is not literally mirrored into
  `AGENTS.md`/`CLAUDE.md`/Copilot/Grok/Cursor contract files (they only
  link to it), so no cross-file mirror edit is required; the change does
  not touch shared phase, dependency, or read-order rules.
- Open decisions: none remaining after Adjudicator wording approval in
  chat; PR itself still needs Adjudicator merge decision.

## Routing

- Model/assistant/tool: Claude Code, direct file inspection and patching
- Reason: Cross-agent process contract change (branch/PR discipline applies
  to every agent listed in `AGENTS.md`)
- Privacy constraints: No private data, secrets, or provider data used

## AI Execution Records

### Attempt 1

- Agent: Claude (Sonnet 5)
- Environment: Local Staqex repository
- Model as displayed: claude-sonnet-5
- Reasoning setting as displayed: unavailable
- Estimated token range: not recorded
- Estimated token midpoint: not recorded
- Actual tokens: unavailable
- Token metric: unavailable
- Token source: unavailable
- Token attribution boundary: this task only
- Actual token unavailable reason: runtime does not expose the metric
- Estimate variance: unavailable
- Variance reason: unavailable
- Scope: Added a new "Branch and PR Granularity" section to
  `branch-commit-pr-discipline.md` stating one branch/PR per Issue as the
  default, with three explicit exceptions.
- Result: Adjudicator reviewed and approved the exact proposed wording in
  chat before the edit was made.
- Attempt boundary: No application code or tests changed
- Notes: Exact wording was presented to the Adjudicator for approval before
  editing, per the Approval Model (process/architecture decision, not
  self-authorized).

## Cost / Reasoning Control

- Operating path: process contract change (same rigor as Architecture Path)
- Files read: `docs/collaboration/branch-commit-pr-discipline.md`,
  `docs/collaboration/prompt-instruction-change-control.md`,
  `docs/templates/ai-work-trace.md`, prior trace
  `2026-07-25-explicit-batch-approval-contract.md` for house style
- Context intentionally omitted: application implementation and unrelated
  specs
- Deterministic checks used: `git diff` review of the single changed section
- Escalation reason: Agent operating contract change requires Adjudicator
  review and a trace per `prompt-instruction-change-control.md`
- Avoided LLM work: No external model or provider routing
- Rework caused by AI output: None — this trace itself is the corrective
  action after the Adjudicator flagged that the earlier chat-only policy
  note was not sufficient

## Adjudicator Decisions

- Adjudicator approved the exact proposed section text and insertion point
  (after "Branches", before "Continuous Integration Gate") in chat before
  the edit was made.
- Adjudicator has not yet reviewed/merged the resulting PR; that review is
  separate from the wording approval above per the Approval Model.

## Verification

- Commands/checks: `git diff` (single section added, no other content
  changed); confirmed the file remains valid Markdown and does not
  contradict the existing "Stacked Branches for Phase Splitting" section
  (the new section explicitly defers to it for the phase-separated-PR
  exception).
- Result: Documentation-only change; no test suite applicable.

## Changed Files

- `docs/collaboration/branch-commit-pr-discipline.md`
- `docs/collaboration/traces/2026-07-25-issue-level-branch-granularity.md`

## Next Safe Action

- Adjudicator reviews and merges this process-contract PR (or requests
  wording changes). Do not merge based only on automated CI, per
  `prompt-instruction-change-control.md`.
- Once merged, apply this granularity default to remaining LISS-0049 work
  (Phase 2 Green onward): one Issue-scoped branch/PR rather than one per
  phase, still pausing for explicit phase approval between commits.

## Notes

- This trace's own existence is the concrete fix for the gap the Adjudicator
  identified: a workflow-behavior change must be recorded in the actual
  contract document with a trace, not just asserted in chat/session memory.
