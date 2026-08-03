# LISS-0291: Surface adoption wave 2 (post–WP-0089 / LISS-0290)

## Metadata

- Local issue ID: LISS-0291
- Status: **complete** (2026-08-03)
- Type: Feature examples + docs hygiene
- Priority: P1
- Depends: WP-0089 **complete**; LISS-0290 **complete**

## Summary

After verifying main (WP-0089 + LISS-0290), close remaining **adoption debt** that
left official samples behind shipped sugars:

1. Drop redundant `// staqex-profile: experiment` on single-file basics (ADR 0182 default).
2. Convert remaining absolute `import examples.…` multi-file mains to relative.
3. Refresh friction ledger to post-0290 truth.

## Exit

- [x] Basics singles rely on default experiment profile
- [x] Applied A02/A04/A07/A09/A10 + QMD + S01 tri relative imports
- [x] Friction ledger §5 updated
- [x] seed-0 on touched samples
