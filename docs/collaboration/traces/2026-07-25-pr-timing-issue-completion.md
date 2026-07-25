# AI Work Trace

## Request

- Date: 2026-07-25
- User request: Clarify when a pull request should be opened relative to
  Issue work, following up on the same-day "Branch and PR Granularity"
  change (PR #13). Considered and rejected a draft-PR-at-Phase-1-Red
  proposal; settled on: create the branch at Issue start, open the PR only
  once the Issue's approved scope is complete and its documentation is
  synchronized, then request the Adjudicator's merge decision.
- Current phase: process contract update (branch/PR discipline)
- Canonical issue or work plan: Process change; no LISS created (applies to
  `docs/collaboration/branch-commit-pr-discipline.md` directly)
- AI planning record: Current conversation design intake

## Context Ledger

- Included: `docs/collaboration/branch-commit-pr-discipline.md` (as amended
  by PR #13 earlier the same day), `docs/collaboration/definition-of-done.md`
  (Issue Status Synchronization section), `docs/collaboration/
  prompt-instruction-change-control.md`, this session's LISS-0049 branch
  history (`feature/liss-0049-qasm-function-call-rejection`, PR #14) as the
  concrete precedent — a PR was opened after Phase 2 Green and kept
  receiving commits through Phase 3 before a single merge, which is the
  behavior this amendment now states explicitly.
- Omitted: application source, tests, unrelated ADRs and specs.
- Assumptions: `branch-commit-pr-discipline.md` is only linked from
  `AGENTS.md`/`CLAUDE.md`/Copilot/Grok/Cursor contract files, not
  duplicated inline in any of them (verified via grep before this change),
  so editing it alone keeps all agent mirrors in agreement — no other
  contract file needed a parallel edit.
- Open decisions: none remaining after Adjudicator wording approval in
  chat; PR itself still needs an Adjudicator merge decision.

## Routing

- Model/assistant/tool: Claude Code, direct file inspection and patching
- Reason: Cross-agent process contract change (branch/PR discipline
  applies to every agent listed in `AGENTS.md`)
- Privacy constraints: No private data, secrets, or provider data used

## AI Execution Records

### Attempt 1

- Agent: Claude (Sonnet 5)
- Environment: Local QPex repository
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
- Scope: Replaced the "Rules" list under "Branch and PR Granularity" to
  state explicitly when to create the branch, when to open the PR
  (Issue-complete and doc-synced, not per phase), and when to request
  merge.
- Result: Adjudicator considered and explicitly rejected an earlier
  draft-PR-at-Phase-1-Red alternative ("AIと実装すると5分で終わるから
  ISSUEが完了したらPR作る方針でいい"), then approved this simpler wording
  in chat before the edit was made.
- Attempt boundary: No application code or tests changed
- Notes: Confirmed with the Adjudicator that this governs all agents (not
  Claude-specific) before editing, since the file is shared contract
  content per `prompt-instruction-change-control.md`.

## Cost / Reasoning Control

- Operating path: process contract change (same rigor as Architecture Path)
- Files read: `docs/collaboration/branch-commit-pr-discipline.md`,
  `docs/collaboration/definition-of-done.md`,
  `docs/collaboration/prompt-instruction-change-control.md`, agent contract
  mirror files (grepped for references, not duplicated content)
- Context intentionally omitted: application implementation and unrelated
  specs
- Deterministic checks used: `git diff` review of the single changed
  section; `grep` across `AGENTS.md`/`CLAUDE.md`/Copilot/Grok/Cursor files
  to confirm no duplicated content needed a parallel edit
- Escalation reason: Agent operating contract change requires Adjudicator
  review and a trace per `prompt-instruction-change-control.md`
- Avoided LLM work: No external model or provider routing
- Rework caused by AI output: The first proposed wording (open PR at
  Phase 1 Red) and the second (draft PR at Phase 1 Red) were both
  superseded by Adjudicator direction before any doc edit was made — no
  wasted edits, only wasted proposals, since wording was confirmed in chat
  before editing each time

## Adjudicator Decisions

- Adjudicator rejected "open PR at Phase 1 Red" and "draft PR at Phase 1
  Red" alternatives in favor of "PR only at Issue completion, after
  documentation is checked."
- Adjudicator confirmed this policy applies to all agents listed in
  `AGENTS.md`, not only Claude Code.
- Adjudicator approved the exact final wording in chat before the edit was
  made.
- Adjudicator has not yet reviewed/merged the resulting PR; that review is
  separate from the wording approval above per the Approval Model.

## Verification

- Commands/checks: `git diff` (single section replaced, no other content
  changed); re-read the surrounding "Feature-Unit Branch Creation" section
  to confirm no contradiction with the new PR-timing rule.
- Result: Documentation-only change; no test suite applicable.

## Changed Files

- `docs/collaboration/branch-commit-pr-discipline.md`
- `docs/collaboration/traces/2026-07-25-pr-timing-issue-completion.md`

## Next Safe Action

- Adjudicator reviews and merges this process-contract PR (or requests
  wording changes). Do not merge based only on automated CI, per
  `prompt-instruction-change-control.md`.
- Apply this PR-timing default going forward: create Issue branches
  immediately, but do not open a PR until the Issue's approved scope is
  complete and its documentation is synchronized.

## Notes

- This is the second amendment to "Branch and PR Granularity" the same day
  (after PR #13). Both were driven by the Adjudicator observing this
  session's actual PR/merge cadence and asking for the document to match
  the intended practice rather than the other way around.
