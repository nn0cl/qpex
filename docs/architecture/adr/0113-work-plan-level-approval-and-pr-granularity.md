# ADR 0113: Work-plan-level approval, push, PR, and merge granularity (Claude Code only)

## Status

Accepted (2026-07-30). Depends on
[ADR 0112](0112-claude-code-contract-independence.md) for the precedence that
makes a Claude-only approval model effective.

**Applies to Claude Code only.** `AGENTS.md`, `.github/copilot-instructions.md`,
`.grok/rules/*.md`, and `.cursor/rules/*.mdc` are unchanged by this decision,
and so are the rules those agents follow. The normative text lives in
`CLAUDE.md`; the shared documents carry pointers that explicitly state the
Issue-level default and the per-phase approval rule still bind every other
agent. See §Cross-Agent Containment.

Adjudicator architecture approval given 2026-07-30. No follow-up Issue is
required: this decision is fully realized by the contract-document changes that
accompany it, and it authorizes no product implementation. The first real
`execution-batch-<id>.json` record will exercise the mechanism; creating it is
ordinary work under this decision, not an outstanding obligation of it.

## Context

Approval and review granularity currently sit at two different levels, and
both produce more Adjudicator moments than the Adjudicator wants.

**Approval.** `CLAUDE.md` §Claude Code Issue-Level Autonomy (approved
2026-07-26) already reduces approvals to two per Issue, but as
[ADR 0112](0112-claude-code-contract-independence.md) §Context documents, four
competing per-phase statements are read first and no precedence rule exists, so
the effective granularity remains per phase.

**Branch, push, PR, and merge.** `docs/collaboration/branch-commit-pr-discipline.md`
§Branch and PR Granularity fixes these at one Issue. The same document
instructs the agent to "keep branches short-lived" (`:35`) and to avoid
"accumulating multiple issues or phases on one long-running branch" (`:36-37`).
That rule was itself a reaction to too many merge moments: memory of the
2026-07-25 session records three PRs merged in quick succession for closely
related LISS-0048/LISS-0049 work, and the Issue-level rule was the fix. The
Adjudicator now judges the Issue level still too fine.

**Work plans are not uniformly sized.** Across the 28 documents in
`docs/work-plans/`, distinct `LISS-` references per work plan are:

| Measure | Issues |
|---|---|
| Median | 4 |
| Minimum | 0 |
| Maximum | 56 (`WP-0025-staqex-v1-north-star.md`) |
| Second | 28 (`WP-0029-current-hardware-delivery-horizon.md`) |
| Third | 19 (`WP-0004-open-architecture-backlog.md`) |

A blanket "one approval per work plan" rule is therefore safe at the median and
unsafe at the tail. WP-0025 spans specification rebaseline, Rust compiler
infrastructure, and frontend work, and `docs/architecture/open-work-register.md`
records for it that "implementation remains per-Issue gated" — an existing
condition that an unbounded work-plan approval would contradict.

**The mechanism already exists and is unused.** ADR 0006 established bounded
execution batch records; `docs/templates/execution-batch-review.md` defines the
JSON shape; `.github/workflows/ci.yml:112` runs
`scripts/check-execution-batch-reviews.py`, which validates required fields,
status transitions, the `batch/<batch-id>` branch convention, and the changed
paths from `approval_commit` against `allowed_paths`. No
`execution-batch-*.json` record has ever been created:
`docs/collaboration/reviews/` contains only two Markdown review records.

The Adjudicator's stated requirements on 2026-07-30 were: raise approval
granularity to the work plan; keep every document that is produced today;
preserve the hard stop that presents detailed premises and options when a
specification decision is needed; keep the AT-TDD frame intact; keep commit
granularity unchanged while moving push, PR, and merge to the work-plan level.

## Dependency Adoption Evidence

Not applicable. No library, framework, provider SDK, datastore client, build
tool, or test helper is selected by this decision. The one code change is a
field addition to an existing first-party validation script.

## Decision

0. **A mandatory investigation step precedes any batch approval.** Because a
   work-plan batch is a broad grant, alignment with the Adjudicator must be
   deliberate rather than assumed. Design already happens while a work plan is
   drafted; this decision makes it a named stage with defined outputs and its own
   approval type. The stage is documents-only — no test, no implementation, no
   status promotion, no ADR acceptance — and it produces: the specification or
   ADR; the local Issues with their scope and exit conditions; a stated rationale
   for the Issue granularity, including which splits were rejected and which
   Issues are deliberately excluded; the execution order with explicit
   dependencies; and a draft batch record. The agent then presents inspected
   premises, the granularity and ordering options with consequences, a
   recommendation, and remaining open questions, and stops. `Investigation
   approval` and `Batch approval` become distinct approval types in `CLAUDE.md`
   §Approval Model, and investigation approval authorizes neither the batch, nor
   a phase, nor implementation.

1. **Approval granularity is the work plan, expressed as a bounded execution
   batch.** One `docs/collaboration/reviews/execution-batch-<id>.json` record
   per approved work-plan scope replaces the per-Issue Plan and Completion
   approvals for the Issues it names.

2. **`work_plan_id` is an optional field in the shared schema, required by
   `CLAUDE.md` for Claude Code.** It names the governing
   `docs/work-plans/WP-*.md`. `schema_version` stays `1` and the field is not
   added to `REQUIRED_FIELDS`, so no record any other agent writes becomes
   invalid. `scripts/check-execution-batch-reviews.py` validates the value only
   when present — format `WP-[0-9]{4}` and the existence of the work-plan
   document — so a Claude record cannot point at a work plan that does not
   exist, while no other agent is newly constrained. An earlier draft of this
   ADR made the field required at `schema_version: 2`; that was withdrawn on
   2026-07-30 because it would have changed CI behavior for every agent.

3. **`issue_ids` remains an enumerated required field.** A work-plan batch
   names the Issues it covers rather than granting the whole work plan. This
   keeps the envelope bounded for a 56-Issue work plan, preserves the CI
   `allowed_paths` audit, and lets one work plan be executed as several
   successive batches. Completing a named Issue does not authorize an Issue the
   record does not list.

4. **Commit granularity is unchanged.** Phase-tagged commits (Red, Green,
   Refactor, doc-sync) continue exactly as
   `docs/collaboration/branch-commit-pr-discipline.md` §Commits specifies.

5. **Branch, push, PR, and merge granularity become the work plan, for Claude
   Code.** One branch and one pull request per work-plan batch, accumulating the
   phase-tagged commits of every Issue in the batch. The branch uses the
   existing `batch/<batch-id>` convention, which the CI validator already
   enforces. The pull request opens once, when the batch's approved scope is
   complete and its documentation is synchronized. For Claude Code the "keep
   branches short-lived" and "do not accumulate multiple issues on one branch"
   rules are relaxed: a batch branch is long-lived by design, bounded by the
   record's `expires_at` rather than by Issue count. Those rules keep their
   original force for every other agent, and
   `docs/collaboration/branch-commit-pr-discipline.md` keeps the Issue-level
   default as its normative text.

6. **Hard stops are preserved and are not weakened by batch approval.** When an
   unanticipated design or architecture decision surfaces mid-batch, the agent
   stops and asks, presenting the detailed premises and the available options
   rather than resolving it. The record's `invalidating_triggers` continue to
   void the batch. Batch approval does not waive the Issue, branch, phase, ADR,
   or human-review rules, and CI success is not Adjudicator approval.

7. **Every artifact produced today is still produced.** The local Issue, the
   work plan, the AT-TDD Red tests, the AI work trace, the Definition of Done
   check, and the batch record itself are all unchanged. This decision reduces
   the number of approval and merge moments, not the number of documents.

8. **`post_review_required` is `true` for any batch that includes an
   implementation phase.** The Adjudicator reviews after execution rather than
   before each phase; removing the pre-phase gate does not remove review.

## Cross-Agent Containment

Every file this decision touches was audited for leakage into the other agent
families. The result:

| File | Scope after this ADR |
|---|---|
| `CLAUDE.md` | Claude Code only. All normative text for the investigation step, work-plan approval, and batch branch/PR rules lives here. |
| `docs/collaboration/branch-commit-pr-discipline.md` | Unchanged for other agents. The Issue-level default and the per-phase approval rule remain the normative text; a clearly labelled pointer notes the Claude-only alternative and states that nothing changes for `AGENTS.md`, Copilot, Codex, Grok, or Cursor. |
| `docs/architecture/agent-quickstart.md` | Unchanged for other agents. §Phase Rule keeps its per-phase gate as the rule and carries a non-normative Claude-only pointer that says so explicitly. |
| `docs/templates/execution-batch-review.md` | `work_plan_id` optional, `schema_version` still `1`. No record any other agent writes becomes invalid. |
| `scripts/check-execution-batch-reviews.py` | Validates `work_plan_id` only when present. A record without it passes exactly as before, so CI behavior for other agents is unchanged. |
| `docs/at-tdd/process.md` | Not modified at all. Claude reaches its carve-out through `CLAUDE.md`'s precedence declaration. |
| `AGENTS.md` | Not modified by this ADR. (ADR 0112 corrects one retired keyword there; that is a defect fix, not a rule change.) |

The containment rule for future changes: a Claude-only process rule belongs in
`CLAUDE.md`. A shared document may carry only a pointer, and that pointer must
state which agents it does not apply to.

## Consequences

Positive:

- Approval moments for a median work plan drop from roughly one per phase
  across four Issues to one batch approval plus one post-review, while the
  investigation step converts the removed per-phase check-ins into a single
  deliberate alignment before the grant is made.
- The broad grant is scoped against an explicitly agreed specification, Issue
  split, and execution order rather than against an assumed shared
  understanding.
- Merge moments drop to one per work-plan batch, which is the concern that
  originally motivated the Issue-level rule, applied one level up.
- The batch mechanism, its template, and its CI validator stop being dead
  weight and start carrying the workflow they were built for.
- The envelope stays machine-checkable: CI verifies the branch name, the
  changed paths against `allowed_paths`, expiry, and status transitions.

Negative:

- A long-lived batch branch diverges from `main` for longer, so merge conflicts
  and stale-branch risk increase. `docs/collaboration/branch-commit-pr-discipline.md:95`
  warns about exactly this, and the warning now applies by design rather than as
  an exception.
- One pull request carries many Issues, so it is larger and harder to review as
  a unit. The existing escape hatch — split when a reviewable unit becomes too
  large — remains, but it now requires deliberate judgment instead of falling
  out of the Issue-level default.
- Errors introduced early in a batch are not caught at a phase boundary and can
  propagate across several Issues before post-review sees them. The agent's
  self-verification obligation in `CLAUDE.md` §Claude Code Issue-Level Autonomy
  carries more weight than before.
- Batch scoping becomes a judgment call. A record that names too many Issues
  recreates the unbounded-approval risk that Decision point 3 exists to
  prevent.

## Enforcement

Code review should reject:

- a Claude Code batch record without `work_plan_id` (the shared schema allows
  its absence; `CLAUDE.md` does not);
- a change that makes `work_plan_id` required in the shared schema, or that
  bumps `schema_version`, without a decision that explicitly accepts the effect
  on the other agent families;
- a Claude-only process rule written as normative text in a shared document
  instead of in `CLAUDE.md`, or a pointer in a shared document that fails to
  state which agents it does not apply to;
- execution started on any Issue of a batch before the investigation output was
  approved and the batch record separately approved;
- an investigation step that produced no specification or ADR, no Issue
  granularity rationale, or no execution order with dependencies;
- an agent setting a batch record to `approved_for_execution` itself;
- a batch record that omits `issue_ids`, or that names Issues outside the
  governing work plan;
- work on an Issue that the active batch record does not name;
- a pull request opened at an intermediate phase of a batch, or a branch that
  carries batch work without the `batch/<batch-id>` name;
- a batch that includes an implementation phase with
  `post_review_required` set to `false`;
- a mid-batch design or architecture decision resolved by the agent instead of
  escalated to the Adjudicator with premises and options;
- any claim that batch approval supplies phase, ADR, or implementation
  approval it does not name.
