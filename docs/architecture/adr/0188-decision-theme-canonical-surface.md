# ADR 0188: Decision-theme canonical surface

## Status

**Accepted** (2026-08-04) — architecture decision for WP-0091.

## Context

The project has 186 numbered ADRs whose decisions are now grouped into seven
coherent themes. Keeping every historical narrative in the active tree makes
the current language and architecture difficult to read. ADR 0187 established
source-record compaction for Issues, Work Plans, and Traces; the same recovery
discipline is now required for settled ADR narratives.

## Decision

1. The seven `DEC-####` documents in
   `docs/architecture/decision-themes/` are the current reading surface for
   settled decisions, with `decision-theme-register.md` as their index.
2. The numbered ADRs `0001`–`0186` are historical source records for those
   themes. They are removed from the working tree after this migration; their
   exact bodies remain recoverable from
   `docs/pre-canonicalization-2026-08-03` at
   `8663ba72295964069ac275b93c350e762a0844d8`.
3. ADR 0187 remains the governing policy for source-record compaction. ADR
   0188 is retained because it defines the current decision surface and the
   archival boundary.
4. New architecture decisions use a retained ADR when an independent
   acceptance boundary is needed, and must also update the affected `DEC-*`
   page. Existing ADR numbers are never reused.
5. The compression map is the sole current-tree index for removed ADR paths;
   redirect stubs are not created.

## Consequences

- Developers start with seven theme pages rather than 186 historical files.
- Historical decision wording remains reproducible without rewriting Git
  history.
- References to settled ADRs point to the relevant theme page; historical
  identifiers may remain in prose where they provide provenance.
- Open Issues, active Work Plans, and required review evidence remain full
  records under ADR 0187.

## Verification

- Every ADR `0001`–`0186` is assigned exactly once in the decision-theme
  register.
- Every removed path is recorded in the compression map and exists at the
  baseline tag.
- Link, documentation, specification, and test suites pass after migration.
