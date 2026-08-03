# LISS-0289: Post-sugar face re-sync (basics / S01 / A06)

## Metadata

- Local issue ID: LISS-0289
- GitHub issue: _(none yet)_
- Status: **complete** — 2026-08-03
- Phase: Feature examples
- Type: Feature Path
- Priority: P0 (program closure)
- Program: [WP-0089](../work-plans/WP-0089-surface-adoption-and-sugar.md)
- Branch: `feature/liss-0289-post-sugar-face-resync`
- Depends: [LISS-0275](LISS-0275-basics-experiment-profile-adoption.md)–[LISS-0280](LISS-0280-pedagogy-docs-and-ledger.md);
  shipped sugars [LISS-0282](LISS-0282-kernel-local-type-inference.md) /
  [LISS-0284](LISS-0284-kernel-named-struct-construction.md) /
  [LISS-0286](LISS-0286-kernel-default-experiment-profile.md) /
  [LISS-0288](LISS-0288-kernel-module-relative-import.md)

## Summary

Terminal consistency pass: re-apply official faces to **all shipped** WP-0089
sugars so the program does not end with Kernel levers unused a second time
(the post–WP-0088 failure mode).

## Exit

- [x] B01/B08 (and basics) use inference / default profile / named structs **if shipped**
  - B01: `answer = dirac(42)` (0180)
  - B08: `J`/`h`/`H_chain` inferred (0180)
  - B07: named `Segment { … }` (0181)
  - B09: `import .domain…` / `.operators…` (0183)
- [x] S01 spine: relative import + named leaf structs (0181/0183); chalk Floats stay typed
  (Call-result bare infer still misbinds — keep `Float` annotations)
- [x] A06: relative import + named `ChainLattice` / `SSHParams`
- [x] Aesthetic scorecard pass on B01, B08, S01 first screen, A06
- [x] seed-0 + SV green (161/161; sugar pytest 5 passed)
- [x] WP-0089 status → complete

## Non-goals

- Implementing unaccepted ADRs
- Expanding scope outside WP-0089 Out list
- Stripping Type-First pedagogy annotations (B06)
- Bare infer for classical Call results / object ctors (Kernel gap; keep typed)

## Verification

- North star §4 checklist: H/ket/evolve shorter or unchanged; enterprise markers down
- Before/after: B08 lost `Float`/`Operator` noise; S01 uses `import .domain…` + `{ field: }`
- Trace: `docs/collaboration/traces/2026-08-03-liss-0289-post-sugar-face-resync.md`
