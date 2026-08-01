# S01 review — language beauty × physicist cognitive load

| Field | Value |
|---|---|
| Issue | [LISS-0223](../../issues/LISS-0223-s01-language-physicist-review.md) |
| Target | `examples/showcase/S01_quantum_disaster_response/` |
| Date | 2026-08-01 |
| Lenses | (1) programming-language beauty (2) physicist cognitive load |
| Class tags | A axiomatic / B sugar gap / C bug / E sample debt (friction ledger) |
| Status | **draft for Adjudicator triage** — not implementation approval |

```markdown
[DESIGN CHECK]
- Scope: review S01 showcase readability; propose ranked findings; no Kernel edits.
- Specs/files: S01 README + mains + domain/physics/protocol samples;
  physicist-dx-harmony; physicist-source-friction-ledger; LISS-0222/WP-0070.
- Boundaries: ops scenario lock stays; Host Python noted lightly; no live QPU.
- Ambiguities: which Class E items must ship as follow-ups (Adjudicator).
- Routing: Architecture Path / docs; human triage next.
- Evidence: concrete source citations; no invented Kernel APIs.
```

## Verdict (one paragraph)

S01 succeeds as a **reality-first coverage harness** and ops envelope document,
but as a **language exhibit for physicists** it currently teaches the wrong
habit: a long classical “tag farm” plus ~30 `inspect` lines precede the few
lines that look like Staqex. The quantum spine (`when` / `evolve` / `expect` /
terminal `measure`) is locally beautiful; the surrounding scorecard ceremony
dominates cognitive load. Treat the ranked list below as refactor guidance, not
as a demand to shrink the disaster OS story.

---

## What already works (keep)

| Signal | Where | Why it helps |
|---|---|---|
| Constraint Hamiltonian spelling | `physics/constraint_h.sqx` `c * (Z[0]*Z[1]) + f * (X[0]+X[1])` | Board-like Operator algebra |
| Indexed binders | `grid/block_costs.sqx` `sum` / `product` | Physicist-readable many-body shape |
| Phase enum | `domain/ops.sqx` `OpsPhase` | Exclusive ops windows without `if` |
| Linear branch | `main_disaster_response.sqx` `when (bit)` | Class A discipline made narrative |
| Evolve spine | same file `evolve … under H for duration using Suzuki` | Schrödinger-shaped story |
| Satellite lanes | `main_comms_channel` / QFT / interference | Separates open-system / spectrum demos |
| Honesty about gaps | README + comments on `inner`/`outer`, SIM-only | Does not fake QPU |

---

## Ranked findings

Severity: **P0** = confuses or mis-teaches physicists today; **P1** = beauty /
maintainability; **P2** = polish.

### P0-1 — Main is an `inspect` museum (beauty + load) — **E**

`main_disaster_response.sqx` builds a rich domain object graph, then collapses
almost every quantity into `Float …_tag` and `inspect(...)`. Roughly thirty
classical inspects sit before the quantum plan. A physicist scanning for the
experiment sees bookkeeping first, physics last.

**Recommendation:** Split “coverage probe” from “readable spine”: either a
thin `main_disaster_response.sqx` that tells tonight’s quantum story, or a
dedicated `main_coverage_probe.sqx` that owns the inspect farm. Keep ops
objects; stop treating every field as an inspect obligation in the primary
entry.

### P0-2 — Meaningless envelope “tags” (load) — **E**

`TheatreScale.k_ku_tag()` / `capital_tag()` sum population, acute caseload,
district counts, QPU box counts, etc. into one `Float`. That number has no
physical or ops meaning; it exists to survive `inspect` for the scorecard.

**Recommendation:** Expose named constants or separate inspects
(`capital_cells`, `capital_qpu_recommended` already exist). Delete sum-tags, or
rename and document them as **non-physical coverage probes** so they are never
mistaken for observables.

### P0-3 — Placeholder / dead domain API (beauty + load) — **E**

Examples:

- `ShelterStatus` enum is declared but sites use `status_tag: Float`.
- `ShelterSite.water_liters_as_kg()` returns a hardcoded `1200.0.kg` and ignores
  `this.water_kg` (with a dummy `_keep` read).
- `CommandBoard.phase_tag()` ignores `phase` and returns `priority`.
- `UnitKind` / `DepotStock` appear unused in the primary spine.

**Recommendation:** Either wire enums/SI fields for real, or delete dead API so
the showcase does not advertise fake physics methods.

### P1-1 — Package path ceremony (beauty + load) — **B / E**

`package com.staqex.examples.showcase.s01_disaster...` plus long
`Disaster.Domain.*` qualification is enterprise Java texture, not blackboard
texture. Harmony allows `namespace` for theory sectors; the fully qualified
Java package tree is optional noise for a showcase script.

**Recommendation:** Prefer shorter package roots for showcase (if Kernel
allows) or document a “physicist entry” that hides import boilerplate in one
facade module.

### P1-2 — Float soup where types exist (beauty + load) — **E**

Roads, hazards, fairness, and shelter status are mostly bare `Float` flags
(`0.0`/`1.0`) beside shipped `enum` / SI surfaces. The language can say more;
the showcase chooses not to.

**Recommendation:** Use `ShelterStatus`, booleans-as-enum, and SI where the
story cares (water, fuel, temperature already partially SI). Reserve raw
`Float` for dimensionless scores that truly are scores.

### P1-3 — Pipe free-fn escape hatch taught as style (beauty) — **B / E**

`protocol/compose.sqx` documents that pipeline RHS cannot be `this.method` and
uses free functions. Correct Kernel friction (Class B), but the showcase
comment frames it as a gotcha without a physicist reading.

**Recommendation:** Keep free-fn compose; add one comment linking to friction
ledger / LISS-0219 rather than “method wrap loses LINEAR seed” only.

### P1-4 — Quantum story buried; LINEAR uncompute tax unexplained (load) — **A / E**

Terminal `state x = |0>` uncomputes are Class A (Never Leave the State). In S01
they appear as silent ceremony after a long classical prelude. Physicists need
one sentence: *why* sibling wires must be discharged.

**Recommendation:** Short comment block citing the axiom; optionally measure a
named register instead of many `|0>` rebinds when that matches the story.

### P1-5 — Satellite fragmentation vs spine (beauty) — **design choice**

Lindblad, QFT burst, tri-register, and interference live in separate mains.
Good for terminal-measure honesty; bad for “one narrative evening.”

**Recommendation:** Adjudicator chooses: keep satellites as labs, or add a
README “reading order” that marks the tonight spine as the aesthetic entry and
satellites as appendix demos (partially true today — strengthen it).

### P2-1 — Host Python vs `.sqx` story (load)

Host companions are necessary honesty (MC inject, credentials). They are easy
to miss as “not the language.” README already lists them; keep that separation
explicit in any physicist walkthrough.

### P2-2 — ADR 0167 inline essay in main (beauty)

Useful for agents; heavy for humans reading the spine. Prefer a one-liner +
link to ADR in comments.

---

## Cognitive-load walk (physicist persona)

1. Opens README → scenario is clear; machine envelope is ops-heavy but honest.
2. Opens `main_disaster_response.sqx` → 15+ imports; long domain construction.
3. Searches for `evolve` / `|ψ⟩` shapes → finds them after ~190 lines.
4. Sees `inspect` wall → assumes the language requires tagging everything.
5. Sees `TheatreScale` sums → suspects “magic fitness” rather than constants.
6. Hits `|0>` uncompute → may think it is a bug unless Class A is taught.

**Net:** ops story is strong; **language beauty is concentrated in ~20 lines**
and diluted by coverage obligations.

---

## Proposed follow-ups (for Adjudicator — do not start without approval)

| ID (suggested) | Scope |
|---|---|
| LISS-0224? | S01 primary spine slim-down: move inspect farm to coverage probe |
| LISS-0225? | Delete or real-wire placeholder domain methods / enums |
| LISS-0226? | TheatreScale: named constants only; kill non-physical sum-tags |
| (link) | LISS-0219 inspect / lane-choice guidance — S01 as motivating sample |

No Kernel change is required to improve most P0/P1 items; they are sample debt.

---

## Next safe action

Adjudicator triage: accept / reject / re-rank findings; authorize which
follow-up Issue(s) to file and whether a refactor Phase is in scope.

---

## Shake pass (2026-08-01) — example debt purge + feature stress

Executed on branch `docs/liss-0223-s01-language-physicist-review`.

### Purged / repaired (Class E)

- Removed dead types `UnitKind`, `DepotStock`.
- Removed placeholder methods (`water_liters_as_kg`, SI `_keep` fakes,
  unused `.tag()` farms, `PriorityPipe.compose`, fake `suzuki_*_tag`,
  `soft_ir_ok`, non-physical `TheatreScale` sum-tags).
- Wired real enums into constructors: `ShelterStatus`, `RoadState`,
  `HazardKind`, `RequestKind`, `RecoveryKind`, with classical `open_weight`
  twins (Joint cannot `when` on enum — see Kernel gaps).
- SI getters return stored `Mass`/`Time`/`Length` fields where possible.
- `physics/tri_register.sqx` is now imported by `main_tri_register.sqx`.

### Scenario / spine shakes

| Shake | Result |
|---|---|
| Classical⊕State `state ration = 2/3; ration = ration + (1/4)` | **OK** |
| Morning `phase(status, 0.2)` | **OK** |
| Evolve under `H_drive + H_damage` or under OpBinder alone | **FAIL** — `cannot compile sparse Pauli for OpBinder` |
| `when (enum_binding)` | **FAIL** — Joint `KeyError` on enum name |
| Field named `state` on `RoadEdge` | **FAIL** — reserved keyword; renamed `road_state` |
| All S01 `main_*.sqx` after purge | **OK** (fidelity_inner: `check` only) |

### Kernel follow-ups to file (not fixed here)

1. **OpBinder → evolve**: sum/product Hamiltonians construct but cannot drive
   `evolve` (sparse Pauli compile). Blocks using grid binders as real physics.
2. **`when` on classical enum**: crashes evaluator (`KeyError`). Blocks
   enum-only scoring without Float twins.
3. (Optional) Document reserved identifiers (`state`) in showcase style guide.

### Recommendation

Keep S01 on this cleaned shape. Promote Kernel gaps (1)(2) to Feature Issues
before claiming “full language beauty” for binder-driven disaster Hamiltonians.
