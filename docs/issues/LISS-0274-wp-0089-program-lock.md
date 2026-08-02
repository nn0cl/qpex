# LISS-0274: WP-0089 program lock (success criteria + Keep list)

## Metadata

- Local issue ID: LISS-0274
- GitHub issue: _(none yet)_
- Status: **complete** (2026-08-03) — plan approved; lock recorded
- Phase: docs-only
- Type: Architecture / docs
- Priority: P0 (gates the rest of WP-0089)
- Program: [WP-0089](../work-plans/WP-0089-surface-adoption-and-sugar.md)
- Approval: [2026-08-03-wp-0089-plan-approval.md](../collaboration/reviews/2026-08-03-wp-0089-plan-approval.md)
- Paths: `docs/work-plans/WP-0089-…`,
  `docs/architecture/surface-modernization-north-star.md` §5 companion WP

## Summary

Lock the post–WP-0088 language-face program so every adoption and sugar Issue
shares one success definition, Keep list, and Out list. Prevents parallel
“modernize” work from diverging (e.g. samples inventing unshipped syntax, or
sugar ADRs weakening axioms).

## Acceptance Notes

- [x] WP-0089 status remains the single program ledger (plan-approved 2026-08-03)
- [x] North star §5 links WP-0089 as the **adoption + sugar** follow-on to WP-0088
- [x] Keep / Out lists in WP-0089 §2 binding for child Issues
- [x] Finding → Issue map in WP-0089 §3 complete

## Dependencies

- Parent: WP-0089
- Depends on: WP-0088 complete (levers shipped)
- Blocks: LISS-0275–0289 (conceptually; Adjudicator may allow parallel docs drafts)

## Adjudicator Decision Points

- Accept WP-0089 as the sole program for these findings (no split into multiple WPs)
- Confirm non-goals (no Kernel `if`/`try`, no live QPU, no S01 collapse)

## Context

- Included: re-review 2026-08-02; north star; minimal dialect; ADRs 0176–0179
- Omitted: implementation
- Assumptions: B08 remains the chalk reference face

## Verification

- Docs-only review; no code
- Checklist: every re-review P0/P1/P2/§5 row maps to an Issue ID in WP-0089 §3
