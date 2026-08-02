# S01 expressiveness & language-design review (LISS-0245 Phase 0)

| Field | Value |
|---|---|
| Date | 2026-08-02 |
| Issue | [LISS-0245](../../issues/LISS-0245-s01-expressiveness-review-scenario-expansion.md) |
| Status | **Review complete — triage Accepted** (2026-08-02); E1 locked-scenario seats authorized (docs) |
| Pedagogy law | [Accepted minimal dialect](../../architecture/physicist-minimal-dialect.md) |
| Scorecard | [constellation index](../../specs/staqex-v1-s01-coverage-scorecard.md) |
| Locked scenario | [staqex-v1-s01-locked-scenario.md](../../specs/staqex-v1-s01-locked-scenario.md) |
| Prior | [LISS-0223 review](2026-08-01-s01-language-physicist-review.md); R1 [LISS-0244](../../issues/LISS-0244-s01-r1-dialect-honesty-readme-scorecard.md); R2 [LISS-0246](../../issues/LISS-0246-s01-r2-spine-dialect-pass.md) |

```markdown
[DESIGN CHECK]
- Scope: Phase 0 only — full A+B inventory, scenario expansion draft,
  spine/constellation map, ranked language-design findings.
- Not in scope: .sqx edits; scorecard row deletion; axiom ADR; live QPU.
- Obligation: keep every A+B surface in the constellation; expand scenario
  when a seat is weak/theatrical.
- Verification: Adjudicator accepts/amends seats → E1 locked-scenario PR → R3.
```

## 0. One-line product rule (reconfirmed)

> Full expressiveness inventory first; scenario grows until each surface has a
> legitimate narrative seat; spine stays dialect-honest.

## 1. Spine vs constellation map

### Spine sentence (E-lane — dialect)

> Tonight corridor-vs-shelter planning tension as a **small** spin system under
> named constraint Hamiltonians; one terminal plan sample (`measure plan0`).

**Path:** `main_disaster_response.sqx`  
**Allowed on spine:** `when`, ket, named `H_*` + Suzuki `evolve for`, sparse
`expect`, typed ration Classical⊕State, `impl`/pipe binds that feed the plan
story, multi-file import, NLTS + singular `measure`, LINEAR residual discharge
(documented Class E until `tracing_out` ADR).  
**Forbidden on spine (R2 already enforced):** `inspect` museum, identity
`evolve times`, unmarked soft `until` as “production.”

### Constellation chapters (must earn locked-scenario prose)

| Chapter ID | Entry | Lane | Scenario phase |
|---|---|---|---|
| CH-tonight-spine | `main_disaster_response.sqx` | E (H-algebra) | Tonight plan |
| CH-morning | `main_morning_collect.sqx` | E + classical | Morning collect |
| CH-day2 | `main_day2_recovery.sqx` | E (H-algebra) | Day-2 recovery |
| CH-comms | `main_comms_channel.sqx` | open / Lindblad | Noisy order channel |
| CH-burst | `main_burst_spectrum.sqx` | circuit | Sensor / RF burst |
| CH-tri | `main_tri_register.sqx` | E multi-register | Multi-command coupling |
| CH-route | `main_route_interference.sqx` | E phase | Competing corridors |
| CH-lattice | `main_lattice_four.sqx` | E Index/Basis | Zone damage field |
| CH-fidelity | `main_fidelity_inner_check.sqx` | E | Prior vs proposal fidelity |
| CH-fuel | `main_fuel_search.sqx` | E Non-placeable | Fuel search under budget |
| CH-host | `host/*.py` | H | Demand inject, credential, job, ticket |

**Rule:** no chapter without a locked-scenario seat paragraph (E1).

## 2. Expressiveness inventory (scorecard A+B + additives)

**Seat today:** Y = named in locked scenario + honest path; weak = path exists
but story thin/theatrical; N = path only / coverage orphan.

| Surface | Current path(s) | Seat today | Proposed seat if expand | Lane | Language-design note | Expressiveness note | Class | Action |
|---|---|---|---|---|---|---|---|---|
| `when` (not `if`) | spine / morning / day2 | Y | Keep: phase & shelter status mixtures | E | Class A control rejection | Strong ops reading | A | keep |
| named Float/struct → Operator | `physics/constraint_h.sqx` | Y | Keep: constraint coeffs → H | E | Matches blackboard H | Core expressiveness | — | keep |
| `expect` | spine (ZZ) | Y | Keep: notebook observable | E | Dialect IN | Good | — | keep |
| `inspect` | morning / day2 / satellites | weak | **Host logs** for ops; sparse chapter peek only | E→H | Official “not measure” vs sample abuse | R2 cleared spine; chapters still printf-heavy | E | expand-scenario + relocate-within-S01 (Host) |
| typed `state` | spine ration | Y | Keep: fair-share ticket State | E | Axiom 1 demo | Good Classical⊕State | — | keep |
| multi-file import | package tree | Y | Keep: theory sectors | E | FQN noise Class E pedagogy | Expresses modular physics packs | E | keep (shorten names Class E hygiene) |
| NLTS + `measure` | each `main_*.sqx` | Y | Keep: one sample per window | E | Axiom 5 | Result boundary; Host envelopes | — | keep |
| ket + `evolve for` | spine / day2 | Y | Keep: tonight / day-2 evolve | E | Dialect core | Good | — | keep |
| `evolve times` (non-identity) | (removed identity from spine) | N | Replan-tick evolve **only if** body is real hop | E | Empty body was theater | Need story or stay absent | E | expand-scenario (optional) or keep absent |
| Operator + Suzuki | spine S2 / day2 S4 | Y | Keep: policy-named Trotter | E | Dialect core | Good | — | keep |
| OOP + visibility | `domain/` / `physics/` | weak | Classical ops packs = **H-adjacent library**; physical `class` only when state evolves | E/H | Harmony table vs DTO reality | Expresses large classical model; blunts “class=system” | E/B | expand-scenario (name classical ops objects) + demote physics reading |
| LINEAR | spine discharge | weak | Document residual; prefer future `tracing_out` | E | Forced tax vs physics trace-out | Expressiveness gap | B | needs-ADR (`tracing_out`) |
| Ports (Rng/MeasureSink/Source) | Kernel + host | Y | Keep: runtime I/O honesty | H/E | Clean Architecture | Good | — | keep |
| fail-closed | `agency_share` / Abort | Y | Keep: credential / budget refuse | H | Host OS shell | Good | — | keep |
| `sum`/`product`+`Index` | `grid/block_costs.sqx`, lattice4 | weak | District damage / flood-zone field aggregates | E | Binder surface | Needs zone story in lock | — | expand-scenario |
| `Basis<N>` | lattice4 | weak | Same zone field basis | E | | | — | expand-scenario |
| `inner`/`outer` | `main_fidelity_inner_check.sqx` | weak | Plan prior vs proposal fidelity check | E | Runnable (LISS-0229) | Honest physics seat if named | — | expand-scenario |
| `evolve … until` | `main_fuel_search.sqx` | weak | Fuel/resource search under convergence budget; **Non-placeable** | E | writeable≠placeable | Soft QPU diag expected | — | expand-scenario |
| phase / interference | `main_route_interference.sqx` | Y | Competing corridor phases | E | | Locked “secondary disaster routes” | — | keep |
| Type-First + SI | `domain/quantities` | Y | Dimful field stocks + `to` at use sites (ADR 0174 / LISS-0254 heal) | E | D5 demotion lifted | Honest Type-First sell | — | keep |
| pipe / Partial / poly Fusion | `protocol/compose` on spine | weak | Priority composition for dispatch order | E | | Ops seat exists in decisions list | — | expand-scenario |
| Trace-Out fn | `local_priority_bump` | weak | Local bump then drop caller locals | E | Related to LINEAR pedagogy | Needs explicit seat | B | expand-scenario |
| Lindblad | `main_comms_channel.sqx` | weak | Intermittent tower / noisy order channel (C-box narrative) | open | Soft/open lane | Locked C-box story | — | expand-scenario |
| QFT / cqft apply | `main_burst_spectrum.sqx` | weak | 119 / sensor burst → classical replan hint (S-box) | circuit | Sub-lane D4 | Locked S-box story | — | expand-scenario |
| Host Job / Credential / MC | `host/*.py` | Y | Demand inject; agency share; rolling replan | H | Two-language D1 | OS shell expressiveness | — | keep |
| TonightTicket export | `export_tonight_ticket.py` | Y | Structured tonight handoff (LISS-0243) | H | Result boundary | Additive row | — | keep |
| multi-register | `main_tri_register.sqx` | weak | Rescue × logistics × fire command coupling | E | | Contention story | — | expand-scenario |
| `impl` dispatch | spine readiness/haul | Y | Capability protocols | E | | Good | — | keep |
| Classical⊕State | spine ration | Y | Fair-share tickets | E | | Good | — | keep |
| soft QPU honesty | fuel + diags | weak | Label Non-placeable in scenario + README | E | ADR 0095 writeable≠exec | Must not read as production | E | expand-scenario |
| register `forEach` | burst spectrum | weak | Circuit-lane register map (not classical `for`) | circuit | for vs forEach pedagogy | Needs lane heading | E | expand-scenario |

**Counts:** inventory rows **30** (A+B + additives).  
**Actions (post ADR 0173/0174 heal):** keep **15**; expand-scenario **13**;
needs-ADR language P0s **0** (LINEAR + Type-First resolved); relocate/Host **1**
(`inspect`). Historical draft had needs-ADR **2** before those ADRs.

## 3. Scenario expansion draft (for each `expand-scenario`)

Prose targets for **E1** locked-scenario amendments (not applied in this PR).

| ID | Who / object | When | Ops or physics | Joint / Host |
|---|---|---|---|---|
| SE-01 inspect→Host | Field / HQ log sinks | All phases | Observation logs are Host MeasureSink / ticket notes — not spine `inspect` museums | Host |
| SE-02 zone Index/Basis | District flood / liquefaction cells | Tonight + morning | `Index`/`Basis` aggregates damage/openness per zone | Joint chapter CH-lattice |
| SE-03 fidelity | Planning cell | Tonight roll | Prior tonight plan vs new proposal fidelity (`inner`/`outer`) before commit | Joint CH-fidelity |
| SE-04 fuel until | Logistics | Tonight | Fuel search / pump-until-converged under max steps; **Non-placeable on QPU** | Joint CH-fuel |
| SE-05 pipe/Fusion | Dispatch desk | Tonight | Priority pipes compose rescue vs haul order | Joint on spine (already coded) + lock prose |
| SE-06 Trace-Out bump | Same desk | Tonight | Local priority bump then drop temps | Joint + lock prose |
| SE-07 Lindblad comms | Comms / C-box | Tonight–morning | Noisy order channel → priority list | Joint CH-comms |
| SE-08 QFT burst | Sensor / S-box | Tonight | Burst spectrum → classical replan hint | Circuit CH-burst |
| SE-09 tri-register | Multi-command | Tonight | Coupled command registers (rescue/logistics/fire) | Joint CH-tri |
| SE-10 OOP classical | HQ classical model | All | CommandBoard / shelters / roads are **classical ops objects** (H-adjacent), not evolving quantum systems | Domain + lock honesty |
| SE-11 soft QPU | Fuel / until | Tonight | Explicit Non-placeable banner in scenario | Docs |
| SE-12 forEach | Burst chapter | Tonight | Circuit register iteration ≠ classical `for` | Circuit docs |
| SE-13 optional evolve times | Replan tick | Tonight roll | Only if body is a real hop (damage update); else remain absent | Optional |

## 4. Language-design findings (ranked)

| Rank | Finding | Class | Recommendation | Status (2026-08-02 heal) |
|---|---|---|---|---|
| P0 | LINEAR hand `|0>` discharge vs physics “where did siblings go?” | B | ADR: `measure … tracing_out` | **Resolved** — [ADR 0173](../../architecture/adr/0173-measure-tracing-out-leftover-policy.md) + LISS-0250–0252 |
| P0 | Type-First units die on `Float` fields | B | Field unit retention | **Resolved** — [ADR 0174](../../architecture/adr/0174-type-first-field-units.md) + LISS-0254 |
| P1 | `inspect` still teaches printf on morning/day2 chapters | E | Host logs; sparse chapter peeks | **Mitigated** — R3 (LISS-0248); residual polish LISS-0260 |
| P1 | `class`/domain packs read as Java DTO, not physical system | E | Classical ops library prose | **Partial** — lock honesty; causal use → [LISS-0256](../../issues/LISS-0256-s01-spine-causal-domain-joint.md) |
| P1 | Circuit vs Hamiltonian sub-lanes unmarked in teaching | E | Chapter headings + lane labels | **Mitigated** — CH-* seats (LISS-0247/0248) |
| P2 | Package / FQN noise | E | Shorten showcase packages where legal | **Open** — [LISS-0260](../../issues/LISS-0260-s01-fqn-inspect-hygiene.md) |
| P2 | Dual `+` (Float / State / Operator) cognitive cost | — | Teach by lane | Open (not WP-0087 Kernel) |
| P2 | Err world-line vs Job diagnostic vocabulary | — | Failure glossary ADR | **Resolved** — [ADR 0175](../../architecture/adr/0175-failure-glossary.md) **Accepted** |

**Forced language costs (historical P0s now closed):** LINEAR leftovers → `tracing_out`;
Type-First fields → ADR 0174. Remaining forced costs: dual `+`, package module tax.  
**Sample / scenario debt remaining:** spine causal gap (domain built but not on Joint) →
[WP-0087](../../work-plans/WP-0087-s01-expressiveness-brushup.md) / LISS-0256+.

## 5. Recommended follow-up Issues (after triage)

| ID | Work | Depends | Status |
|---|---|---|---|
| **E1** | Amend locked scenario with SE-01…SE-12 seats | Adjudicator accept this review | **complete** LISS-0247 |
| **R3** | Align chapter READMEs / thin morning inspect / name chapters | E1 | **complete** LISS-0248 |
| ADR ① | `tracing_out` | Architecture Path | **Accepted** ADR 0173 / LISS-0250–0252 |
| ADR ② | Type-First fields | Architecture Path | **Accepted** ADR 0174 / LISS-0254 |
| ADR ③ | failure glossary | Architecture Path | **Accepted** ADR 0175 / LISS-0258 |
| Brush-up | causal spine / chapter arcs / ticket meaning | WP-0087 | **complete + post_reviewed** LISS-0255–0260 |
| Optional | Reintroduce non-identity `evolve times` only with SE-13 | E1 | deferred |

## 6. Adjudicator triage checklist

**Accepted** (Adjudicator, 2026-08-02) — recommended policy:

- [x] Accept inventory Actions (keep / expand-scenario / needs-ADR as filed)
- [x] Accept scenario expansion IDs **SE-01…SE-12** for E1 (SE-13 optional/later)
- [x] ADR batch order: **① `tracing_out` → ② Type-First fields vs demote → ③ failure glossary**
- [x] Authorize **E1** docs (locked-scenario seats) now
- [x] Confirm: **no** scorecard A+B demotion in this wave

**Policy one-liner:** do not shrink the scorecard; grow the scenario until each
surface has a legitimate seat; spine stays dialect-honest; language gaps → ADR;
sample lies → E1 then R3.

## 7. Completion report (Phase 0)

## Summary
- Inventory rows complete: **30** (A+B + additives)
- expand-scenario count: **13**
- language-design P0 findings: **2** (LINEAR/`tracing_out`; Type-First fields)

## Artifacts
- review path: `docs/collaboration/reviews/2026-08-02-s01-expressiveness-scenario-review.md`
- scenario draft: §3 SE-01…SE-13 (locked-scenario text not yet edited)

## Adjudicator decisions needed
- Triage §6; authorize E1

## Follow-up Feature Issues
- E1 locked-scenario amend; R3 chapter align; ADR batch as ranked
