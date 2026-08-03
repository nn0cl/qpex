# WP-0089: Surface adoption + sugar (post–WP-0088 language face)

| Field | Value |
|---|---|
| Status | **complete** (2026-08-03) — adoption 0274–0280; ADR 0180–0183 Accepted + Kernel; LISS-0289 face re-sync |
| Purpose | Close the **gap between shipped Kernel levers (WP-0088) and the face of official source**, then land the remaining **modern surface sugars** under one coherent program so adoption and language design stay aligned |
| Motive | Language design re-review (2026-08-02, post–#289): meaning strong; Kernel surface levers shipped; **first impression still half enterprise** because samples do not use 0176–0178, and residual ceremony needs ADR-gated sugar |
| Parents | [surface-modernization north star](../architecture/surface-modernization-north-star.md) (**Accepted**); [minimal dialect](../architecture/physicist-minimal-dialect.md) (**Accepted**); [vision](../architecture/adjudicator-language-vision.md); [axioms](../architecture/staqex-language-axioms.md); [ADR 0095](../architecture/adr/0095-design-horizon-ideal-form-first.md); WP-0088 (**complete**) |
| Predecessor | [WP-0088](WP-0088-surface-modernization.md) — shipped ADRs 0176–0179 + Kernel 0270–0273 |
| Approval | [2026-08-03-wp-0089-plan-approval.md](../collaboration/reviews/2026-08-03-wp-0089-plan-approval.md) |
| Branch | `docs/wp-0089-surface-adoption-and-sugar` (adoption may continue here or split feature/*) |
| Execution | **complete** — adoption + sugar Kernel (#292) + LISS-0289 face re-sync |

```markdown
[DESIGN CHECK]
- Scope: one work plan covering all re-review findings (adoption + docs +
  sugar ADRs + Kernel children + post-sugar re-sync); no second parallel WP.
- Not in scope of this filing: implementation, ADR Accept, Kernel Red, batches.
- Constraint: physicist-first; no axiom rewrite; no Kernel if/while/try;
  machine convenience must not reshape chalk (ADR 0095).
- Consistency rule: every Issue cites this WP; sugar ADRs share the same
  success definition (north star §4 + minimal dialect); sample work must not
  invent surface the Kernel does not yet provide.
```

## 1. Goal (single product outcome)

When an unfamiliar physicist opens **B01–B08**, a thin **S01 spine**, and
**A06**:

1. they see **physics first** (executable chalk), not reverse-DNS packages,
   constructor theaters, or FQN forests;
2. they do **not** think “this is 2010s enterprise Java/Kotlin with kets”;
3. NLTS / `when` / terminal `measure` still read as **law**, not style;
4. multi-file library scale remains honest (packages, `class` for true systems,
   Host ports) without teaching that face as the default notebook.

WP-0088 built the **levers**. This WP **uses them everywhere official**, then
adds only the sugars still required for a modern notebook face.

## 2. Binding language-design policy (do not violate)

| Rule | Source |
|---|---|
| Physicist mental model primary; DX secondary with a physics reading | vision; physicist-dx-harmony |
| Ideal form first; machine convenience never shapes chalk | ADR 0095 |
| NLTS; `when` not `if`; terminal `measure`; no Kernel exceptions/threads | axioms |
| E vs H two-language honesty; Host owns tickets / I/O | minimal dialect |
| `struct`/`enum` default for data; `class` only for true physical systems | harmony; LISS-0268 |
| Writeable ≠ executable (capability fail-closed) | vision §2.1 |
| No gate-DSL-first rewrite of Hamiltonian chalk | vision §4 |
| Phase discipline: ADR Accept → Red → Green; no `main` mutation | agent contract |

### Explicit non-goals (Out)

- Restore Kernel `if` / `while` / bare `for` / `try` / `throw`
- Mid-program collapse or Result-unwrap quantum style
- Live QPU provider SDK / technology selection
- Trait specialization ship (LISS-0196 stays design boundary)
- Force Dirac `⟨φ|ψ⟩` as sole teaching default (Call form remains valid)
- Delete modules, Host ports, or multi-file packages
- Collapse S01 constellation into a single 10-line Ising (dialect violation)
- Second language semantics for “Rust-only” / “Python-only”

## 3. Finding → Issue map (complete coverage)

Re-review items are **all** owned by this WP. No parallel “later WP.”

| Review item | Owner Issue(s) |
|---|---|
| Program success criteria / consistency lock | [LISS-0274](../issues/LISS-0274-wp-0089-program-lock.md) |
| P0-1 Basics experiment-profile adoption (B01–B06, B07 face, B12, eligible singles) | [LISS-0275](../issues/LISS-0275-basics-experiment-profile-adoption.md) |
| P0-2 S01 selective import + `use Enum.*` + spine lane | [LISS-0276](../issues/LISS-0276-s01-import-use-lane-adoption.md) |
| P0-3 S01 domain DTO `class` → `struct` (true systems keep `class`) | [LISS-0277](../issues/LISS-0277-s01-domain-struct-first.md) |
| P0-4 A06 (+ applied face) inspect/package hygiene | [LISS-0278](../issues/LISS-0278-applied-a06-face-sync.md) |
| P1-1 Package root naming (`com.staqex…` → short root) | [LISS-0279](../issues/LISS-0279-package-root-naming-policy.md) |
| P1-2…P1-4 + §5 pedagogy residuals (QUICKSTART, 0175 links, Host split, dual `state`/`State`, interface reading, B09 honesty, ledger refresh) | [LISS-0280](../issues/LISS-0280-pedagogy-docs-and-ledger.md) |
| P2-1 Local type inference | [LISS-0281](../issues/LISS-0281-adr-local-type-inference.md) → [LISS-0282](../issues/LISS-0282-kernel-local-type-inference.md) |
| P2-2 Named struct construction + no mandatory `fn init` on struct | [LISS-0283](../issues/LISS-0283-adr-named-struct-construction.md) → [LISS-0284](../issues/LISS-0284-kernel-named-struct-construction.md) |
| P2-3 Default experiment profile (marker optional for single-file) | [LISS-0285](../issues/LISS-0285-adr-default-experiment-profile.md) → [LISS-0286](../issues/LISS-0286-kernel-default-experiment-profile.md) |
| P2-4 Module-relative import | [LISS-0287](../issues/LISS-0287-adr-module-relative-import.md) → [LISS-0288](../issues/LISS-0288-kernel-module-relative-import.md) |
| P2-5 struct init ceremony (folded into 0283/0284) | LISS-0283 / 0284 |
| §5 residual surface after sugar lands | [LISS-0289](../issues/LISS-0289-post-sugar-face-resync.md) |
| Dual `state` keyword vs `State<T>` note | LISS-0280 (docs); optional clarify in 0281 if inference touches it |
| `-> Unit` / main wrapper noise | 0275 (profile) + 0285/0286 (default) |
| Namespace FQN forests | 0276 + 0279 + selective import |
| Host Python DTO enterprise feel | LISS-0280 (H-lane honesty; no Kernel change) |
| Constellation vs OS narrative residual | Keep constellation; 0276/0277 thin ceremony only — **not** OS deletion |
| Intentional non-problems (LINEAR/`tracing_out`, `when`, soft circuit-in-experiment) | Documented as Keep in LISS-0274; no Issue to “fix” |

## 4. Issue graph (single plan)

| Order | ID | Title | Path type | Depends on | Status |
|---|---|---|---|---|---|
| 0 | [LISS-0274](../issues/LISS-0274-wp-0089-program-lock.md) | Program lock + success criteria (docs) | Architecture / docs | — | **complete** |
| 1 | [LISS-0275](../issues/LISS-0275-basics-experiment-profile-adoption.md) | Basics experiment-profile adoption | Feature examples | 0274 | **complete** |
| 2 | [LISS-0276](../issues/LISS-0276-s01-import-use-lane-adoption.md) | S01 import/use + lane adoption | Feature examples | 0274 | **complete** (spine + morning/day2/lattice/route) |
| 3 | [LISS-0277](../issues/LISS-0277-s01-domain-struct-first.md) | S01 domain struct-first demotion | Feature examples | 0274; pairs with 0276 | **complete** (leaf structs; Type-First/nested stay class) |
| 4 | [LISS-0278](../issues/LISS-0278-applied-a06-face-sync.md) | Applied A06 face sync | Feature examples | 0274 | **complete** |
| 5 | [LISS-0279](../issues/LISS-0279-package-root-naming-policy.md) | Package root naming policy + migration | docs + examples | 0274 | **complete** (`examples.…` root) |
| 6 | [LISS-0280](../issues/LISS-0280-pedagogy-docs-and-ledger.md) | Pedagogy docs + friction ledger | docs | 0274 | **complete** |
| 7 | [LISS-0281](../issues/LISS-0281-adr-local-type-inference.md) | ADR: local type inference | Architecture ADR | 0274 | **Accepted** + Kernel shipped |
| 8 | [LISS-0282](../issues/LISS-0282-kernel-local-type-inference.md) | Kernel: local type inference | Feature Kernel | 0281 **Accepted** | **complete** |
| 9 | [LISS-0283](../issues/LISS-0283-adr-named-struct-construction.md) | ADR: named struct construction | Architecture ADR | 0274 | **Accepted** + Kernel shipped |
| 10 | [LISS-0284](../issues/LISS-0284-kernel-named-struct-construction.md) | Kernel: named struct construction | Feature Kernel | 0283 **Accepted** | **complete** |
| 11 | [LISS-0285](../issues/LISS-0285-adr-default-experiment-profile.md) | ADR: default experiment profile | Architecture ADR | 0274 | **Accepted** + Kernel shipped |
| 12 | [LISS-0286](../issues/LISS-0286-kernel-default-experiment-profile.md) | Kernel: default experiment profile | Feature Kernel | 0285 **Accepted** | **complete** |
| 13 | [LISS-0287](../issues/LISS-0287-adr-module-relative-import.md) | ADR: module-relative import | Architecture ADR | 0274 | **Accepted** + Kernel shipped |
| 14 | [LISS-0288](../issues/LISS-0288-kernel-module-relative-import.md) | Kernel: module-relative import | Feature Kernel | 0287 **Accepted** | **complete** |
| 15 | [LISS-0289](../issues/LISS-0289-post-sugar-face-resync.md) | Post-sugar face re-sync (basics/S01/A06) | Feature examples | 0275–0280; sugars that Accepted+shipped | **complete** |

### Dependency diagram (policy edges only)

```text
0274 program lock
  │
  ├─► 0275 basics adoption ──┐
  ├─► 0276 S01 import/use  ──┤
  ├─► 0277 S01 struct-first ─┼─► (may interleave; no Kernel required)
  ├─► 0278 A06 face          │
  ├─► 0279 package root      │
  ├─► 0280 pedagogy/ledger ──┘
  │
  ├─► 0281 ADR inference ──► 0282 Kernel
  ├─► 0283 ADR named struct ──► 0284 Kernel
  ├─► 0285 ADR default profile ──► 0286 Kernel
  └─► 0287 ADR relative import ──► 0288 Kernel
                    │
                    └─► 0289 post-sugar re-sync (uses whatever has shipped)
```

**Why one WP, not multi-wave WPs:** adoption without sugar, and sugar without
adoption, recreate the post–0088 failure mode (levers exist, face stays old).
One program owns the **end-to-end face**. Dependency edges exist only where
architecture policy requires (ADR Accept before Kernel Red).

**Parallelism (allowed after 0274):** 0275–0280 may run in parallel. ADR drafts
0281/0283/0285/0287 may draft in parallel; each Kernel child waits only on its
own ADR Accept. 0289 waits until at least the adoption set is done and applies
any sugar that has already shipped by then (re-run if later sugars land).

## 5. Granularity rationale

| Choice | Why |
|---|---|
| One WP | Adjudicator asked for a single coherent plan covering all findings |
| 0274 separate | Locks success definition so sample and ADR work cannot diverge |
| Adoption Issues split by tree (basics / S01 import / S01 domain / A06) | Reviewable units; different blast radius; independent merge |
| Docs bundle 0280 | Pedagogy residuals share one verification (links + ledger), not six micro-Issues |
| One ADR + one Kernel child per sugar | Independent Accept/reject; no mega-ADR; Red/Green phase honesty |
| 0289 terminal re-sync | Prevents “Kernel shipped but samples still write old face” a second time |

**Left out of this WP (never or other programs):**

- Live QPU credentials / provider selection
- Trait specialization surface ship
- Continuous PDF Kernel
- CUDA deferred workers
- Display-unit restore (LISS-0197)

## 6. Aesthetic / acceptance ruler (shared)

Every sample or surface PR under this WP **passes** only if:

1. Blackboard H / ket / evolve spelling is unchanged or **shorter**
2. Enterprise markers decrease (`com.…` depth, `Class.Class`, mandatory
   `pub fn main() -> Unit` in teaching singles, DTO `fn init` forests)
3. No new inspect museum / identity evolve / city-OS claim on spines
4. E vs H and circuit lanes stay honest (lane markers where required)
5. SV / seed-0 examples still run where claimed
6. No axiom or ADR 0095 violation

A PR **fails** if it only renames for fashion, lengthens chalk for the
compiler, or implements sugar without an Accepted ADR.

## 7. Recommended execution order (single queue)

Not a multi-WP stage gate — a **dependency-respecting queue inside WP-0089**:

1. **LISS-0274** — Accept program lock (docs)
2. **LISS-0275, 0276, 0277, 0278, 0279, 0280** — adoption + docs (Kernel-ready
   features only: 0176–0178 already on main)
3. **LISS-0281, 0283, 0285, 0287** — ADR drafts → Adjudicator Accept each
4. **LISS-0282, 0284, 0286, 0288** — Kernel Red→Green→Refactor per Accept
5. **LISS-0289** — re-sync official faces to shipped sugars

## 8. Current next Issue

| Field | Value |
|---|---|
| Issue | **none** — WP-0089 **complete** (LISS-0289 face re-sync 2026-08-03) |
| Unblocked | Program closed; further surface work needs a new WP or ad-hoc Issue |
| Adjudicator needed | Merge LISS-0289 PR; optional post_review |
| Post-WP residuals (ad-hoc) | LISS-0290…0299: surface sugars, free-fn Kernel, showcase/applied face; **0299** residual selective import + bare-pipe transitive link (**complete** 2026-08-03) |

## 9. Risks

| Risk | Mitigation |
|---|---|
| Sample churn races sugar ADRs | Adoption uses **only shipped** 0176–0179; 0289 re-applies later sugars |
| Package rename breaks multi-file imports | 0279 is policy + mechanical migration with SV; no silent path breaks |
| Type inference mis-classifies State vs Classical | 0281 must define fail-closed rules; Red tests before Green |
| Struct demotion breaks S01 methods | 0277 keeps `class` for true systems; methods on struct only if already value-like pure fns / free fns |
| Scope creep into QPU/traits | Explicit Out list; hard stop if mid-work design appears |

## 10. Verification plan (program-level)

- Per-Issue exit checklists
- Seed-0 runs for touched `.sqx`
- `python3 tests/spec_verification/run_all.py` when Kernel or contract docs change
- Named pytest for each Kernel sugar Issue
- Aesthetic spot-check: B01, B08, S01 spine first screenful, A06 main
- Friction ledger section dated post–WP-0089

## 11. Approval model (reminder)

| Approval | Authorizes |
|---|---|
| Plan approval (this WP) | Investigation complete; Issues exist; **not** Red/Green |
| ADR Accept (0281/0283/0285/0287 each) | Architecture decision only |
| Phase / Implementation / batch | Kernel or sample execution as named |

Filing this WP does **not** authorize implementation.
