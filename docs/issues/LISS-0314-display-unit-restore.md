# LISS-0314: Display-unit restore after canonical promote

## Metadata

- Local issue ID: LISS-0314
- Status: **complete** (2026-08-03)
- Type: Feature Kernel units
- Priority: P3 residual (reopen LISS-0197)
- Depends: [ADR 0186](../architecture/adr/0186-display-unit-restore.md) **Accepted**;
  ADR 0155 promote shipped
- Branch: `feature/liss-0314-display-unit-restore`
- Supersedes deferral: [LISS-0197](LISS-0197-display-unit-restore-deferred.md)

## Problem

Mixed-unit promote leaves results in the canonical unit. Notebook chalk often
wants the LHS unit after `a + b`.

## Acceptance

```text
When Mass x = 1.0.g + 1.0.kg
Then x magnitude is 1001.0 and unit is g

When Mass x = 1.0.kg + 1.0.g
Then x magnitude is 1.001 and unit is kg

When same-unit or explicit `to` paths run
Then behavior stays ADR 0155 / 0124 compliant
```

## Exit

- [x] dimensions + evaluator + typecheck
- [x] Red suite + update promote tests for affine LHS
- [x] LISS-0197 marked superseded/complete
- [x] Trace
