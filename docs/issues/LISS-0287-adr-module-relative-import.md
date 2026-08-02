# LISS-0287: ADR — module-relative import

## Metadata

- Local issue ID: LISS-0287
- GitHub issue: _(none yet)_
- Status: **proposed** (ADR 0183 draft filed 2026-08-03)
- Phase: Architecture Path (ADR draft → Accept)
- Type: Architecture ADR
- Priority: P2
- Program: [WP-0089](../work-plans/WP-0089-surface-adoption-and-sugar.md)
- Depends: [LISS-0274](LISS-0274-wp-0089-program-lock.md); complements ADR 0177
- Blocks: [LISS-0288](LISS-0288-kernel-module-relative-import.md)

## Summary

Decide relative / short module imports so multi-file demos need not repeat full
roots on every line:

```text
import .domain.{CommandBoard, OpsPhase}   // illustrative
```

Absolute imports and selective `{A,B}` remain valid. No wildcard deep-tree
imports that hide physics dependencies in official samples without review.

## Decision questions

1. Syntax: `.path`, `./path`, `package-relative` only?
2. Resolution rules vs package declaration
3. Interaction with default experiment package `staqex.experiment`
4. Style guide: when relative is preferred in official samples

## Exit

- [ ] ADR Accept
- [ ] No change to visibility / `pub` rules

## Policy guard

- Dependencies stay visible (no silent prelude of entire domain trees)
