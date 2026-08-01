# LISS-0216: Issue-planning vocabulary, index, and inbox have drifted from practice

## Metadata

- Local issue ID: LISS-0216
- Status: **complete** — 2026-08-01 (WP-0077)
- Phase: process-only
- Type: process
- Priority: P3
- Planning size: S
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Related: [`local-issue-planning.md`](../collaboration/local-issue-planning.md),
  [`definition-of-done.md`](../collaboration/definition-of-done.md)

## Intent

`local-issue-planning.md` is the normative document for how Issues are written,
but three of its parts no longer describe what the repository does.

## Evidence (verified 2026-08-01)

**1. Status vocabulary is incomplete.** §Status Values defines

```
proposed | ready | in_progress | blocked | review | done | wont_do
```

Recent Issues and the Definition of Done completion gate actually use
`complete`, `open`, `deferred`, `superseded`, and `final-review-ready` — none of
which are in the list. LISS-0195 (`complete`), LISS-0196 (`open`), LISS-0197
(`deferred`), LISS-0186 (`superseded`) are all current examples, and
`definition-of-done.md` mandates `final-review-ready` → `complete` by name.

**2. The Issue index is 62 IDs stale.** §Current Staqex local issues stops
around LISS-0135, while the §Active ID claims table in the same file runs to
LISS-0197. Two tables in one document disagree about which Issues exist, and
only one is maintained.

**3. `docs/issues/inbox/` holds three notes for closed work:**

```
docs/issues/inbox/2026-07-23-examples-driven-brush-up.md
docs/issues/inbox/2026-07-23-openqasm3-braket-codegen.md
docs/issues/inbox/2026-07-27-examples-catalog-v2-refresh.md
```

All three correspond to Issues that have since completed. Nothing documents
what the inbox is for or when a note leaves it.

## Adjudicator decision points

1. Extend §Status Values to the vocabulary actually in use, or bring practice
   back to the seven listed values? (Recommend extending — the DoD gate depends
   on `final-review-ready`, so practice is the more considered of the two.)
2. Retire the §Current Staqex local issues index and keep §Active ID claims as
   the single table, or maintain both with a check? (Recommend retiring the
   index; a hand-maintained duplicate is what drifted.)
3. Define the inbox lifecycle, or remove the directory?

## Exit

- [x] Status vocabulary matches practice and the DoD gate
- [x] One Issue table, not two
- [x] Inbox lifecycle defined or directory removed
- [x] `docs/templates/local-issue.md` reconciled with the lean form recent
      Issues actually use

## Non-goals

Changing the Definition of Done completion gate; retro-editing existing Issue
files to a new status vocabulary.

## Resolution (WP-0077)

Extended Status Values; retired the stale local-issues index; archived closed
inbox notes under `docs/issues/inbox/archive/` and documented inbox purpose.
