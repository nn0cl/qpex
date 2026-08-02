# LISS-0275: Basics experiment-profile adoption

## Metadata

- Local issue ID: LISS-0275
- GitHub issue: _(none yet)_
- Status: **proposed**
- Phase: Feature examples (no new Kernel)
- Type: Feature Path
- Priority: P0 (first impression)
- Program: [WP-0089](../work-plans/WP-0089-surface-adoption-and-sugar.md)
- Depends: [LISS-0274](LISS-0274-wp-0089-program-lock.md); Kernel ADR 0176 already shipped
- Paths: `examples/basics/B01_*`…`B08_*`, eligible singles `B12_*`, `examples/basics/README.md`
- Not primary: multi-file `B09_*` (keep packages; document honesty — see also LISS-0279/0280)

## Summary

Convert eligible **single-file** basics from `package com.staqex…` +
`pub fn main() -> Unit` to `// staqex-profile: experiment` bare body (as B08).
Modernize B07 face (reduce FQN noise within profile constraints). Leave B09 as
multi-file package teaching with an honesty note that notebook default is profile.

## Problem

Only B08 uses the experiment profile. Learners open B01–B07 and still see JVM
ceremony → “real Staqex is enterprise.”

## Exit

- [ ] B01–B06, B12 (and other single-file basics that need no cross-package export)
      use experiment profile or documented exception
- [ ] B07: physics-first; shorter names where possible; no Tracker regression
- [ ] B08 remains north-star; not regressed
- [ ] B09 README: multi-file packages vs notebook profile honesty
- [ ] seed-0 run on touched mains
- [ ] Aesthetic pass (north star §4)

## Non-goals

- New Kernel syntax
- Package root global rename (LISS-0279)
- Type inference (LISS-0281+)

## Verification

```bash
python3 -m compiler.staqex run examples/basics/B01_never_leave_the_state/never_leave_the_state.sqx --seed 0
python3 -m compiler.staqex run examples/basics/B08_operators_hamiltonians/operators_hamiltonians.sqx --seed 0
# + other touched paths
```
