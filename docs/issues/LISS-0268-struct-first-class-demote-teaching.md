# LISS-0268: struct-first teaching; demote class-as-DTO (de-enterprise OOP)

## Metadata

- Local issue ID: LISS-0268
- GitHub issue: https://github.com/nn0cl/staqex/issues/273
- Status: **complete** (2026-08-02)
- Type: docs + optional ADR note (mostly teaching)
- Priority: P1
- Program: [WP-0088](../work-plans/WP-0088-surface-modernization.md)
- Related: physicist-dx-harmony class reading; destructive sketch class DTO demote

## Intent

Kill the enterprise OOP face of parameter bags:

| Prefer | Avoid as “the” language |
|---|---|
| `struct` / `enum` immutable packs | `class` + `fn init` + `this` for pure data |
| `class` only when holding evolving physical state | mutable Tracker counters in E-lane demos |

Deliverables:

1. Update physicist-dx-harmony / minimal dialect / north star cross-links after 0261
2. B07 rewrite guidance coordinated with LISS-0262
3. Optional: ADR only if new surface sugar (`record` keyword) is desired — default is **teaching + examples**, not new syntax

## Exit

- [x] Teaching table + struct-first paragraph in physicist-dx-harmony
- [x] 0262 B07 aligns (struct geometry + physical-system class)
- [x] No Kernel change

## Non-goals

- Deleting `class` from the language
- Forcing S01 domain rewrite in this Issue (may follow later)
