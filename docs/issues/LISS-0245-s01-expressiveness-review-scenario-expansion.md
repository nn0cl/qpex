# LISS-0245: S01 language-design & expressiveness review (full pattern coverage via scenario expansion)

## Metadata

- Local issue ID: LISS-0245
- Status: **open** (docs intake 2026-08-02)
- Type: Architecture Path → design review (`.sqx` edits only after scenario lock + phase approval)
- Priority: P1
- Parent showcase: [LISS-0222](LISS-0222-s01-quantum-disaster-response.md)
- Prior reviews:
  - [LISS-0223](LISS-0223-s01-language-physicist-review.md) — beauty × cognitive load (**complete**)
  - [LISS-0244](LISS-0244-s01-r1-dialect-honesty-readme-scorecard.md) — README/scorecard constellation honesty (**complete**)
- Pedagogy law: [physicist-minimal-dialect](../architecture/physicist-minimal-dialect.md) (**Accepted**)
- Redesign companion: [S01 redesign sketch](../specs/staqex-v1-s01-redesign-toward-minimal-dialect.md)
- Scenario lock: [staqex-v1-s01-locked-scenario.md](../specs/staqex-v1-s01-locked-scenario.md)
- Scorecard: [staqex-v1-s01-coverage-scorecard.md](../specs/staqex-v1-s01-coverage-scorecard.md)
- Related Host: [LISS-0243](LISS-0243-s01-tonight-job-result-export.md) (structured JobResult / ticket; separate)
- Branch (suggested): `docs/liss-0245-s01-expressiveness-scenario` or current docs redesign branch until split
- Implementation permission: **no** for `.sqx` until Adjudicator accepts (1) review record and (2) scenario-lock deltas

## Purpose (primary)

**Not** “make examples prettier by dropping surfaces.”

1. **Language design review** — does syntax, layering, OOP, lanes, and the result boundary still match Adjudicator vision and axioms when the full shipped surface set is exercised?
2. **Language expressiveness review** — can those surfaces carry a coherent, reality-first ops story without Class E habits that teach the wrong lesson?

### Coverage obligation

Every pattern in scorecard **A+B** (plus any extra shipped surface the review elects to add) must remain in the **S01 constellation** with an evidence path.

### Remedy when cramped or theatrical

**Expand or refine the locked scenario** so the surface has an honest ops/physics seat.

Do **not** default to:

- deleting scorecard rows,
- unlabeled “coverage only” orphans,
- dumping to `examples/basics/` (basics-only requires explicit Adjudicator demotion).

### Product rule (one line)

> Full expressiveness inventory first; scenario grows until each surface has a
> legitimate narrative seat; spine stays dialect-honest (minimal dialect).

## Relationship to other artifacts

| Artifact | Relationship |
|---|---|
| LISS-0223 | Prior beauty/load findings are input. This Issue **reframes**: full expressiveness + scenario expansion as first-class fix (not thin-only). |
| LISS-0244 (R1) | Docs honesty / constellation wording already landed. This Issue **fills seats** under that constellation. |
| Minimal dialect | Gates **spine** pedagogy only. Does **not** authorize dropping scorecard rows. |
| Redesign sketch | Prefer scenario expansion over “relocate coverage to basics.” Chapters = scenario seats, not orphans. |
| LISS-0243 | Host structured results (result-boundary expressiveness). Separate implementation track. |
| Scorecard A+B | Normative inventory. Blank evidence = fail. Theater without scenario seat = fail until scenario expanded. |

## Non-goals

- Axiom changes without ADR
- Live QPU SDK / technology selection
- “Shrink scorecard” or “spine-only showcase” as the *goal*
- Using Host Python as a substitute for language expressiveness (H-lane still needs scenario seats)
- Treating destructive-simplification sketch as automatic S01 surface deletion authority

## Work products (order)

### Phase 0 — Design review (closeable on docs if Adjudicator rules so)

1. **Expressiveness inventory** — review file under `docs/collaboration/reviews/`  
   One row per scorecard A+B surface (extend if needed):

   | Surface | Current path(s) | Scenario seat today (Y/weak/N) | Proposed seat if expand | Lane (E/H/circuit/open) | Language-design note | Expressiveness note | Class A/B/C/E | Action |

   **Action** ∈  
   `keep` | `relocate-within-S01` | `expand-scenario` | `split-main` | `host-only` | `needs-ADR` | `basics-only-with-approval`

2. **Scenario expansion draft** against locked scenario  
   For each `expand-scenario`: who / when / ops or physics object / Joint or Host job.

3. **Spine vs constellation map**  
   - Spine (E-lane): one dialect-honest Joint sentence.  
   - Constellation: all other S01 mains/modules as **named scenario chapters**.  
   - No chapter without locked-scenario prose.

4. **Language design findings** (ranked)  
   Separate forced language costs (LINEAR kill list, vacuum envelopes, unit loss on fields, package noise, dual `+`, lane split) from pure sample debt.

5. **Stop for Adjudicator**  
   Accept/amend scenario; authorize follow-up Feature Issues; forbid silent demotions.

### Phase 1+ — After approval (Feature Issues or batch)

- Update locked scenario.
- Align README / scorecard “scenario seat” notes.
- Edit `.sqx` / `host/` so paths match seats (no identity `evolve` without story; no inspect museum on spine; chapters earn their main).
- Do not remove a scorecard row without demotion approval.

## Scorecard inventory seed (all rows required in the table)

### A — Required

`when`; named Float/struct → Operator; `expect`/`inspect`; typed `state`; multi-file import; NLTS+`measure`; ket + `evolve for/times`; Operator+Suzuki; OOP+visibility; LINEAR; Ports; fail-closed.

### B — Shipped extensions

`sum`/`product`+`Index`; `Basis<N>`; `inner`/`outer`; `evolve … until`; phase/interference; Type-First+SI; pipe/Partial/poly Fusion; Trace-Out fn; Lindblad; QFT/cqft apply; Host Job/Credential/MC; multi-register; `impl` dispatch; Classical⊕State.

Review may **add** rows (e.g. register `forEach`, soft QPU honesty, ticket export) but must not silently drop A/B.

## Scenario expansion principles

1. Name the **ops/physics object**.  
2. Name the **phase** (Tonight / Morning / Day-2 / Host job).  
3. Name the **lane** (E / H / circuit / open).  
4. If it cannot be named without lying → `needs-ADR` or Adjudicator `basics-only` — not fake Float tags.

### Illustrative seats (draft — not locked)

| Cluster | Possible seat |
|---|---|
| Lindblad / density | Intermittent tower / noisy order channel |
| QFT / burst | RF or sensor burst spectrum under outage |
| multi-register | Rescue × logistics × fire command with coupling as contention |
| Index / Basis lattice | District damage / flood-zone field |
| interference | Competing corridor phases |
| `evolve until` | Fuel/resource search under convergence budget (label non-placeable QPU) |
| Type-First SI | Typed stocks/windows/current/temperature (not Float-tag only) |
| pipe / Partial / Fusion | Priority composition for dispatch order |
| `impl` | Capability protocols (rescue vs haul) |
| Classical⊕State ration | Fair-share tickets in allocation mixture |
| Host MC / Credential / Job | Demand inject; agency share; rolling replan (“OS shell”) |
| `inner`/`outer` | Plan prior vs proposal fidelity |
| LINEAR + terminal `measure` | One executable plan sample per window |

## Exit criteria

### Review phase

- [ ] Review record with **complete A+B inventory** (no blank rows)
- [ ] Every row has Action; every `expand-scenario` has draft prose
- [ ] Spine vs constellation map; minimal-dialect spine sentence stated
- [ ] Language-design findings ranked (A/B/C separate from pure E)
- [ ] Adjudicator triage recorded

### Implementation phase (follow-ups)

- [ ] Locked scenario updated for accepted seats
- [ ] Sources/README/scorecard paths match seats
- [ ] No A+B row removed without demotion
- [ ] Spine still passes minimal dialect (no inspect museum / identity evolve / OS lie on spine sentence)
- [ ] Soft/non-placeable surfaces labeled in scenario + README

## Process

1. Architecture Path; `[DESIGN CHECK]` at start.
2. Docs-only until phase approval for `.sqx`.
3. No mutations on `main`.
4. Stop on implied axiom/new measure sugar → ADR.
5. Prefer docs review PR, then Feature Issue(s) for source.

## Agent prompt payload

```text
Execute LISS-0245 Phase 0 only (unless Adjudicator expanded approval):
- Purpose: language design review + expressiveness review of Staqex via S01.
- Obligation: full scorecard A+B coverage; do NOT drop surfaces to clean up.
- If a pattern is cramped or theatrical: propose locked-scenario expansion so it
  has an honest ops/physics seat (constellation chapters OK; spine stays
  minimal-dialect honest).
- Deliver: docs/collaboration/reviews/<date>-s01-expressiveness-scenario-review.md
  with inventory table, scenario expansion draft, spine/constellation map,
  ranked language-design findings (A/B/C/E).
- Out: Kernel code, live QPU, scorecard row deletion, axiom changes.
- Inputs: LISS-0223, LISS-0244 R1, minimal dialect, scorecard, locked scenario, S01 tree.
```

## Completion report template

```markdown
## Summary
- Inventory rows complete:
- expand-scenario count:
- language-design P0 findings:

## Artifacts
- review path:
- scenario draft:

## Adjudicator decisions needed
-

## Follow-up Feature Issues
-
```

## Dependencies

- Input: LISS-0223, LISS-0244 (R1 complete).
- Soft: minimal dialect Accepted.
- Parallel OK: LISS-0243.
- Blocks implementation: Adjudicator acceptance of scenario deltas.

## Priority rationale

S01 is the flagship language-spec / expressiveness exhibit. Cognitive-load cleanups must not erase the product need: **prove the language can carry the full shipped-surface story**, and when it cannot do so honestly, **grow the story** (or name a language gap) rather than hide surfaces.
