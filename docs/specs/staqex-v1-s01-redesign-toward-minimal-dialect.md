# S01 redesign sketch — toward the minimal dialect

| Field | Value |
|---|---|
| Status | **Design draft (authorized)** — dialect [Accepted](../architecture/physicist-minimal-dialect.md) 2026-08-02; **`.sqx` / scorecard edits still require a named Issue + phase approval** |
| Date | 2026-08-02 |
| Implementation | **Not approved** by dialect acceptance alone |
| Parent showcase | [LISS-0222](../issues/LISS-0222-s01-quantum-disaster-response.md), [locked scenario](staqex-v1-s01-locked-scenario.md), [scorecard](staqex-v1-s01-coverage-scorecard.md) |
| Companion | [destructive simplification sketch](../architecture/staqex-destructive-simplification-sketch.md) |

```markdown
[DESIGN CHECK]
- Scope: concrete S01 shape against Accepted minimal dialect (E vs H);
  migration map from current tree; Issue-sized slices.
- Not in scope: editing .sqx in this turn; Kernel LINEAR sugar; axiom ADR.
- Constraint: coverage theater must not override dialect honesty (Adjudicator
  chose dialect; scorecard becomes constellation index).
```

## 1. Problem (one line)

S01 teaches Kernel+scorecard survival, not “deployment tension as one honest
Joint experiment.”

## 2. Target tree

```text
examples/showcase/S01_quantum_disaster_response/
  README.md                 # experiment + Host; not “city OS solved”
  main_disaster_response.sqx   # E-lane spine only (rename optional later)
  host/                     # H-lane: Job, ticket, MC, credentials
  domain/                   # classical packs — library, not blackboard
  physics/                  # named Operators / coeffs used by spine
  protocol/ provenance/ grid/  # keep if spine needs; else demote
  # satellites stay but README labels them coverage — not the OS
  main_*.sqx (comms, burst, …)
```

### Spine sentence (must match source)

> Tonight corridor-vs-shelter planning tension as a **small** spin system
> under named constraint Hamiltonians; one terminal plan sample.

If the source cannot be summarized that way, it fails the dialect test.

### Spine rules (binding for a future Issue)

| Rule | Requirement |
|---|---|
| Wires | Prefer 2 (plan pair); avoid growing a kill-list |
| Operators | Named `H_*` from `physics/`; coeffs from structs with physics reading |
| Observation | Sparse `expect`; **zero** `viewed_*` / `inspect` flood |
| Terminal | Single `measure`; document LINEAR leftover gap until `tracing_out` ADR |
| Forbidden on spine | Identity `evolve times`; unmarked soft-only `until`; Float-tag theater |
| Placeability | Soft QPU diags → banner or satellite, not silent “production main” |

### Host rules

- JobResult → TonightTicket remains the structured result path (LISS-0243).
- Ops narrative / logs live in Host — not `inspect` in `.sqx`.
- Vacuum success is not an accepted teaching outcome.

### Coverage rules

- Scorecard = **constellation index** (path → surface), not proof that one
  `main` is an OS.
- Surfaces not needed for the spine sentence → `examples/basics/` or clearly
  labeled S01 satellites.

## 3. Migration map (current → target)

| Current pattern | Target |
|---|---|
| ~20× `inspect` / `viewed_*` in spine | Remove; Host or drop |
| Long `|0>` discharge list | Shrink wire set; residual kill documented as Class E until language help |
| `evolve times 2 { (plan0, plan1) }` | Delete from spine |
| `evolve fuel … until` | Satellite + Non-placeable label, or basics |
| CommandBoard / Float tags driving `main` | Classical `domain/` only; quantum story from `physics/` H |
| QFT / Lindblad / tri-register mains | Satellites; README: coverage, not OS |
| README “Disaster Response OS” tone | “Ops-inspired language experiment” |

## 4. Suggested Issue slices (when implementation is approved)

| Slice | Scope | Notes |
|---|---|---|
| S01-R1 | Docs honesty: README + scorecard constellation wording | **complete** — [LISS-0244](../issues/LISS-0244-s01-r1-dialect-honesty-readme-scorecard.md) |
| S01-R2 | Spine strip: inspect flood, identity evolve, shrink discharge | Feature; dialect gate; **not** approved yet |
| S01-R3 | Physics-named H only; demote Float-tag path from spine | Feature; **not** approved yet |
| S01-R4 | Host ticket regression + seed-0 non-vacuum | Depends on R2 / LISS-0243; **not** approved yet |
| S01-R5 | Relocate coverage rows to basics or labeled satellites | Docs + moves; **not** approved yet |

Do **not** start R2+ without an Issue ID and phase approval.

## 5. Exit criteria (future implementation)

- [x] R1: README / scorecard match constellation honesty ([LISS-0244](../issues/LISS-0244-s01-r1-dialect-honesty-readme-scorecard.md))
- [ ] Spine passes minimal-dialect scoring rule (R2+)
- [ ] Host ticket path non-vacuum or fail-closed (seed 0) — LISS-0243 lineage
- [ ] No new LINEAR / `tracing_out` surface without ADR
- [ ] Critique fatal trio absent from spine (kill ritual flood, inspect/Float flood, OS granularity lie)

## 6. Stop conditions

- Reverting to “full scorecard on one main” → conflicts with Accepted dialect
- Inventing `tracing_out` in S01 without ADR → stop
- Mixing unmarked circuit + Hamiltonian teaching in spine → stop
