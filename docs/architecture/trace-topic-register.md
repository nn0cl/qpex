# Trace topic register

This register groups phase-level and planning traces by the shared LISS/WP topic. The retained path is the current representative record; deleted paths are recoverable from the immutable baseline and are also recorded in `documentation-compression-map.md`.

## Recovery

- Source tag: `docs/pre-canonicalization-2026-08-03`
- Source commit: `8663ba72295964069ac275b93c350e762a0844d8`
- Recovery: `git show docs/pre-canonicalization-2026-08-03:<source_path>`

## Consolidated topics

| Topic | Representative Trace | Consolidated source paths |
|---|---|---|
| `LISS-0068` | `docs/collaboration/traces/2026-07-27-liss-0068-e0-adjudicator-completion.md` | `2026-07-27-liss-0068-rebaseline-slice2.md`; `2026-07-27-liss-0068-rebaseline-slice3.md`; `2026-07-28-liss-0068-v1-promotion.md` |
| `LISS-0069` | `docs/collaboration/traces/2026-07-28-liss-0069-slice-c-plan-intake.md` | `2026-07-28-liss-0069-plan-intake.md`; `2026-07-28-liss-0069-slice-a-phase1-red.md`; `2026-07-28-liss-0069-slice-b-plan-intake.md`; `2026-07-28-liss-0069-slice-c-completion.md` |
| `LISS-0071` | `docs/collaboration/traces/2026-07-28-liss-0071-slice-c-plan-intake.md` | `2026-07-28-liss-0071-completion.md`; `2026-07-28-liss-0071-plan-intake.md`; `2026-07-28-liss-0071-slice-b-phase1-red.md`; `2026-07-28-liss-0071-slice-b-phase2-green.md`; `2026-07-28-liss-0071-slice-b-plan-intake.md`; `2026-07-28-liss-0071-slice-c-phase2-green.md` |
| `LISS-0072` | `docs/collaboration/traces/2026-07-28-liss-0072-plan-intake.md` | `2026-07-28-liss-0072-completion.md`; `2026-07-28-liss-0072-slice-a-phase1-red.md`; `2026-07-28-liss-0072-slice-a-phase2-green.md`; `2026-07-28-liss-0072-slice-a-phase3-refactor.md`; `2026-07-28-liss-0072-slice-b-phase3-refactor.md`; `2026-07-28-liss-0072-slice-c-phase3-refactor.md` |
| `LISS-0073` | `docs/collaboration/traces/2026-07-29-liss-0073-slice-g-plan-intake.md` | `2026-07-28-liss-0073-plan-intake.md`; `2026-07-28-liss-0073-slice-b-plan-intake.md`; `2026-07-28-liss-0073-slice-c-plan-intake.md`; `2026-07-28-liss-0073-slice-d-plan-intake.md`; `2026-07-29-liss-0073-slice-e-phase1-red.md`; `2026-07-29-liss-0073-slice-e-plan-intake.md`; `2026-07-29-liss-0073-slice-f-phase1-red.md`; `2026-07-29-liss-0073-slice-f-plan-intake.md`; `2026-07-29-liss-0073-slice-g-phase1-red.md`; `2026-07-29-liss-0073-slice-g-phase2-green.md` |
| `LISS-0074` | `docs/collaboration/traces/2026-07-29-liss-0074-slice-e-plan-intake.md` | `2026-07-29-liss-0074-plan-intake.md`; `2026-07-29-liss-0074-slice-b-plan-intake.md`; `2026-07-29-liss-0074-slice-c-plan-intake.md`; `2026-07-29-liss-0074-slice-d-phase2-green.md`; `2026-07-29-liss-0074-slice-d-plan-intake.md`; `2026-07-29-liss-0074-slice-e-phase1-red.md`; `2026-07-29-liss-0074-slice-e-phase2-green.md` |
| `LISS-0075` | `docs/collaboration/traces/2026-07-29-liss-0075-plan-intake.md` | `2026-07-29-liss-0075-completion.md`; `2026-07-29-liss-0075-pause-before-slice-c.md`; `2026-07-29-liss-0075-residual-triage.md`; `2026-07-29-liss-0075-slices-c-d-complete.md` |
| `LISS-0076` | `docs/collaboration/traces/2026-07-29-liss-0076-slice-e.md` | `2026-07-29-liss-0076-plan-intake.md`; `2026-07-29-liss-0076-slice-a.md`; `2026-07-29-liss-0076-slice-d.md` |
| `LISS-0080` | `docs/collaboration/traces/2026-07-29-liss-0080-plan-intake.md` | `2026-07-29-liss-0080-slice-c-green-refactor.md`; `2026-07-29-liss-0080-slice-d-green-refactor.md` |
| `LISS-0081` | `docs/collaboration/traces/2026-07-29-liss-0081-plan-intake.md` | `2026-07-29-liss-0081-global-closeout.md` |
| `LISS-0082` | `docs/collaboration/traces/2026-07-30-liss-0082-slice-b-review.md` | `2026-07-29-liss-0082-design-deepening.md`; `2026-07-29-liss-0082-plan-intake.md`; `2026-07-30-liss-0082-completion-audit.md`; `2026-07-30-liss-0082-gap3-design.md`; `2026-07-30-liss-0082-gap3-green.md`; `2026-07-30-liss-0082-gap3-red.md`; `2026-07-30-liss-0082-gap3-refactor.md`; `2026-07-30-liss-0082-slice-b-final-review.md`; `2026-07-30-liss-0082-slice-b-followup-green.md`; `2026-07-30-liss-0082-slice-b-followup-red.md`; `2026-07-30-liss-0082-slice-b-red.md`; `2026-07-30-liss-0082-slice-c-design.md`; `2026-07-30-liss-0082-slice-c-green.md`; `2026-07-30-liss-0082-slice-c-refactor.md`; `2026-07-30-liss-0082-slice-c-status-sync.md`; `2026-07-30-liss-0082-slice-d-design.md`; `2026-07-30-liss-0082-slice-d-status-sync.md`; `2026-07-30-liss-0082-slice-e-cross-cutting-redesign.md`; `2026-07-30-liss-0082-slice-e-red.md` |
| `LISS-0114` | `docs/collaboration/traces/2026-07-29-liss-0114-slice-f-complete.md` | `2026-07-29-liss-0114-slice-b-complete.md` |
| `LISS-0115` | `docs/collaboration/traces/2026-07-29-liss-0115-slice-d-complete.md` | `2026-07-29-liss-0115-slice-c.md` |
| `LISS-0120` | `docs/collaboration/traces/2026-07-30-liss-0120-language-review-gate-intake.md` | `2026-07-31-liss-0120-rebaseline-intake.md` |
| `LISS-0123` | `docs/collaboration/traces/2026-07-31-liss-0123-applied-heal-complete.md` | `2026-07-31-liss-0123-0124-complete.md` |
| `LISS-0196` | `docs/collaboration/traces/2026-08-03-liss-0196-accept-open-topics-sync.md` | `2026-08-03-liss-0196-trait-surface-design-draft.md` |
| `LISS-0250` | `docs/collaboration/traces/2026-08-02-liss-0250-phase3-complete.md` | `2026-08-02-liss-0250-phase1-red.md`; `2026-08-02-liss-0250-phase2-green.md` |
| `LISS-0254` | `docs/collaboration/traces/2026-08-02-liss-0254-s01-quantities-heal.md` | `2026-08-02-liss-0254-phase1-red.md`; `2026-08-02-liss-0254-phase2-green.md`; `2026-08-02-liss-0254-phase3-refactor.md` |
| `LISS-0289` | `docs/collaboration/traces/2026-08-03-liss-0289-post-sugar-resync.md` | `2026-08-03-liss-0289-post-sugar-face-resync.md` |
| `LISS-0290` | `docs/collaboration/traces/2026-08-03-liss-0290-phase3-refactor.md` | `2026-08-03-liss-0290-phase1-red.md`; `2026-08-03-liss-0290-phase2-green.md` |
| `WP-0072` | `docs/collaboration/traces/2026-08-01-wp-0072-s01-coverage-residuals-intake.md` | `2026-08-01-wp-0072-execution.md` |
| `WP-0088` | `docs/collaboration/traces/2026-08-02-wp-0088-wave-b-accept.md` | `2026-08-02-wp-0088-approval-filing.md`; `2026-08-02-wp-0088-wave-a.md`; `2026-08-02-wp-0088-wave-b-adr-drafts.md` |
| `WP-0089` | `docs/collaboration/traces/2026-08-03-wp-0089-adoption-pass.md` | `2026-08-02-wp-0089-surface-adoption-and-sugar-plan.md`; `2026-08-03-wp-0089-chapters-and-sugar-adrs.md`; `2026-08-03-wp-0089-sugar-kernel-0180-0183.md` |

## Rule

A new phase trace is not added when the same topic already has a current representative and the new record contains no unresolved obligation, approval boundary, or review evidence. Update the representative or canonical ADR/Issue/WP instead. Active or directly referenced records remain at their original paths until their references are intentionally migrated.
