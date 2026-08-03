# Local Issue Planning

Local Issues are the durable planning records for offline work and AI-agent
coordination. GitHub Issues remain useful for remote collaboration, but they do
not replace the repository-native record.

## Canonical locations

- Issues: `docs/issues/LISS-0001-short-title.md`
- Multi-issue plans: `docs/work-plans/WP-0001-short-title.md`
- Current open/deferred/completed summary:
  [`docs/architecture/open-work-register.md`](../architecture/open-work-register.md)
- Documentation compression and recovery:
  [`documentation-canonicalization-policy.md`](../architecture/documentation-canonicalization-policy.md)

Do not create a second hand-maintained inventory of all Issues or Work Plans.
The current register summarizes status; source files carry the detailed
acceptance and dependency record.

## Stable identifiers

- `LISS` means local issue. Never reuse an Issue ID.
- `WP` means work plan. Never reuse a Work Plan ID.
- When a GitHub Issue exists, record its number or URL in the local metadata.
- Before claiming a new ID, search the repository, including the baseline
  compression tag and open branches.

## Required Issue metadata

Each Issue should record:

- ID and title
- status and phase
- type and priority
- initial and current planning size
- owner or agent
- dependencies, blocks, parent, and related work
- branch and GitHub Issue when available
- acceptance notes and Adjudicator decision points
- an AI planning record for size `M`, `L`, or `XL`

Use exactly one durable planning artifact for a bug or feature. Other notes,
traces, and work plans link to that artifact instead of copying mutable status
prose.

## Required Work Plan metadata

A Work Plan is appropriate for multiple related Issues or an approved bounded
batch. It must state:

- scope and exclusions
- dependency order
- branch and approval record
- execution phases
- verification and stopping conditions
- status synchronization destinations

Feature work still follows the branch, phase, review, and completion rules in
[`branch-commit-pr-discipline.md`](branch-commit-pr-discipline.md) and
[`definition-of-done.md`](definition-of-done.md).

## Status values

Use these current values:

`proposed`, `ready`, `in_progress`, `blocked`, `review`,
`final-review-ready`, `complete`, `open`, `deferred`, `superseded`, and
`wont_do`.

Historical `done` remains readable but new records should use `complete`.

## Phase values

`phase-0-design`, `phase-1-red`, `phase-2-green`, `phase-3-refactor`,
`docs-only`, and `process-only`.

## Planning size

| Size | Use when |
|---|---|
| `S` | One area, explicit behavior, local correction, deterministic check |
| `M` | Related multi-file change, small behavior change, or second attempt |
| `L` | Multiple modules/phases, broad verification, or meaningful uncertainty |
| `XL` | Architecture boundary, migration, many dependencies, or high uncertainty |
| `TBD` | Investigation is required before sizing |

Choose the largest applicable size. Preserve the initial size and record the
reason for any reclassification.

## Dependency and execution rules

- `depends_on` blocks execution until completion or explicit waiver.
- `blocks` identifies downstream work; `parent` identifies decomposition;
  `related` is context only.
- Every Issue or Work Plan change uses a dedicated branch, never `main`.
- Begin with design intake. Do not start implementation before the reviewed
  acceptance specification and applicable phase approval.
- Synchronize Issue status, Work Plan status, accepted spec/ADR references, and
  completion evidence in the same reviewable unit.

## Inbox

`docs/issues/inbox/` is scratch space before an Issue exists. When promoted,
completed, or superseded, move the note to `inbox/archive/` or remove it when
the durable Issue contains all useful information. Do not leave closed-work
notes in the live inbox.

## AI planning records

Size `M`, `L`, and `XL` work needs a vendor-neutral AI planning record with the
status, authoring environment, date, size, route, estimate or `N/A` reason,
assumptions, confidence, and revision links. See
[`ai-work-trace-log.md`](ai-work-trace-log.md).

## Review triggers

Stop for Adjudicator review when dependencies are unclear, an Issue is split or
merged, a boundary changes, a branch scope diverges from the plan, or a status
cannot be synchronized deterministically.
