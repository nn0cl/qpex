# LISS-0289: Post-sugar face re-sync (basics / S01 / A06)

## Metadata

- Local issue ID: LISS-0289
- GitHub issue: _(none yet)_
- Status: **proposed**
- Phase: Feature examples
- Type: Feature Path
- Priority: P0 (program closure)
- Program: [WP-0089](../work-plans/WP-0089-surface-adoption-and-sugar.md)
- Depends: [LISS-0275](LISS-0275-basics-experiment-profile-adoption.md)–[LISS-0280](LISS-0280-pedagogy-docs-and-ledger.md);
  plus any of [LISS-0282](LISS-0282-kernel-local-type-inference.md) /
  [LISS-0284](LISS-0284-kernel-named-struct-construction.md) /
  [LISS-0286](LISS-0286-kernel-default-experiment-profile.md) /
  [LISS-0288](LISS-0288-kernel-module-relative-import.md) that have **shipped**
  by the time this Issue runs (apply what exists; do not wait for rejected ADRs)

## Summary

Terminal consistency pass: re-apply official faces to **all shipped** WP-0089
sugars so the program does not end with Kernel levers unused a second time
(the post–WP-0088 failure mode).

## Exit

- [ ] B01/B08 (and basics) use inference / default profile / named structs **if shipped**
- [ ] S01 spine uses relative import / named structs **if shipped**
- [ ] A06 updated similarly where multi-file allows
- [ ] Aesthetic scorecard pass on B01, B08, S01 first screen, A06
- [ ] seed-0 + SV green
- [ ] WP-0089 status → complete only after this Issue (or explicit Adjudicator waiver)

## Non-goals

- Implementing unaccepted ADRs
- Expanding scope outside WP-0089 Out list

## Verification

- North star §4 checklist signed in PR
- Before/after snippet in PR body for B08 and S01 spine
