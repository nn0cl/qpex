# LISS-0279: Package root naming policy + migration

## Metadata

- Local issue ID: LISS-0279
- GitHub issue: _(none yet)_
- Status: **proposed**
- Phase: docs + examples (no Kernel semantics change expected)
- Type: Feature / docs
- Priority: P1
- Program: [WP-0089](../work-plans/WP-0089-surface-adoption-and-sugar.md)
- Depends: [LISS-0274](LISS-0274-wp-0089-program-lock.md)
- Paths: package policy doc (north star companion or project-structure);
  `examples/**/*.sqx` package/import lines; tests that hardcode package paths

## Summary

Define official package root for samples: prefer short **`staqex.examples…`**
(or equivalent) over reverse-DNS **`com.staqex.examples…`**. Migrate official
examples that still use `com.staqex` without changing module semantics. Document
that reverse-DNS remains **legal** for external libraries.

## Problem

`com.staqex…` is pure JVM enterprise symbol with no physics reading.

## Exit

- [ ] Written policy: default sample root; external packages free
- [ ] Official examples migrated (or explicit defer list with reason)
- [ ] Imports / multi-file graphs updated together
- [ ] SV / tests that assert package strings updated
- [ ] No behavior change to physics

## Non-goals

- Module system redesign
- Forbidding `package` on multi-file programs
- Relative import sugar (LISS-0287)

## Adjudicator Decision Points

- Exact root string: `staqex.examples` vs `examples` vs keep `com.` for one
  release with deprecation note only

## Verification

- rg count of `package com.staqex` in `examples/` → 0 or documented exceptions
- Seed-0 / module tests
