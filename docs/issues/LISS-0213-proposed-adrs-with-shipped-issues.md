# LISS-0213: Four ADRs remain `Proposed` while their dependent Issues shipped

## Metadata

- Local issue ID: LISS-0213
- Status: **complete** — 2026-08-01 (WP-0077)
- Phase: docs-only
- Type: process
- Priority: P2
- Planning size: S
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Related: `CLAUDE.md` §Approval Model

## Intent

`CLAUDE.md` states that a `Proposed` ADR "records a design candidate only. It
does not authorize implementation." Four ADRs are still `Proposed` while the
Issues that depend on them are complete and shipped in the Kernel. Either the
ADRs should have been promoted, or shipped code is running without accepted
architecture authority.

## Evidence (verified 2026-08-01)

| ADR | Title | Status | Dependent Issue |
|---|---|---|---|
| [0065](../architecture/adr/0065-job-based-host-execution.md) | Job-based host execution | **Proposed** | LISS-0022 — "Phase 3 complete" |
| [0075](../architecture/adr/0075-povm-measurement-contract.md) | POVM measurement contract | **Proposed** | LISS-0037 — "Phase 3 reviewed; terminal computational-basis POVM slice complete" |
| [0076](../architecture/adr/0076-numeric-representation-policy.md) | Numeric representation policy | **Proposed** | LISS-0018 — "Phase 3 reviewed; numeric policy slice complete" |
| [0097](../architecture/adr/0097-numeric-representation-horizon.md) | Numeric representation horizon | **Proposed** | cited by the open-work register as governing `f64` policy |

ADR 0076 / 0097 are additionally cited as live constraints by
[`staqex-v1-open-topics-permanent-out.md`](../specs/staqex-v1-open-topics-permanent-out.md)
("ADR 0076/0097 still constrain runtime") and by ADR 0125's rational-mode
boundary — so `Proposed` documents are being treated as binding.

Each ADR body also carries the sentence "This ADR does not authorize
implementation or provider selection", which the shipped state contradicts.

## Adjudicator decision points

1. Per ADR: promote to `Accepted` with a date, or record explicitly that the
   shipped slice ran ahead of acceptance and what that means?
2. If promoted, does the `Accepted` text need narrowing to the slice that
   actually shipped, rather than the full proposal?
3. Is there a systemic gap — should a check flag "Proposed ADR referenced by a
   complete Issue"? (Cheap to add next to the existing consistency script.)

## Exit

- [x] Each of the four ADRs has a status that matches reality
- [x] Where a slice shipped narrower than the ADR proposed, the ADR says so
- [x] Decision recorded on whether to automate the check

## Non-goals

Reopening the design decisions in those ADRs; auditing all 162 ADRs — only
these four were found `Proposed`-with-shipped-dependents.

## Resolution (WP-0077)

Promoted ADR 0065 / 0075 / 0076 / 0097 to **Accepted** (2026-08-01) with
shipped-slice narrowing. Automation check deferred to a later Issue.
