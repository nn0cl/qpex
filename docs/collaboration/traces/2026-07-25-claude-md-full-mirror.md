# AI Work Trace

## Request

- Date: 2026-07-25
- User request: Review why `CLAUDE.md` was not operating with the same
  strictness as the other agent contract files (Grok, Copilot), then update
  the context files so Claude Code achieves equivalent, strict behavior.
- Current phase: Architecture Path — process contract update
- Canonical issue or work plan: Process change; no new LISS created. Amends
  ADR 0006.
- AI planning record: Current conversation design intake plus two explicit
  Adjudicator choices (full-mirror vs. minimal reinforcement; drop vs. keep
  `@AGENTS.md`) captured inline in this session.

## Context Ledger

- Included: `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`,
  `.grok/rules/*.md`, `.cursor/rules/*.mdc`, `docs/architecture/adr/0006-prompt-instruction-change-control.md`,
  `docs/collaboration/prompt-instruction-change-control.md`,
  `docs/collaboration/adoption-guide.md`.
- Omitted: application source, tests, provider code, unrelated ADRs and
  Issues.
- Assumptions: Cursor's mechanism (native `AGENTS.md` auto-apply) is a
  verified product feature independent of Claude Code's `@`-import and is
  not affected by this change.
- Open decisions: none remaining — both forks (full mirror vs. minimal;
  drop vs. keep the import) were resolved by explicit Adjudicator choice
  before editing began.

## Routing

- Model/assistant/tool: Claude Code (this session) plus deterministic file
  inspection (`Read`/`Bash`/`git`/`gh`)
- Reason: Cross-agent process contract change requires the same agent that
  found the gap to propose and, on explicit approval, implement the fix
- Privacy constraints: No private data, secrets, or provider data used

## AI Execution Records

### Attempt 1

- Agent: Claude Code (Sonnet 5)
- Environment: Local Staqex repository, branch `process/claude-md-full-mirror`
- Model as displayed: claude-sonnet-5
- Reasoning setting as displayed: unavailable (not surfaced to the agent)
- Estimated token range: N/A
- Estimated token midpoint: N/A
- Actual tokens: unavailable
- Token metric: unavailable
- Token source: unavailable
- Token attribution boundary: this task only
- Actual token unavailable reason: runtime does not expose the metric
- Estimate variance: unavailable
- Variance reason: unavailable
- Scope: `CLAUDE.md` full-mirror rewrite; ADR 0006 revision; consistency-check
  wording sync in `prompt-instruction-change-control.md` and
  `adoption-guide.md`; this trace
- Result: `CLAUDE.md` converted from a `@AGENTS.md` import plus Claude-only
  sections into a full literal mirror (Prime Directive, Mandatory Design
  Check, Approval Model, Explicit Batch and Approval Source Rules, Session
  Entry, Clean Architecture Dependency Rule, External Resources Must Be
  Ports) plus its existing Claude/Staqex-specific sections, matching the
  Copilot/Grok structural pattern. The `@AGENTS.md` line was removed.
- Attempt boundary: No application code or tests changed
- Notes: Two design forks were resolved by explicit Adjudicator choice
  (via `AskUserQuestion`) before any file was edited: (1) full mirror over
  minimal Cursor-style reinforcement, and (2) drop the `@AGENTS.md` import
  entirely over keeping it as a redundant fallback.

## Cost / Reasoning Control

- Operating path: Architecture Path
- Files read: all five agent operating contract files, ADR 0006,
  `prompt-instruction-change-control.md`, `adoption-guide.md`,
  `process-gap-register.md`
- Context intentionally omitted: application implementation and unrelated
  specs/Issues
- Deterministic checks used: `git status`, `git diff --check`, `git log`,
  `gh pr` (for the earlier LISS-0048 evidence cited in ADR 0006)
- Escalation reason: Agent operating contract change requires Adjudicator
  review per `docs/collaboration/prompt-instruction-change-control.md`
- Avoided LLM work: No external model or provider routing
- Rework caused by AI output: None; this is itself a correction of an
  earlier Adjudicator-approved design (ADR 0006, 2026-07-16) based on new
  evidence from live session behavior, not a defect in this trace's own work

## Adjudicator Decisions

- Confirmed: full-mirror approach over minimal Cursor-style reinforcement.
- Confirmed: drop the `@AGENTS.md` import line entirely rather than keep it
  alongside the mirrored text.
- Pending: final PR review of the contract wording and mirror consistency.

## Verification

- Commands/checks: `git diff --check`; manual side-by-side comparison of
  `CLAUDE.md`'s new sections against `AGENTS.md`'s source text for effective
  content match; repo-wide grep for stale `@AGENTS.md`/"CLAUDE.md resolves"
  references.
- Result: `git diff --check` clean. One stale reference found and fixed
  (`docs/collaboration/adoption-guide.md`). Application tests not applicable
  (no code changed).

## Changed Files

- `CLAUDE.md`
- `docs/architecture/adr/0006-prompt-instruction-change-control.md`
- `docs/collaboration/prompt-instruction-change-control.md`
- `docs/collaboration/adoption-guide.md`
- `docs/collaboration/traces/2026-07-25-claude-md-full-mirror.md` (this file)

## Next Safe Action

- Adjudicator reviews this process-contract PR. Do not merge based only on
  automated checks (CI's "Repository sanity" trace-presence check is
  necessary but not sufficient — it cannot verify effective-content
  correctness, only that a trace file exists).

## Notes

- `.grok/rules/*.md` and `.github/copilot-instructions.md` are unchanged;
  they already carried the full mirror and needed no edit.
- `.cursor/rules/*.mdc` is unchanged; its mechanism (native `AGENTS.md`
  auto-apply) is unaffected by this Claude Code-specific finding.
