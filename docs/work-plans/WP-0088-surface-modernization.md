# WP-0088: Surface modernization (de-enterprise look, physicist-first)

| Field | Value |
|---|---|
| Status | **approved for Wave A + Wave B ADR drafting** (2026-08-02 Adjudicator「承認・起票」); Wave C Kernel Red only after each Wave B ADR Accept |
| Purpose | Modernize Staqex **surface ceremony** so the language no longer reads as 2010s Java/Kotlin enterprise, without violating axioms, NLTS, or Adjudicator vision |
| North star | [surface-modernization-north-star.md](../architecture/surface-modernization-north-star.md) (**Accepted**) |
| Approval record | [2026-08-02-wp-0088-approval.md](../collaboration/reviews/2026-08-02-wp-0088-approval.md) |
| Parents | [minimal dialect](../architecture/physicist-minimal-dialect.md) (**Accepted**); language design re-review 2026-08-02 (L-01…L-27) |
| Out | Kernel `if`/`while`/exceptions; live QPU; scorecard row deletion; axiom rewrites |
| Branch (docs intake) | `docs/wp-0088-surface-modernization-plan` |
| Execution | per-Issue or future `batch/wp-0088-…` after Adjudicator approval |

## Personal / product target (explicit)

> 表面の「見た目」は 2010 年代の Java/Kotlin エンタープライズ寄り  
> → **払拭する**

Success is emotional and pedagogical: **executable chalk**, not enterprise Kotlin
with kets. Physics spelling stays primary.

## Operating constraints (binding)

1. Physicist mental model **primary**; programmer DX secondary ([vision](../architecture/adjudicator-language-vision.md)).
2. Ideal form first ([ADR 0095](../architecture/adr/0095-design-horizon-ideal-form-first.md)) — do not shorten chalk by forbidding physics.
3. NLTS / `when` / terminal `measure` / no Kernel exceptions or threads.
4. Sample policy: no inspect museum, no identity `evolve times`, no city-OS claim on spines.
5. Phase discipline: docs/ADR before Kernel; Red before Green; no `main` mutation.

## Issue rows

| Order | ID | Wave | Title | Path type | Status |
|---|---|---|---|---|---|
| 0 | [LISS-0261](../issues/LISS-0261-surface-modernization-north-star.md) | 0 | Accept/revise surface modernization north star | Architecture / docs | **complete** |
| 1 | [LISS-0262](../issues/LISS-0262-basics-dialect-face-sync.md) | A | Basics dialect face sync (B07/B08 + north-star samples) | Feature examples | **complete** |
| 2 | [LISS-0263](../issues/LISS-0263-spec-kotlin-like-wording.md) | A | Spec/vision wording: Kotlin-like DX is secondary | docs | **complete** |
| 3 | [LISS-0264](../issues/LISS-0264-adr-experiment-surface-profile.md) | B | ADR 0176 experiment surface profile | Architecture ADR | **Proposed — Accept pending** |
| 4 | [LISS-0265](../issues/LISS-0265-adr-import-use-ergonomics.md) | B | ADR 0177 import/use ergonomics | Architecture ADR | **Proposed — Accept pending** |
| 5 | [LISS-0266](../issues/LISS-0266-adr-lane-annotation.md) | B | ADR 0178 lane annotation | Architecture ADR | **Proposed — Accept pending** |
| 6 | [LISS-0267](../issues/LISS-0267-adr-classical-call-in-expr.md) | B | ADR 0179 classical Call in expr | Architecture ADR | **Proposed — Accept pending** |
| 7 | [LISS-0268](../issues/LISS-0268-struct-first-class-demote-teaching.md) | A+B | struct-first teaching + class demotion (docs; optional ADR sugar) | docs / optional ADR | **complete** |
| 8 | [LISS-0269](../issues/LISS-0269-kernel-wave-b-green-followups.md) | C | Kernel Green follow-ups for Accepted Wave B ADRs (placeholder umbrella) | Feature Kernel — **only after** B Accept | **open — blocked on B Accept** |

## Execution order

```text
0261 north star Accept ──► gates aesthetic scoring for all later PRs
        │
        ├─► Wave A (parallel OK after 0261 or with 0261 if Adjudicator allows):
        │     0262 basics face    0263 wording    0268 struct-first teaching
        │
        └─► Wave B ADRs (Architecture Path; order recommended):
              0264 experiment profile (largest de-enterprise hit)
              0265 import/use
              0266 lane annotation
              0267 classical call in expr
              then 0269 Kernel Green per accepted ADR (split Issues as needed)
```

**Rationale:** Learners meet basics first (A). Enterprise feel is mostly
**package / FQN / class init / main wrapper** → 0264–0265 first among ADRs.
Lane markers (0266) prevent “one language soup.” Classical expr (0267) is
independent DX and can parallelize after 0261.

## Granularity rationale

| Split | Why |
|---|---|
| North star separate | Aesthetic criteria need Adjudicator Accept before mass sample churn |
| Wave A vs B | Samples must not wait on ADR; ADRs must not pretend samples alone fix Kernel |
| One ADR per concern | Independent Accept/reject; no mega-ADR |
| 0269 umbrella | Avoid inventing Kernel Issues before Accept; split when B lands |

**Left out of this WP (later or never):**

- Dirac paper sugar policy (already dual-accept; style guide only)
- Full effect system / generic programming expansion
- Live QPU provider
- Reopening `if` / exceptions

## Enterprise markers → Issue map

| Enterprise marker | Mitigation |
|---|---|
| `package com.staqex.examples.…` | 0264 profile + 0262 shorter paths where legal |
| `Foo.Bar.Baz` FQN everywhere | 0265 import/use; 0262 samples |
| `class` + `fn init` + `this` for bags | 0268 teaching; optional record sugar in 0264/0268 |
| `pub fn main() -> Unit` as only face | 0264 experiment profile (wrapper optional / elided in teaching) |
| Tracker-style mutable OOP | 0262/0268 demote from E-lane teaching |
| Unmarked multi-lane soup | 0266 |

## Verification (program)

Wave A:

```bash
# After 0262
python3 -m compiler.staqex run examples/basics/B08_operators_hamiltonians/operators_hamiltonians.sqx --seed 0
python3 -m compiler.staqex run examples/basics/B01_never_leave_the_state/never_leave_the_state.sqx --seed 0
# B08 must use tracing_out (no ritual |0> teach); no inspect museum
```

Wave B/C: per ADR + SV / pytest named in follow-up Issues.

Aesthetic: north star §4 scorecard on any sample PR.

## Approval model

| Step | Approval |
|---|---|
| This WP + Issues + north star file | Scope / planning |
| LISS-0261 | Architecture Accept of north star (or amend) |
| Wave A Issues | Plan / Feature per agent family |
| Wave B ADRs | Architecture Accept each |
| Wave C Kernel | Phase / Implementation after each Accept |

**Planning files do not authorize Kernel Red/Green.**

## Success definition

1. Official basics **look like minimal dialect**, not enterprise entry points.
2. Spec/docs no longer imply “Kotlin-like” is co-equal with physicist spelling.
3. At least one Accepted ADR that **materially shortens** experiment ceremony
   (package and/or import), **or** explicit Adjudicator reject with alternate.
4. Adjudicator can honestly say: surface no longer reads as 2010s enterprise
   Kotlin-with-kets (subjective gate on 0261 scorecard).
