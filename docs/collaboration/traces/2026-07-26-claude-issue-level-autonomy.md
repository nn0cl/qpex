# AI Work Trace

## Request

- Date: 2026-07-26
- User request: The current `CLAUDE.md` approval cadence (a separate
  Scope/Architecture/Technology/Phase check-in before each of Red, Green,
  and Refactor) has not matched how this session actually operated with
  Claude Code — strict adherence is not realistic. Add a Claude-only
  operating mode collapsing this to two Adjudicator approval points (plan,
  completion), with an explicit stop-and-ask rule for any unanticipated
  design decision found mid-work, and a self-verification step before
  reporting completion. Do this in `CLAUDE.md` only — do not edit
  `AGENTS.md`, `.github/copilot-instructions.md`, `.grok/rules/*.md`,
  `.cursor/rules/*.mdc`, or `docs/collaboration/prompt-instruction-change-control.md`,
  since those are read by other agents (including lightweight models
  currently following the strict cadence correctly) and editing them risks
  affecting behavior this change is not meant to touch.
- Current phase: process contract update (Claude-only operating mode)
- Canonical issue or work plan: Process change; no LISS created. Amends
  `CLAUDE.md` only.
- AI planning record: Current conversation design intake; exact wording
  drafted, then compacted on request, then approved verbatim before this
  edit was made.

## Context Ledger

- Included: `CLAUDE.md` (full text, to find placement and confirm no
  internal contradiction), `docs/collaboration/prompt-instruction-change-control.md`
  (to identify the consistency requirement this change intentionally does
  not satisfy across files, and to confirm the trace requirement that does
  still apply to `CLAUDE.md` itself), `docs/collaboration/branch-commit-pr-discipline.md`
  (referenced by the new section, not edited).
- Omitted: `AGENTS.md`, `.github/copilot-instructions.md`,
  `.grok/rules/*.md`, `.cursor/rules/*.mdc` — deliberately not read for
  editing purposes; this change does not touch them, by explicit
  instruction.
- Assumptions: `prompt-instruction-change-control.md`'s cross-file
  consistency check ("Code review should reject: ... agent operating
  contract changes that leave `AGENTS.md`, `CLAUDE.md`, ... inconsistent
  with each other in effective content") is a code-review guideline, not a
  CI-enforced gate (only trace-file presence is CI-enforced per that
  document's own "Enforcement" section). The Adjudicator, as the human
  reviewer that guideline exists to inform, is the one making this specific,
  documented exception — this is not a silent or accidental divergence.
- Open decisions: none remaining — exact wording was proposed, then
  shortened on request, then approved before editing.

## Routing

- Model/assistant/tool: Claude Code (this session), direct file editing
- Reason: The change is specifically about Claude Code's own operating
  cadence; no other agent's file is touched
- Privacy constraints: No private data, secrets, or provider data used

## AI Execution Records

### Attempt 1

- Agent: Claude (Sonnet 5)
- Environment: Local QPex repository, branch `process/claude-issue-level-autonomy`
- Model as displayed: claude-sonnet-5
- Reasoning setting as displayed: unavailable
- Estimated token range: N/A
- Estimated token midpoint: N/A
- Actual tokens: unavailable
- Token metric: unavailable
- Token source: unavailable
- Token attribution boundary: this task only
- Actual token unavailable reason: runtime does not expose the metric
- Estimate variance: unavailable
- Variance reason: unavailable
- Scope: Added a "Claude Code Issue-Level Autonomy" section to `CLAUDE.md`,
  placed after "Phase Discipline" and before "Project Boundaries". No other
  file touched.
- Result: Section added verbatim as approved; this trace records the
  intentional cross-file divergence.
- Attempt boundary: No application code or tests changed
- Notes: The Adjudicator explicitly considered and rejected adding a
  matching carve-out to `prompt-instruction-change-control.md` itself (the
  author's first proposal), on the grounds that the file is read by other
  agents/lightweight models currently following the strict cadence
  correctly, and any edit there — even a narrow, Claude-specific exception
  clause — risks affecting their behavior. The final instruction was to
  touch `CLAUDE.md` only.

## Cost / Reasoning Control

- Operating path: process contract change (same rigor as Architecture Path)
- Files read: `CLAUDE.md` (full), `docs/collaboration/prompt-instruction-change-control.md`,
  `docs/collaboration/branch-commit-pr-discipline.md` (for the cross-reference
  in the new section)
- Context intentionally omitted: `AGENTS.md` and the other three agent
  contract mirrors — not read, not edited, by design
- Deterministic checks used: `git diff` review of the single new section;
  read-through of the full `CLAUDE.md` after the edit to confirm no
  internal contradiction with the unedited Approval Model / Phase
  Discipline sections above it (the new section explicitly narrows those,
  rather than silently ignoring them)
- Escalation reason: `CLAUDE.md` is a listed agent operating contract file
  under `prompt-instruction-change-control.md`; a trace is required for any
  change to it, including this Claude-only one
- Avoided LLM work: No external model or provider routing
- Rework caused by AI output: The first full-length wording draft was
  shortened on request before approval; no wasted file edits, since wording
  was finalized in chat before touching `CLAUDE.md`

## Adjudicator Decisions

- Confirmed: the divergence lives in `CLAUDE.md` only; `AGENTS.md` and the
  other three agent contract files are explicitly not to be edited or
  treated as needing a matching update.
- Confirmed: `prompt-instruction-change-control.md` itself is also not to
  be edited, even to add a narrow cross-file exception clause, because it
  is read by other agents/lightweight models.
- Approved the exact final (shortened) wording in chat before this edit was
  made.
- Pending: final review of this specific PR/diff.

## Verification

- Commands/checks: `git diff` (single new section, ~20 lines, no other
  content changed); manual read-through confirming the new section
  correctly scopes itself as Claude-only and does not silently contradict
  the still-present, unedited Approval Model / Phase Discipline sections
  above it.
- Result: Documentation-only change; no test suite applicable.

## Changed Files

- `CLAUDE.md`
- `docs/collaboration/traces/2026-07-26-claude-issue-level-autonomy.md` (this file)

## Next Safe Action

- Adjudicator reviews and merges this process-contract PR. Do not merge
  based only on automated CI (trace-file-presence check is necessary but
  not sufficient — it cannot verify that the intentional cross-file
  divergence recorded here is actually what the Adjudicator wants kept
  long-term).
- Apply this cadence starting with the next Feature Path Issue: state
  expected design-decision risk immediately after plan approval, run
  Red/Green/Refactor without per-phase check-ins, stop immediately on any
  unanticipated design decision, and self-verify all three phases before
  requesting completion approval.

## Notes

- This is an intentional, permanent (until revisited) divergence in
  effective content between `CLAUDE.md` and `AGENTS.md`/the other three
  agent contract mirrors, for this one section only. Every other section of
  `CLAUDE.md` that mirrors `AGENTS.md` content remains untouched and must
  still be reviewed as literally matching `AGENTS.md` per the existing
  rule; only this new, clearly-labeled section is exempt.
