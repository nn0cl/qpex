# S01 redesign sketch — toward the minimal dialect

| Field | Value |
|---|---|
| Status | **Design draft (authorized)** — dialect [Accepted](../architecture/physicist-minimal-dialect.md) 2026-08-02; **adjusted 2026-08-02** for expressiveness-first scenario expansion ([LISS-0245](../issues/LISS-0245-s01-expressiveness-review-scenario-expansion.md)); **`.sqx` / scenario-lock edits still require named Issue + phase approval** |
| Date | 2026-08-02 |
| Implementation | **Not approved** by dialect acceptance alone |
| Parent showcase | [LISS-0222](../issues/LISS-0222-s01-quantum-disaster-response.md), [locked scenario](staqex-v1-s01-locked-scenario.md), [scorecard](staqex-v1-s01-coverage-scorecard.md) |
| Expressiveness Issue | **[LISS-0245](../issues/LISS-0245-s01-expressiveness-review-scenario-expansion.md)** — full A+B coverage; expand scenario when cramped |
| R1 honesty | [LISS-0244](../issues/LISS-0244-s01-r1-dialect-honesty-readme-scorecard.md) (**complete**) |
| Companion | [destructive simplification sketch](../architecture/staqex-destructive-simplification-sketch.md) (language horizon only; not S01 deletion authority) |

```markdown
[DESIGN CHECK]
- Scope: concrete S01 shape against Accepted minimal dialect (E vs H) **and**
  LISS-0245 expressiveness obligation (full pattern coverage via scenario seats).
- Not in scope: editing .sqx in this turn without phase approval; Kernel LINEAR
  sugar; axiom ADR.
- Constraint: spine stays dialect-honest; scorecard rows are **not** dropped to
  clean the tree — weak seats → expand locked scenario (LISS-0245), not demote
  to basics by default.
```

## 1. Problem (two lines)

S01 must serve **language design + expressiveness review** (all shipped surfaces
in a coherent disaster story). Today it often teaches Kernel+scorecard survival
instead: either a crowded spine or orphan mains without scenario seats.

## 1.1 Binding product rule (LISS-0245)

| Rule | Meaning |
|---|---|
| Full coverage | Scorecard **A+B** remains in the S01 **constellation** |
| Scenario first | If a surface feels theatrical, **expand/refine the locked scenario** so it has an ops/physics role |
| Spine honesty | Tonight **E-lane** spine still obeys minimal dialect (no inspect museum, no identity evolve) |
| Not the goal | Deleting surfaces or dumping them to `examples/basics/` to reduce noise (basics-only needs Adjudicator demotion) |

## 2. Target tree

```text
examples/showcase/S01_quantum_disaster_response/
  README.md                 # constellation map: spine + scenario chapters
  main_disaster_response.sqx   # E-lane spine (dialect-honest Joint experiment)
  host/                     # H-lane: Job, ticket, MC, credentials (scenario “OS shell”)
  domain/                   # classical packs justified by scenario objects
  physics/                  # named Operators / coeffs used by spine or chapters
  protocol/ provenance/ grid/
  main_*.sqx                # scenario chapters (comms, burst, lattice, …)
                            # each must cite a locked-scenario paragraph
```

### Spine sentence (must match source)

> Tonight corridor-vs-shelter planning tension as a **small** spin system
> under named constraint Hamiltonians; one terminal plan sample.

If the spine source cannot be summarized that way, it fails the dialect test.
**Other surfaces live in constellation chapters**, each with a scenario seat —
not in an `inspect` flood on the spine.

### Spine rules (binding for implementation Issues)

| Rule | Requirement |
|---|---|
| Wires | Prefer 2 (plan pair); avoid growing a kill-list |
| Operators | Named `H_*` from `physics/`; coeffs from structs with physics reading |
| Observation | Sparse `expect`; **zero** `viewed_*` / `inspect` flood on spine |
| Terminal | Single `measure`; document LINEAR leftover gap until language help / ADR |
| Forbidden on spine | Identity `evolve times`; unmarked soft-only `until` as “production”; Float-tag theater |
| Placeability | Soft QPU diags → labeled chapter or banner, not silent success |

### Host rules

- JobResult → TonightTicket remains the structured result path (LISS-0243).
- Ops narrative / logs live in Host — not `inspect` museums in `.sqx`.
- Vacuum success is not an accepted teaching outcome.

### Coverage / constellation rules

- Scorecard = **constellation index** (path → surface → **scenario seat**).
- One `main` is not “the whole OS”; the **tree + Host** is the OS exhibit.
- Surfaces not on the spine sentence → **S01 scenario chapters** (preferred)
  with locked-scenario prose, **or** Adjudicator-approved demotion.
- Default fix for cramming: **expand scenario** (LISS-0245), not delete row.

## 3. Migration map (current → target)

| Current pattern | Target |
|---|---|
| ~20× `inspect` / `viewed_*` in spine | Remove from spine; Host ticket / sparse `expect`; do not reintroduce as scorecard glue |
| Long `|0>` discharge list | Shrink spine wire set; residual kill documented; language gap tracked separately |
| `evolve times 2 { (plan0, plan1) }` | Delete unless scenario gives it a real replan-tick meaning |
| `evolve fuel … until` | **Scenario chapter** (fuel search) + non-placeable QPU label — not orphan |
| CommandBoard / Float tags driving `main` | Classical `domain/` only if scenario objects need them; quantum story from `physics/` H on spine |
| QFT / Lindblad / tri-register mains | **Scenario chapters** with locked seats (spectrum sensing, noisy channel, multi-command registers) — not unlabeled coverage orphans |
| README tone | Language-expressiveness showcase on a reality-first ops story; honesty preserved (R1 done) |

## 4. Issue slices

| Slice | Scope | Issue / notes |
|---|---|---|
| S01-R1 | README + scorecard constellation honesty | **complete** — [LISS-0244](../issues/LISS-0244-s01-r1-dialect-honesty-readme-scorecard.md) |
| S01-E0 | Expressiveness inventory + scenario expansion draft + language-design findings | **review-complete** — [LISS-0245](../issues/LISS-0245-s01-expressiveness-review-scenario-expansion.md) / [review](../collaboration/reviews/2026-08-02-s01-expressiveness-scenario-review.md); triage pending |
| S01-E1 | Accept/amend locked scenario for new seats | Docs; after E0 triage |
| S01-R2 | Spine dialect pass (inspect flood, identity evolve, discharge) | **complete** — [LISS-0246](../issues/LISS-0246-s01-r2-spine-dialect-pass.md) |
| S01-R3 | Align chapters to scenario seats (rename/split mains OK) | Feature; **keep all A+B paths** |
| S01-R4 | Host ticket regression + seed-0 non-vacuum | LISS-0243 + R2 |
| S01-R5 | ~~Relocate coverage to basics by default~~ | **Superseded policy** — use LISS-0245 expand-scenario; basics-only only with Adjudicator demotion |

Do **not** start R2+ source edits without Issue ID and phase approval.
Do **not** use R-slices to drop scorecard rows.

## 5. Exit criteria (implementation wave)

- [x] R1: README / scorecard constellation honesty ([LISS-0244](../issues/LISS-0244-s01-r1-dialect-honesty-readme-scorecard.md))
- [x] LISS-0245 review inventory complete and triaged — **inventory complete**; triage pending Adjudicator
- [ ] Locked scenario carries seats for retained constellation chapters
- [x] Spine passes minimal-dialect scoring rule (R2 — [LISS-0246](../issues/LISS-0246-s01-r2-spine-dialect-pass.md))
- [ ] Host ticket path non-vacuum or fail-closed (seed 0) when LISS-0243 in scope
- [ ] No scorecard A+B row removed without Adjudicator demotion
- [ ] No new LINEAR / `tracing_out` surface without ADR

## 6. Stop conditions

- Dropping scorecard surfaces “to satisfy minimal dialect” without LISS-0245 triage → stop
- Stuffing full scorecard back onto **one** spine `main` → conflicts with dialect
- Inventing `tracing_out` in S01 without ADR → stop
- Mixing unmarked circuit + Hamiltonian teaching **on the spine** → stop (chapters may be circuit-lane if scenario seat is sensing/QFT)
