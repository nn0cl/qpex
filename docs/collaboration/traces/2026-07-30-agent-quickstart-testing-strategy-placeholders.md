# AI Work Trace

## Request

- Date: 2026-07-30
- User request: Fill the unfilled template placeholders left in
  `docs/architecture/agent-quickstart.md`, then the same class of placeholders
  in `docs/architecture/testing-strategy.md`, with correct project values. Add
  `docs/architecture/agent-quickstart.md` to the agent operating contract file
  list if agents other than Claude read it.
- Current phase: documentation-only (no AT-TDD phase; no test or implementation
  change)
- Canonical issue or work plan: none — Adjudicator-directed documentation
  correction discovered during a `/doctor` configuration review. No LISS Issue
  was opened; see Next Safe Action if one is required retroactively.
- AI planning record: in-session design note (scope, inspected files,
  constraints, verification plan) presented before each file was edited.

## Context Ledger

- Included: `docs/architecture/agent-quickstart.md`,
  `docs/architecture/testing-strategy.md`,
  `docs/collaboration/prompt-instruction-change-control.md`,
  `docs/architecture/README.md` (§Ports, §Selected Technology, §Runtime
  Direction, §Detailed Rules, §Remaining Technology Evaluation), `CLAUDE.md`
  (§External Resources Must Be Ports, §Project Boundaries),
  `docs/architecture/open-work-register.md`, `.github/workflows/ci.yml`,
  `QUICKSTART.md`, `tests/` tree listing, `compiler/staqex/` port class names.
- Omitted: ADR bodies, `docs/specs/` contents, issue and work-plan documents,
  example programs. None of the filled values required them; every value was
  derived from the architecture documents and the actual repository tree.
- Assumptions: the `<FILL IN: ...>` and `` `<Add ...>` `` forms are unfilled
  collaboration-template leftovers rather than intentional content. Generic
  syntax such as `<T>` in `staqex-abstraction-model.md` and VO names such as
  `<DomainEntityId>` in `ai-request-routing.md` are legitimate content and were
  left untouched.
- Open decisions: whether the Front-End Tests and E2E Tests sections should be
  deleted outright rather than marked not-applicable; whether the placeholder
  fixes needed a LISS Issue.

## Routing

- Model/assistant/tool: Claude Code (Claude Opus 5); deterministic `grep` /
  `ls` / `jq` inspection for all fact gathering.
- Reason: the task is documentation correction whose correctness depends on
  repository facts. Every value was verified against the tree rather than
  generated, to satisfy the minimal-hallucination constraint.
- Privacy constraints: local repository content only. No external network
  access, no source or document content sent to any third party.

## AI Execution Records

### Attempt 1

- Agent: Claude Code
- Environment: macOS desktop app session, repository
  `/Users/nn0cl/Documents/git/qpex`
- Model as displayed: Opus 5 (`claude-opus-5`)
- Reasoning setting as displayed: not displayed in this session surface
- Estimated token range: not estimated before execution
- Estimated token midpoint: n/a
- Actual tokens: unavailable
- Token metric: n/a
- Token source: n/a
- Token attribution boundary: n/a
- Actual token unavailable reason: the session surface does not expose
  per-attempt token counters to the agent.
- Estimate variance: n/a
- Variance reason: n/a
- Scope: three placeholder sites in `agent-quickstart.md` (§Core Boundaries,
  §Required Area Documents, §Stop Conditions); four placeholder sites in
  `testing-strategy.md` (Acceptance Tests placement, Front-End Tests, E2E
  Tests, Mocking Rule); one list addition in
  `prompt-instruction-change-control.md`.
- Result: complete. Zero placeholders remain outside `docs/templates/` and
  `docs/collaboration/traces/`.
- Attempt boundary: one continuous session; no retry or rollback.
- Notes: an earlier proposal in the same session to trim `CLAUDE.md:279-320`
  was withdrawn after inspection showed the doc index duplicates
  `agent-quickstart.md` for only 5 of 27 entries; the Adjudicator judged the
  index intentional and no `CLAUDE.md` change was made.

## Optional Reference Total

- Value: n/a
- Metric: n/a
- Source: n/a
- Compatibility statement: no cross-attempt totals are combined.

## Cost / Reasoning Control

- Operating path: Fast Path escalated to a documented design note per file,
  because `agent-quickstart.md` and
  `prompt-instruction-change-control.md` define agent behavior.
- Files read: listed under Context Ledger. Architecture documents were read
  section-by-section rather than whole where possible.
- Context intentionally omitted: ADR bodies and specification documents, since
  every value was available from the architecture documents and the tree.
- Deterministic checks used: placeholder-residue `grep`; existence check of all
  25 paths referenced by the edited `agent-quickstart.md`; existence check of
  the 5 new paths and 3 port class names referenced by the edited
  `testing-strategy.md`; `grep` confirmation that four agent families reference
  `agent-quickstart.md`.
- Escalation reason: none. No architecture or technology decision was required;
  all values already existed in accepted documents.
- Avoided LLM work: no generated prose describing project structure — the
  document classification was taken from `docs/architecture/README.md`
  §Detailed Rules rather than re-derived.
- Rework caused by AI output: one self-corrected error. An initial report
  described `CLAUDE.md:279-320` as duplicating `agent-quickstart.md:144-153`;
  inspection showed only 5 of 27 entries overlap, and the claim was withdrawn
  before any edit was made.

## Adjudicator Decisions

- Fill the `agent-quickstart.md` placeholders with correct values
  (2026-07-30).
- Fill the `testing-strategy.md` placeholders as well (2026-07-30).
- Add `docs/architecture/agent-quickstart.md` to the agent operating contract
  file list, conditional on non-Claude agents reading it. Condition verified:
  `AGENTS.md:34`, `.github/copilot-instructions.md:94`,
  `.grok/rules/01-quickstart.md:88`, and `CLAUDE.md:130` each direct agents to
  read it (2026-07-30).
- Leave `CLAUDE.md` unchanged; its document index is intentional, not
  redundant (2026-07-30).

## Verification

- Commands/checks:
  - `grep -rn '<FILL IN\|`<Add ' docs/ *.md` excluding `docs/templates/` and
    `docs/collaboration/traces/` — expected 0 hits.
  - existence check of every `docs/`, `tests/`, and `compiler/` path newly
    referenced by the two edited architecture documents.
  - `grep -rn 'class QpuSubmitPort\|class QpuJobPort\|class
    ObservationExecutionPort' compiler/staqex/` to confirm the mocking-rule
    examples name ports that exist.
- Result: placeholder count 0; all referenced paths and all three port classes
  exist. No test or implementation file was touched, so no AT-TDD verification
  applies.

## Changed Files

- `docs/architecture/agent-quickstart.md` — filled §Core Boundaries datastore
  placeholder with the MVP no-datastore boundary and the port list; filled
  §Required Area Documents with the stack-specific document set; replaced the
  four generic §Stop Conditions placeholders with this project's real
  technology-choice stop conditions. The removed placeholder referenced a
  `CLAUDE.md` section named "Current Non-Decision" that does not exist; the
  replacement points to `docs/architecture/README.md` §Remaining Technology
  Evaluation and `docs/architecture/open-work-register.md` instead.
- `docs/architecture/testing-strategy.md` — filled acceptance-test placement
  with the real `tests/` layout and script-based runner; marked Front-End Tests
  and E2E Tests not applicable to the MVP, since there is no UI framework and
  no deployment target; replaced the three placeholder port names in the
  Mocking Rule with `QpuSubmitPort`, `QpuJobPort`, and
  `ObservationExecutionPort`.
- `docs/collaboration/prompt-instruction-change-control.md` — added
  `docs/architecture/agent-quickstart.md` to the agent operating contract file
  list, with the four referencing contract files named inline.

## Next Safe Action

- Align `.github/workflows/ci.yml:176` with the contract file list: the case
  pattern does not include `docs/architecture/agent-quickstart.md`, so CI will
  not require a trace when only that file changes. The document and the CI gate
  currently disagree.
- Decide whether the Front-End Tests and E2E Tests sections of
  `testing-strategy.md` should be deleted rather than marked not-applicable.
- Decide whether this documentation correction requires a retroactive LISS
  Issue under `docs/collaboration/local-issue-planning.md`.

## Notes

- `CLAUDE.md:341-358` "Current Open Topics" is stale relative to
  `docs/architecture/open-work-register.md`: ADR 0057 density matrix / Lindblad
  CPTP, `evolve ... until`, pipeline `|>` / currying, trait `impl`, and
  concrete QPU IR are all recorded there as complete or Phase 3 reviewed while
  `CLAUDE.md` still lists them as not accepted. No change was made; the
  Adjudicator was informed.
- `docs/architecture/agent-quickstart.md` §Required Area Documents previously
  carried an unfilled placeholder in the same list that already held five real
  entries, which is why the file read as partially configured rather than
  clearly incomplete.
