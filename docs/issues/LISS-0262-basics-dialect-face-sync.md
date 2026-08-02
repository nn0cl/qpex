# LISS-0262: Basics dialect face sync (de-enterprise first impression)

## Metadata

- Local issue ID: LISS-0262
- GitHub issue: https://github.com/nn0cl/staqex/issues/271
- Status: **complete** (2026-08-02)
- Type: Feature Path (examples)
- Priority: **P0** (first impression)
- Program: [WP-0088](../work-plans/WP-0088-surface-modernization.md)
- Depends: [LISS-0261](LISS-0261-surface-modernization-north-star.md) **complete**
- Paths: `examples/basics/B07_*`, `B08_*`, optionally B01/B02 comments; `examples/basics/README.md`

## Problem

Official basics still teach enterprise / pre-0173 faces:

- **B08:** `inspect` + ritual `state s1 = |0>` before `measure` (contradicts ADR 0173 / dialect)
- **B07:** mutable `Tracker` + classical advance → inspect → measure (OOP theater as “structure”)

First-hour learners meet this before S01.

## Goal

Make B07/B08 (and README pointers) match **Accepted minimal dialect** and north star:

- B08: Operator + evolve + sparse expect + `measure … tracing_out …`; **no** ritual `|0>` teach; **no** inspect museum
- B07: prefer `struct`/`enum` parameter packs; if `class` remains, label as **non-E-lane structure demo** or replace Tracker with immutable segment demo that still exercises visibility without mutable counter theater
- Comments: physics first; avoid Java constructor narrative

## Exit

- [x] B08 uses `tracing_out`; no taught `|0>` kill; no inspect
- [x] B07: struct/enum geometry + `IsingChain` class builds H (no Tracker)
- [x] seed 0 run on B07/B08
- [x] basics + B07/B08 README notes
- [x] Aesthetic: physics-first face (north star §4)

## Non-goals

- New Kernel syntax
- Renaming all `package com.staqex…` (Wave B 0264)
- S01 spine rewrite

## Verification

```bash
python3 -m compiler.staqex run examples/basics/B08_operators_hamiltonians/operators_hamiltonians.sqx --seed 0
python3 -m compiler.staqex run examples/basics/B07_structure_visibility/structure_visibility.sqx --seed 0
```
