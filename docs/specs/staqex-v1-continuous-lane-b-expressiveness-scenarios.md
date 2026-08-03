# Continuous / Lane B — expressiveness scenarios (proper-demand seats)

| Field | Value |
|---|---|
| Status | **Accepted as expressiveness inventory** (2026-08-03) — docs seats only |
| Issue | [LISS-0315](../issues/LISS-0315-continuous-lane-b-expressiveness-scenarios.md) |
| Review | [2026-08-03-continuous-lane-b-expressiveness-intake.md](../collaboration/reviews/2026-08-03-continuous-lane-b-expressiveness-intake.md) |
| Ship law | Mid-program `Continuous` **not** shipped — [ADR 0185](../architecture/adr/0185-kernel-continuous-value.md) Lane A only; Lane B needs a **future** ship ADR |
| Companions | ADR 0126, 0162, 0163, 0164; Lane A surface LISS-0313; S01 [locked scenario](staqex-v1-s01-locked-scenario.md) §Field continuous |
| Pedagogy | [physicist-minimal-dialect](../architecture/physicist-minimal-dialect.md); Ideal form first (ADR 0095) |

```markdown
[DESIGN CHECK]
- Scope: lock proper-demand scenarios for mid-program Continuous (Lane B) so
  language expressiveness can be scored like S01 A+B seats — Ideal chalk vs
  current Kernel, Class, action.
- Not in scope: Kernel Continuous Red; city-wide continuous QC; CFD/seismic
  waveform sims; amending ADR 0185 to ship Lane B.
- Obligation: each seat names Ideal form, hard gates, Lane A/Host substitute,
  and expressiveness gap (not theatrical coverage).
```

## 0. Product rule (Continuous expressiveness)

> Inventory **proper** continuous demand first; scenario seats grow only where
> multi-step continuous carriers must be first-class mid-program values; spine
> disaster OS stays finite jobs + Host. Ideal form is written before machine
> spelling. Measure / QPU remain finite-only forever under these seats.

**Proper-demand one-liner (Lane B):**

> Finiteize より前に、連続キャリアへの複数の意味ある変換を、Staqex 中盤の
> first-class 値として書き、有限化以降だけを Joint / measure に載せたい。

**Not proper (do not seat as Lane B):**

- 首都圏グリッド / 多セル Host federation alone  
- one-shot demand histogram inject (Lane A `finiteize` / Host MC)  
- magical continuous city-wide optimum QC  

---

## 1. Lane map (honesty)

| Lane | Role in these seats |
|---|---|
| **H** | Sensors, GIS, raw continuous models, MC draw callables |
| **Continuous mid-program (Lane B — future)** | Named continuous carriers; multi-step field algebra; **no** `measure` |
| **finiteize (Lane A — shipped)** | Continuous description / samples → finite `State` |
| **E finite Joint** | Tonight plan / zone assignment after finiteize; terminal `measure` |

```text
[H / Theory continuous world]
        │  (optional: bind as Continuous mid-program — Lane B)
        │  multi-step continuous transforms
        ▼
   finiteize  ──▶  finite State / Joint  ──▶  measure
   (Lane A)         (E-lane disaster plan)
```

---

## 2. Locked seats (expressiveness chapters)

Each seat must remain checkable even while Lane B is unshipped: Ideal chalk is
normative for **review**; Runtime path today is the **Lane A / Host substitute**.

### CH-field-compose — multi-step continuous field algebra → one finiteize

| Field | Value |
|---|---|
| Seat ID | **CH-field-compose** |
| Ops story | K-ku: damage density × flood / fire risk weight × impassable mask → zone priority field → finite bins for tonight shelter / rescue pressure |
| Why Lane B proper | ≥2 continuous transforms before any discrete assignment; Ideal form wants named mid-program continuous carriers, not one opaque Host blob |
| Phase | Pre-tonight Host prep → inject into E plan job |
| Hard gates | No `measure` on continuous; no silent grid; provenance on finiteize |

**Ideal form (blackboard — not legal Kernel Continuous yet):**

```text
// Ideal — continuous world (Lane B)
Continuous damage = field_from_host(…)      // or Theory/Host bridge
Continuous risk   = weight(damage, flood)
Continuous masked = mask(risk, impassable)
// explicit finiteization (Lane A surface once continuous is a value)
state zone = finiteize(masked, bins = N, interval = …)
// finite E-lane plan (existing disaster dialect)
state plan = … evolve / when …
measure plan tracing_out …
```

**Today (shipped substitute — expressiveness debt for Ideal form):**

```text
// Host builds histogram / inject; or single finiteize(lo,hi,bins,samples)
// multi-step continuous algebra lives in Python — not typed Staqex mid-program
state zone = finiteize(0.0, 1.0, N, samples, seed)  // uniform MVP only (LISS-0313)
```

| Check | Ideal | Today | Gap |
|---|---|---|---|
| Named continuous multi-step | Y | N | **B — needs Lane B ship ADR** |
| Explicit finiteize | Y | partial (uniform histogram MVP) | A — extend finiteize args / Host draw |
| Finite plan + measure | Y | Y | — |
| City-wide continuous QC | forbidden | forbidden | — |

---

### CH-field-fork — one continuous carrier → dual finiteize (two resolutions)

| Field | Value |
|---|---|
| Seat ID | **CH-field-fork** |
| Ops story | Same damage / demand field: coarse bins for capital fairness Host, fine bins for K-ku tonight assignment |
| Why Lane B proper | Shared continuous root; two finiteizations; Host dual-pipeline loses a single typed source |
| Phase | Morning re-estimate + tonight dual inject |
| Hard gates | Both finiteize paths carry independent ADR 0074 provenance |

**Ideal form:**

```text
Continuous damage = …
state coarse = finiteize(damage, grid = CoarseWard)
state fine   = finiteize(damage, grid = FineBlock)
// Host may federate coarse; E-lane measures fine plan only
measure fine_plan tracing_out …
```

**Today:** two Host MC injects or two `finiteize` calls with **no shared Continuous value** — formulas duplicated in Python.

| Check | Ideal | Today | Gap |
|---|---|---|---|
| Shared continuous bind | Y | N | **B** |
| Dual finiteize provenance | Y | Host-only | A/H |
| Independent resolution | Y | Y (Host) | type story missing |

---

### CH-field-theory — Theory continuous_operator aligned with notebook continuous

| Field | Value |
|---|---|
| Seat ID | **CH-field-theory** |
| Ops story | Pedagogy seat: continuous operator / field equation in Theory scope → same continuous type vocabulary → finiteize → small Joint evolve (not full CFD) |
| Why Lane B proper | Unifies Theory bridge (ADR 0074 / LISS-0111) with notebook continuous carriers; without Continuous type, Theory and Host remain disconnected dialects |
| Phase | Teaching / constellation satellite (not tonight spine) |
| Hard gates | Explicit discretization contract; no silent FD; no measure continuous |

**Ideal form:**

```text
// Theory continuous_operator + contract (existing path, Ideal continuous type)
Continuous psi_c = …
state psi = finiteize(psi_c, contract = UniformGrid(…))
state psi = evolve psi under H_grid for t
measure psi
```

**Today:** Theory discretization bridge lowers to grid Hamiltonian; Host MC separate; **no** mid-program Continuous shared type.

| Check | Ideal | Today | Gap |
|---|---|---|---|
| One continuous type world | Y | N (two paths) | **B + vocabulary ADR** |
| Explicit discretization | Y | Y (Theory) | keep |
| Finite evolve + measure | Y | Y | — |

---

## 3. Expressiveness inventory (score like S01 A+B)

**Seat today:** Y = Ideal + Runtime path honest; weak = substitute only; N = Ideal only.

| Surface / intent | Ideal seat | Path today | Seat today | Lane | Language-design note | Expressiveness note | Class | Action |
|---|---|---|---|---|---|---|---|---|
| Mid-program `Continuous` bind | CH-field-compose/fork/theory | — | N | B future | ADR 0126 Decision 1 still holds | Core Ideal gap | **B** | needs-ADR (Lane B ship) |
| Continuous multi-step map/weight/mask | CH-field-compose | Host Python | weak | H | Ideal form first | Ops field algebra expressiveness | **B** | needs-ADR + expand-scenario |
| `finiteize` from Continuous value | all CH-field-* | `finiteize(lo,hi,…)` uniform MVP | weak | A | ADR 0185 Lane A | Entry honest; args thin | **E** | extend finiteize (Feature) after B or Host profile |
| Dual finiteize shared root | CH-field-fork | dual Host inject | weak | H/A | provenance ×2 | Fork expressiveness | **B** | needs-ADR |
| Theory continuous_operator | CH-field-theory | LISS-0111 bridge | weak | Theory | ADR 0074 | Vocabulary split vs Host MC | **B** | needs-ADR unify |
| Host MC inject | demand / damage prior | 0163/0164 + S01 host | Y | H | OS shell | Good for one-shot inject | — | keep |
| Lane A `finiteize` Call | B18 | LISS-0313 | Y | A | shipped | Teaching entry | — | keep |
| Finite Joint plan + `tracing_out` | S01 spine | shipped | Y | E | NLTS | Disaster OS core | — | keep |
| Continuous `measure` | — | forbidden | N/A | — | hard gate | Must stay illegal | **A** | keep-forbidden |
| City-wide continuous QC | — | forbidden | N/A | — | locked scenario | Anti-goal | **A** | keep-forbidden |
| CFD / continuous seismic waveform | — | out | N/A | — | S0 honesty | Not language seat | — | permanent-out sample |

**Counts:** inventory **12** rows.  
**needs-ADR (Lane B):** **4**. **extend finiteize:** **1**. **keep / keep-forbidden:** **7**.

---

## 4. Language-design findings (ranked)

### P0 — Mid-program Continuous type world (blocked)

Ideal seats require `Continuous` as a distinct type with hard gates. **Not**
unsealed by ADR 0185. Opening is Architecture Path + ship ADR only.

### P1 — Finiteize consumption of Continuous values

Even after Lane B, `finiteize` must accept Continuous (not only uniform
positional floats). Lane A MVP is intentionally thin (LISS-0313).

### P1 — Vocabulary split Theory bridge vs Host MC vs Ideal Continuous

Three continuous-adjacent stories. Expressiveness review treats unification as
Lane B family work, not silent merge under Lane A.

### P2 — S01 spine must not absorb Continuous

Tonight spine stays finite dialect. CH-field-* are **constellation / pre-inject**
seats — same rule as scorecard: one main is not the whole OS.

### P2 — Pedagogical Ideal chalk must stay marked Ideal

Agents must not treat Ideal Continuous snippets as Kernel Green permission.

---

## 5. Verification plan (expressiveness check procedure)

Use this checklist in Architecture / Feature reviews (same spirit as S01
expressiveness Phase 0):

1. **Seat exists?** Each Ideal continuous demand maps to a CH-field-* ID here
   or is explicitly rejected as improper.
2. **Ideal form written?** Blackboard-first snippet present (ADR 0095).
3. **Hard gates stated?** No measure / no QPU / explicit finiteize.
4. **Today path honest?** Lane A/Host substitute named; no fake Runtime Continuous.
5. **Class + action?** needs-ADR / extend finiteize / keep / keep-forbidden.
6. **Spine purity?** No CH-field Continuous forced onto `main_disaster_response.sqx`.
7. **Physicist sentence?** One sentence per seat matching Ideal form.

**Pass:** inventory complete; no silent Lane B claim; gaps Class-tagged.  
**Fail:** Ideal Continuous sold as shipped; or city-wide continuous QC seated as
proper demand.

---

## 6. Out of inventory (improper demand — recorded so not re-proposed as B)

| Claim | Why improper for Lane B | Prefer |
|---|---|---|
| 首都圏 80-cell cover | Scale = Host grid of finite jobs | locked scenario scale-out |
| Rolling replan frequency | Orchestration, not continuous type | Host jobs |
| One histogram inject | Single finiteize | Lane A / Host MC |
| Continuous city optimum | Anti-goal | forbidden |

---

## 7. Next gates (not authorized by this doc)

| Gate | Artifact |
|---|---|
| Architecture Accept Lane B ship shape | Future ADR (beyond 0185) |
| Feature Red Continuous type | Future LISS after ship ADR |
| Finiteize Continuous-valued args | Feature after or with B |
| S01 chapter `.sqx` for CH-field-* | Only after Runtime surface exists — until then Host demos + Ideal chalk |

This document **authorizes documentation seats and expressiveness scoring only**.
