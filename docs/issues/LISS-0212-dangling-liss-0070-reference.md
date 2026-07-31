# LISS-0212: `LISS-0070` is referenced by six documents but was never created

## Metadata

- Local issue ID: LISS-0212
- Status: **proposed** (investigation intake)
- Phase: docs-only
- Type: bug
- Priority: P2
- Planning size: S
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)

## Intent

`LISS-0070` is cited as the tracking Issue for the Rust compiler /
differential-oracle work and as the blocker for conformance Slice D. No
`docs/issues/LISS-0070-*.md` exists, and `local-issue-planning.md` lists 0070
among the unused IDs that must not be reused.

## Evidence (verified 2026-08-01)

`ls docs/issues/LISS-0070*` → no matches. Referenced by:

```
docs/architecture/open-work-register.md          "deferred — next version"; tracked as LISS-0070 in WP-0025
docs/work-plans/WP-0025-staqex-v1-north-star.md
docs/specs/staqex-v1-conformance-plan.md         Slice D "blocked on LISS-0070"
docs/specs/staqex-v1-conformance-scenario-catalog.md  "Rust differential (Slice D / LISS-0070)"
docs/specs/staqex-v1-migration-matrix.md
docs/specs/staqex-v1-cst-formatter-plan.md
```

The effect is that conformance Slice D is blocked on an Issue that cannot be
opened, started, or closed, and the open-work register records a dependency
that does not resolve.

## Adjudicator decision points

1. Restore `LISS-0070` as a real deferred Issue (it is a reserved ID, so this
   is legitimate), or rewrite the six references to point at the Rust row in
   the open-work register directly?
2. If restored: is the Rust VM still the intended path, given the shipping
   Python Kernel? The register says "deferred — next version" — confirm that is
   still the position before writing an Issue that implies scheduling.

## Exit

- [ ] `LISS-0070` exists, or every reference to it is rewritten
- [ ] Conformance Slice D's blocker resolves to something actionable
- [ ] Reserved-ID list in `local-issue-planning.md` updated to match

## Non-goals

Starting the Rust work; changing the deferral decision.
