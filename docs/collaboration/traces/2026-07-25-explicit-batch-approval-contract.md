# AI Work Trace

## Request

- Date: 2026-07-25
- User request: Strengthen the agent contract so explicit ordered instructions
  are distinguished from assistant recommendations and issue work never mutates
  `main`.
- Current phase: Architecture Path — process contract update
- Canonical issue or work plan: Process change; no new LISS created yet
- AI planning record: Current conversation design intake

## Context Ledger

- Included: `AGENTS.md`, `CLAUDE.md`, Copilot/Grok/Cursor contract files,
  prompt-instruction change control, and branch discipline.
- Omitted: application source, tests, provider code, and unrelated ADRs.
- Assumptions: `CLAUDE.md` imports `AGENTS.md`; Cursor loads root
  `AGENTS.md` independently. Copilot and Grok require matching effective rules.
- Open decisions: Adjudicator review is required before merge; no application
  behavior is changed.

## Routing

- Model/assistant/tool: Codex plus deterministic file inspection and patching
- Reason: Cross-agent process contract change
- Privacy constraints: No private data, secrets, or provider data used

## AI Execution Records

### Attempt 1

- Agent: Codex
- Environment: Local QPex repository
- Model as displayed: unavailable
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
- Scope: Contract wording and cross-agent consistency
- Result: Added explicit batch approval, approval-source, and main-branch
  mutation rules to the agent contract mirrors.
- Attempt boundary: No application code or tests changed
- Notes: Pre-existing uncommitted documentation changes were preserved and
  intentionally not staged.

## Cost / Reasoning Control

- Operating path: Architecture Path
- Files read: Contract and change-control documents listed above
- Context intentionally omitted: application implementation and unrelated specs
- Deterministic checks used: `git diff --check`, contract text comparison
- Escalation reason: Agent operating contract change requires Adjudicator review
- Avoided LLM work: No external model or provider routing
- Rework caused by AI output: None

## Adjudicator Decisions

- Pending explicit review of the contract wording and mirror consistency.

## Verification

- Commands/checks: `git diff --check`; `git diff --name-only`; effective-rule review
- Result: Pending final review; application tests are not applicable.

## Changed Files

- `AGENTS.md`
- `.github/copilot-instructions.md`
- `.grok/rules/01-quickstart.md`
- `docs/collaboration/traces/2026-07-25-explicit-batch-approval-contract.md`

## Next Safe Action

- Adjudicator reviews this process-contract PR. Do not merge based only on
  automated checks.

## Notes

- `CLAUDE.md` and Cursor rules inherit or independently load `AGENTS.md`; no
  duplicate wording was added there.
