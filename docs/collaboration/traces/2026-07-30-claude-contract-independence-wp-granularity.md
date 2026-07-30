# AI Work Trace

## Request

- Date: 2026-07-30
- User request: Reduce the number of Adjudicator approval steps while keeping
  the hard stop that presents detailed premises and options when a
  specification decision is needed, and keeping the AT-TDD frame and all its
  documents intact. Raise approval granularity to the work-plan level. Keep
  commit granularity as-is but move push, PR, and merge to the work-plan level.
  Remove the `AGENTS.md` mirror clause from `CLAUDE.md`, absorbing
  `AGENTS.md`-only content first.
- Current phase: Architecture Path — process and contract decision. No AT-TDD
  phase; no test or product code change.
- Canonical issue or work plan: none yet. Both ADRs record "Follow-up Issue: to
  be assigned"; see Next Safe Action.
- AI planning record: in-session investigation and a 12-item change plan,
  presented and approved before any file was edited. Two Adjudicator choices
  shaped it: work-plan batches keep `issue_ids` enumerated, and the mirror
  clause is removed outright rather than scoped.

## Context Ledger

- Included: `CLAUDE.md`, `AGENTS.md`,
  `docs/collaboration/prompt-instruction-change-control.md`,
  `docs/collaboration/branch-commit-pr-discipline.md`,
  `docs/architecture/adr/0006-prompt-instruction-change-control.md`,
  `docs/architecture/adr/0026-*.md` (supersession convention),
  `docs/architecture/adr/0066-*.md`, `docs/architecture/agent-quickstart.md`,
  `docs/at-tdd/process.md`, `docs/templates/adr.md`,
  `docs/templates/execution-batch-review.md`,
  `docs/templates/ai-work-trace.md`,
  `scripts/check-execution-batch-reviews.py`, `.github/workflows/ci.yml`,
  `docs/architecture/open-work-register.md`,
  `docs/specs/staqex-language-specification.md:558`, `docs/work-plans/` listing,
  `docs/collaboration/reviews/` listing.
- Omitted: product code, tests, example programs, specification bodies other
  than the one line needed to confirm the canonical constructor spelling.
- Assumptions: the Adjudicator's "ワーキングプラン単位" means the approval and
  review unit, not the removal of per-Issue documents; "文章は作成される必要が
  ある" means every artifact produced today still gets produced.
- Open decisions: the status of both ADRs (they are `Proposed`, so they do not
  authorize the accompanying contract changes to merge); whether a LISS Issue is
  required; whether `CLAUDE.md` §Current Open Topics should be corrected.

## Routing

- Model/assistant/tool: Claude Code (Claude Opus 5); deterministic `grep`,
  `sed`, `git`, `jq`, and `python3` inspection for every factual claim.
- Reason: the decision rests on what the repository actually says. Each
  conflicting statement was located by line before being cited, because the
  central finding is a contradiction between documents.
- Privacy constraints: local repository only. No network access, no repository
  content sent to any third party.

## AI Execution Records

### Attempt 1

- Agent: Claude Code
- Environment: macOS desktop app session, repository
  `/Users/nn0cl/Documents/git/qpex`, branch
  `docs/claude-contract-independence-wp-granularity`
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
- Scope: two new ADRs; supersession note on ADR 0006; `CLAUDE.md` mirror
  removal, content absorption, precedence, and autonomy extension; mirror-clause
  amendment in `prompt-instruction-change-control.md`; `work_plan_id` in the
  batch template and validator; work-plan granularity in
  `branch-commit-pr-discipline.md`; `fn init` correction in `AGENTS.md`;
  contract-pattern fix in `ci.yml`.
- Result: complete as a proposal. All ten files changed; verification below
  passes. Nothing is authorized to merge until the ADRs are accepted.
- Attempt boundary: one continuous session, following an earlier commit
  (`a865235`) of unrelated placeholder work on a separate branch.
- Notes: the preceding placeholder work was committed first, on its own branch,
  because `CLAUDE.md:109-110` requires stopping when uncommitted changes make
  branch ownership unclear.

## Optional Reference Total

- Value: n/a
- Metric: n/a
- Source: n/a
- Compatibility statement: no cross-attempt totals are combined.

## Cost / Reasoning Control

- Operating path: Architecture Path.
- Files read: listed under Context Ledger, read by section rather than whole
  where the section was known.
- Context intentionally omitted: product code and tests, which no part of this
  decision touches.
- Deterministic checks used: see Verification.
- Escalation reason: two decisions were escalated rather than resolved. The
  mirror-clause treatment (remove versus scope) and the ADR split (one versus
  two) were both put to the Adjudicator with premises and options; the
  Adjudicator chose removal and two ADRs.
- Avoided LLM work: the conflicting statements were located by `grep` and cited
  by line rather than recalled; the work-plan size distribution was computed
  from the tree rather than estimated.
- Rework caused by AI output: two corrections, both self-found.
  1. An earlier statement claimed adding `work_plan_id` needed no validator
     change. That holds only if the field is left unvalidated; CI enforcement
     would have required a `REQUIRED_FIELDS` addition and a `schema_version`
     bump. The Adjudicator was told before the change was made.
  2. **Cross-agent leakage in this agent's own first pass.** When the Adjudicator
     asked for a containment double-check, an audit of the ten changed files
     found three changes that silently bound the other agent families:
     `docs/collaboration/branch-commit-pr-discipline.md` had been rewritten so
     the work-plan batch became the default granularity *for every agent*;
     `docs/templates/execution-batch-review.md` made `work_plan_id` required at
     `schema_version: 2`; and
     `scripts/check-execution-batch-reviews.py` enforced that requirement in CI,
     so any record another agent wrote without the field would have failed. All
     three were reverted to Claude-only scope, as recorded under Changed Files.
     Nothing had been committed, so the leakage never left the working tree.

## Adjudicator Decisions

- Raise approval granularity to the work plan, keeping `issue_ids` enumerated
  rather than granting a whole work plan (2026-07-30).
- Remove the `AGENTS.md` mirror clause from `CLAUDE.md` outright; the scoped
  alternative ("mirror except for enumerated divergences") was presented and
  declined (2026-07-30).
- Absorb `AGENTS.md`-only content into `CLAUDE.md` as part of the removal
  (2026-07-30).
- Keep commit granularity; move push, PR, and merge to the work-plan level
  (2026-07-30).
- Split the decision into two ADRs rather than one (2026-07-30).
- Add a mandatory investigation step before any batch approval, producing the
  specification, the Issues, the Issue-granularity rationale, and the execution
  order, because work-plan approval is a broad grant that needs deliberate
  alignment first (2026-07-30).
- Contain the change to Claude Code, double-checking that no other agent family
  is affected (2026-07-30).
- Commit the pending placeholder work first, on its own branch, and start this
  work on a new branch (2026-07-30).

## Verification

- Commands/checks:
  - `python3 -m py_compile scripts/check-execution-batch-reviews.py` — syntax.
  - `python3 scripts/check-execution-batch-reviews.py --branch ""` — behavior
    with zero records, confirming no regression from the `schema_version` bump.
  - `jq empty` over the JSON block extracted from
    `docs/templates/execution-batch-review.md` — template validity.
  - `git diff .github/workflows/ci.yml` — confirms the edit is a single pattern
    inside the existing shell `case` block, between `;;` and `esac`, so the
    surrounding YAML literal block is unchanged. A `yaml.safe_load` check was
    attempted but PyYAML is not installed in this environment; this was not
    substituted with a weaker claim of YAML validation.
  - `grep -n 'fun init\|`fun`'` across the contract files — confirms the
    retired keyword is gone from the absorbed text and from `AGENTS.md`.
  - `grep -n 'mirror\|AGENTS.md' CLAUDE.md` — confirms no stale mirror claim
    survives and caught `CLAUDE.md:165`, which still ordered the agent to read
    `AGENTS.md` first; that step was rewritten.
  - **Cross-agent containment test**, run by importing `validate_record` and
    exercising it against synthetic records:
    a record with no `work_plan_id` passes (other agents unaffected);
    a record naming an existing work plan passes;
    `WP-9999` fails with "work plan document not found";
    `WP-25` fails with "invalid work plan ID";
    `schema_version: 2` fails, confirming the withdrawn bump is really gone.
  - `REQUIRED_FIELDS` extracted and printed to confirm `work_plan_id` is absent
    from it.
- Result: all checks pass. Two residual `fun` occurrences remain at
  `CLAUDE.md:428` and `:435`; see Notes.

## Changed Files

- `docs/architecture/adr/0112-claude-code-contract-independence.md` — new,
  `Proposed`. Supersedes the `CLAUDE.md` literal-full-mirror portion of ADR
  0006, requires `CLAUDE.md` self-sufficiency, names the four absorbed items,
  and declares precedence over `agent-quickstart.md` and `at-tdd/process.md`
  for Claude Code.
- `docs/architecture/adr/0113-work-plan-level-approval-and-pr-granularity.md` —
  new, `Proposed`. Work-plan approval via a bounded execution batch with
  required `work_plan_id` and enumerated `issue_ids`; commit granularity
  unchanged; branch, push, PR, and merge at the work-plan level.
- `docs/architecture/adr/0006-prompt-instruction-change-control.md` — Status
  records the partial supersession, following the ADR 0026 convention. The rest
  of ADR 0006 stays in force.
- `CLAUDE.md` — mirror clause replaced by an independence and precedence
  statement; new §Project absorbing the `State<T>` semantics, language surface,
  and long-term target; ADR-and-ambiguity-boundary rule added to §Mandatory
  Design Check; honest phase-status reporting added to §Phase Discipline, whose
  unconditional phase sentence is now qualified; §Claude Code Issue-Level
  Autonomy renamed and extended with a work-plan level, an explicit hard-stop
  subsection, and branch/commit/PR guidance; reading sequence step 1 no longer
  points at `AGENTS.md`.
- `docs/collaboration/prompt-instruction-change-control.md` — `CLAUDE.md`
  excluded from the cross-file consistency check, with the review, reason, and
  trace obligations restated as still applying.
- `docs/templates/execution-batch-review.md` — `work_plan_id` documented as an
  **optional** field, `schema_version` unchanged at `1`, with the Claude-only
  obligation named as living in `CLAUDE.md` rather than imposed here.
- `scripts/check-execution-batch-reviews.py` — `work_plan_id` validated **only
  when present** (`WP-[0-9]{4}` plus existence of the work-plan document);
  `REQUIRED_FIELDS` and `schema_version` are unchanged, so no record another
  agent writes becomes invalid.
- `docs/collaboration/branch-commit-pr-discipline.md` — the Issue-level default
  and the per-phase approval rule are **restored as the normative text**. A
  labelled Claude-only pointer describes the work-plan alternative and states
  that nothing changes for `AGENTS.md`, Copilot, Codex, Grok, or Cursor. The two
  bullet-level carve-outs (Phase 2 precondition, short-lived branches) are marked
  "Claude Code only … Unchanged for every other agent."
- `AGENTS.md` — `fun init` corrected to `fn init`. It was teaching a keyword
  retired by ADR 0066 (2026-07-23) to Copilot, Codex, Grok, and Cursor.
- `.github/workflows/ci.yml` — `docs/architecture/agent-quickstart.md` added to
  the contract-file pattern, closing the gap opened by commit `a865235`.

## Next Safe Action

- Both ADRs were accepted by the Adjudicator on 2026-07-30 and record that no
  follow-up Issue is required; `docs/architecture/README.md` §Accepted Decisions
  (collaboration template) now lists them. This branch is complete and ready for
  its pull request.
- Exercise the new mechanism once: create the first
  `docs/collaboration/reviews/execution-batch-<id>.json`. No record has ever
  existed, so while the validator's rejection paths were tested with synthetic
  records, its happy path is still unproven against a real committed file.
- Decide separately whether `CLAUDE.md` §Current Open Topics should be corrected
  against `open-work-register.md`; see Notes.

## Notes

- The core finding is that the autonomy the Adjudicator granted on 2026-07-26
  was never in force. Four statements assert per-phase approval
  (`agent-quickstart.md:100` and `:106-107`, `CLAUDE.md:186`,
  `at-tdd/process.md:12`, `:77`, `:124`), the earliest is read at step 2 of
  `CLAUDE.md`'s own reading sequence, and no precedence rule existed. The
  mirror clause compounded it by instructing the agent to treat the divergence
  as a defect.
- `CLAUDE.md:428` still lists "Trait `impl` surface; measure-effect marking on
  `fun`" as an open topic. It uses the retired `fun` keyword, and
  `open-work-register.md` records both trait `impl` (ADR 0082) and effect
  marking (ADR 0081) as Phase 3 reviewed and shipped. `CLAUDE.md:435` also
  mentions `fun`, but legitimately, as history. The whole §Current Open Topics
  section is stale against `open-work-register.md`; the Adjudicator judged it
  out of scope earlier in this session, so it was left untouched rather than
  quietly widened into this change.
- `docs/at-tdd/process.md` and `docs/architecture/agent-quickstart.md` were
  deliberately not rewritten to Claude's approval model. They remain normative
  for the other agent families. `agent-quickstart.md` §Phase Rule carries only a
  non-normative pointer to `CLAUDE.md`'s autonomy section, explicitly stating
  that the per-phase gate still binds `AGENTS.md`, Copilot, Codex, Grok, and
  Cursor. `docs/at-tdd/process.md` was left entirely untouched; Claude reaches
  its carve-out through `CLAUDE.md`'s precedence declaration rather than through
  an edit to a document the other four agents share.
