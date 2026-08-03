# S01 locked scenario — Quantum Disaster Response OS

| Field | Value |
|---|---|
| Status | **Locked** (2026-08-01) |
| Purpose | Authoritative story for the language-spec benchmark showcase |
| Showcase | [`examples/showcase/S01_quantum_disaster_response/`](../../examples/showcase/S01_quantum_disaster_response/) |
| Mission | [mission lock](staqex-v1-showcase-mission-lock.md) |
| S0 | [S0 disaster](staqex-v1-showcase-s0-disaster-response.md) |

**This program was written as a language-specification / expressiveness
benchmark.** The scenario below is the reality-first story that the benchmark
rides on — not a claim that a city was optimally solved.

When reality and a syntax demo conflict, **reality wins** (do not invent
unshipped Kernel surfaces to “look quantum”).

---

## Product (public)

**Name:** Quantum Disaster Response OS（量子災害緊急対応 OS）

**Social problem:** Evacuation chaos, competing rescue claims, outages, unfair
allocation, and secondary hazards after a major coastal earthquake.

**One sentence:**

> A command-room OS you would actually use after a disaster: maps, stocks,
> units, comms, and priorities as real ops data; explore many candidate actions
> at once; grow a plan under field constraints; inspect mid-window; ingest
> demand noise; allocate fairly; lock tonight’s executable plan; then carry
> morning measurements into next-day recovery.

---

## Setting (one fixed story)

### Publish name vs design archetype

| Field | Value |
|---|---|
| **Publish name (body text)** | **K-ku**（K区） |
| Design archetype (repo note only) | Eastern Tokyo lowland ward pattern: liquefaction + wooden dense-fire risk + zero-meter flood basin. **Do not expand the real ward name in public-facing copy.** |
| Showcase | Graphs shrunk for runtime; roles/data kinds stay HQ-grade |

### Locked scale — K-ku single HQ

| Quantity | Locked assumption (one K-ku HQ) | Notes |
|---|---|---|
| Resident population | **~4.5×10⁵** (≈ 450,000) | Mid-size ward-class jurisdiction |
| People in acute impact overnight | **~1.0×10⁵–1.2×10⁵** | Overlap of liquefaction damage, wooden-fire threat, and zero-meter inundation — not “all residents dead” |
| Ops districts / cells inside K-ku | **48** | Neighborhood planning partitions; showcase may run 4–8 |
| Open / candidate shelters | **24** | Capacity + fill tracked |
| Concurrent high-urgency request clusters (first-night peak) | **~400** (200–800 band) | Entrapment / shelter / supply / firefighting / aftershock survey — clustered |
| Deployable field units (rescue + logistics + fire) | **~80** (40–120 band) | Assignable in tonight window |
| Road / corridor graph (ops-grade) | **~300** directed edges | Showcase shrinks for Joint cost |
| Characteristic hazards (K-ku) | Liquefaction; wooden dense-area fire / firestorm risk; zero-meter inundation; aftershock re-collapse | Ops tags — not CFD / full seismic waveform |
| Tonight replan cadence | Event + **~15 min** rolls | Several–tens of planning jobs / night |
| Morning → day-2 | 1 collect package + recovery queue **~40** items | Continues into T+1 |

**What scales with load:** job **width** on planning box **P** (logical carriers /
ops), and classical Host data — **not** “one QPU per 10,000 people.”

**What does *not* scale linearly with population:** QPU **box count per HQ**.
Larger theatres use a **grid of K-ku-class HQs** (see Kanto section), not one
mega-machine per metro.

### What happened (trigger timeline) — K-ku

1. Late night: a **strong mainshock** hits the capital region; K-ku feels
   intense shaking.
2. **Liquefaction** damages roads, buried lines, and building foundations in
   soft / filled ground.
3. **Zero-meter / lowland inundation** (storm surge / embankment stress /
   drainage failure) threatens riverside and basin neighborhoods.
4. **Wooden dense blocks** ignite; under wind + debris + outages, **firestorm
   risk** rises (ops pressure tags).
5. Wide-area **power outage** and **intermittent tower / cellular failure**.
6. Ward HQ / 119 flooded with simultaneous rescue, shelter-open, supply, and
   firefighting requests.
7. **Aftershocks** re-block corridors and create new entrapment / survey demand.

### Field problems (what K-ku is suffering)

| Problem | Substance |
|---|---|
| Fragmented information | Which roads survived liquefaction, which shelters are full, who is trapped / cut off by water or fire — data late or missing |
| Resource contention | Ambulances, heavy gear, fire/SDF/police, meds, fuel, water, comms bandwidth |
| Unfair allocation risk | Loud or nearby requests win; basin / wooden-dense / remote cells wait |
| Secondary disaster | Wrong routes → jam / isolation; fuel out; command loss; fire / firestorm spread; aftershock re-damage; inundation expansion |
| Time pressure | Tonight’s plan in tens of minutes to a few hours; situation keeps changing |

### Decisions the OS bundles (not one named puzzle)

One execution cycle addresses **combinatorial assignment + uncertainty +
fairness**:

1. **Reachability-aware deployment** — assign units/vehicles to requests on the
   passable road graph.
2. **Shelter capacity allocation** — flow people from flood/collapse zones
   under full shelters and closed corridors.
3. **Supply / fuel dispatch order** — what moves where, in what sequence (SI).
4. **Comms priority** — which orders / sensor updates get scarce bandwidth.
5. **Replan cycle** — road reopen, new entrapments, tower restore, fires /
   aftershocks, and **morning measured data** feed next-day recovery (tonight
   is not the end).

---

## Realtime optimization (locked honesty)

**Assume:** operational **near-real-time / event-driven rolling replan**.

| Layer | Assumption | Example |
|---|---|---|
| Seconds–minutes | New request / road block / tower restore / fire alarm → **start a replan job** | Entrapment found → update assignment within minutes |
| Minutes–~15 min | Tonight **periodic roll** re-optimizes unfinished work | Congestion / fuel burn reflected |
| Hours–day | Morning collect → next-day plan | Recovery priority queue |

**Do not pretend:**

- Magical continuous QC that always solves the whole city strictly optimally
- Sub-second global optimality on a live quantum cloud
- Fully synchronized global optimization under total comms blackout

**Language / execution:** each replan is a finite-support State/Joint **job**
(candidate expand → evolve → expect → measure). “Realtime” comes from job
frequency and input refresh. Host batches sensors/reports for inject. Slightly
future machines still run **job-shaped** work.

**Quantum meaning (honest):** superpose many candidate plans, grow under
constraints, inspect, ingest noise, collapse to one executable plan per window.
**Not** a continuous strict-optimum guarantee — but a fresh feasible plan for
*this* window whenever the world changes.

---

## Social outputs (full cycle)

Outputs are not “tonight only.” **Tonight execute → morning collect → next-day
moves** is one ops cycle.

### A. Tonight (T0 → morning) — immediate execution

| Output | Audience | Content |
|---|---|---|
| Execution plan ticket | Fire / medical / SDF–police / logistics | Destinations, routes, times, loads per unit/vehicle |
| Evacuation guidance | Shelters / public info / field command | Which districts → which shelters; detours |
| Supply / fuel allocation | Depots / dispatch | What to where, SI units |
| Comms priority list | Info / comms cell | What ships tonight vs deferred |
| Rolling replan deltas | All units | Who’s destination changed after event / roll |
| Fairness / provenance report | HQ / audit | Why this allocation; unmet; honesty |
| Unmet / residual risk | HQ | Unserved requests; fire / aftershock / isolation risk |

### B. Morning — next-cycle inputs (official artifacts)

| Output | Audience | Content |
|---|---|---|
| Passability / blockage map update | Map / info | Roads that worked / failed; new collapse (incl. aftershock) |
| Request status update | Command | Filled / partial / unreachable / new entrapment / firefighting |
| Shelter field census | Shelter cell | Occupancy; water / food / medical remaining; hygiene risk |
| Unit / vehicle condition | Field command | Fatigue, fuel left, faults, delay |
| Comms restore snapshot | Comms | Towers back / still down |
| Fire / firestorm watch update | Fire / HQ | Active fires, corridor closures, firestorm-risk districts |
| Noise re-estimation samples | Host / analysis | Measured demand / ETA → next Host MC prior |

Missing fields stay **missing** (do not invent).

### C. Next day (T+1) — recovery / continued rescue

| Output | Audience | Content |
|---|---|---|
| Day-2 execution plan | All units | Continued rescue, new requests, redeploy, relief crews |
| Recovery priority queue | Civil / power / comms | Which roads / lines open first (rescue-effect order) |
| Resupply / external aid intake | Logistics / liaison | Intake points and dispatch order (CredentialPort-gated) |
| Shelter merge / return draft | HQ / public info | Relief of overcrowding; secondary evacuate; advisories |
| Daily fairness review | Audit / public explain | How last night’s unmet was handled |
| Carryover risk to T+1 night | HQ | Remaining isolation / medical / hygiene / fire watch |

**Value returned to society:** a feasible plan on the chaotic first night;
honest morning data about what really happened; next-day moves updated from
that data.

**Intentionally not emitted:** victim PII dumps; live cloud QPU submit; city-wide
“proof of optimality.”

```text
TonightPlan → FieldExecution → MorningDataCollection
  → NextDayReplan → Day2FieldMoves → NextNightCarryover
```

---

## Physical quantum computers — K-ku install

**Question:** For **one K-ku HQ** (~4.5×10⁵ residents, ~1×10⁵ acute overnight,
48 districts, ~400 request clusters, ~80 units), how many **real** quantum
computers to **build / install**, and at what spec?

Envelopes: ADR **0109** / **0110** / **0111**
([delivery envelope](../architecture/current-hardware-delivery-envelope.md)).
Not a vendor PO; not “ward optimally solved.”

> **Note:** Shipping Kernel path for S01 today is **SIM-only**. Manufacturing
> counts ignore simulators.

### Sizing method

1. Lock K-ku demographics (table above).  
2. Encode tonight’s decisions as **finite jobs** (not 1 qubit / person).  
   With U≈80, R≈400, D_sector≈8–12 → packed planning width typically
   **O(10²) logical** carriers per job — **not** O(10⁵).  
3. **Box count** = concurrent lanes at **this** HQ (P / C / S), not population÷N.  
4. **Box spec** = NH5 band covering that job width + ops budget.

### How many to make — K-ku

| Decision | Physical QPU boxes | Meaning |
|---|---:|---|
| **Minimum** | **1** | Planning **P** only (C/S queue on P or classical/SIM + honesty) |
| **Recommended** | **3** | Full lanes **P + C + S** |
| **High availability** | **4** | 3 + **1 spare = P** |
| **Rejected** | 48 / 400 / 10⁵ | One per district / request / person |

Classical hosts at K-ku HQ: **1–2** (not quantum).

### Specs — K-ku (諸元)

| ID | Qty | Spec (K-ku) | Role |
|---|---:|---|---|
| **P** | **1** | **`NH5_FT_MEGA`**: **~150–300 logical** carriers; **~10⁶–10⁸** logical ops **per replan job**; gate + Hamiltonian evolve; terminal measure | Tonight / 15‑min roll / day-2 assignment under liquefaction / fire / inundation constraints |
| **C** | **1** | **`NH5_NATIVE_LARGE` band**: **~10³–10⁴** sites (geometry + jump/loss); Lindblad-class toy, not full CPTP product | Comms degradation → priority list |
| **S** | **1** | Digital **~32–128** physical qubits ops-grade (`CH1` ≤16 only for demos) | 119 / sensor burst spectrum → classical replan hint |
| Spare | **0–1** | Same as **P** | Maintenance / aftershock surge |

**K-ku procurement default:** **build 3** (or **1** if forced).

---

## Scale-out — 首都圏 cover (1都3県 grid of K-ku-class cells)

Do **not** run all of 首都圏 as one planning job on one mega-QPU. Cover the
capital region with a **fixed ops grid**: each cell is **K-ku-class**; a
regional layer **federates** cell plans.

### Locked grid assumption (首都圏 cover)

| Field | Locked constant |
|---|---|
| Theatre | **首都圏（1都3県）** — Tokyo / Kanagawa / Saitama / Chiba |
| Theatre population (order) | **~3.6×10⁷** |
| Grid | **80** ops cells **G01–G80** |
| Mean load per cell | ≈ **K-ku class** (~4.5×10⁵ residents; own HQ) — 80 × 4.5×10⁵ ≈ 3.6×10⁷ |
| Cell fleet | Same as K-ku: recommended **3** (P+C+S), min **1**, HA **4** |
| Regional classical federation | **1** capital coordination center (Host / CredentialPort / cross-cell fairness) |
| Optional regional planners | **2–4** boxes **Pᵣ** (inter-cell mutual-aid only) |
| Showcase spine | Still **one K-ku** cell; 首都圏 numbers are the deploy envelope constants |
| Out of this lock | 関東七県の山間・広域町村を同一粒度で全部 — 必要なら外縁セルを粗く足す別拡張 |

Illustrative bands (ops IDs, not legal boundaries):

```text
G01–G24   Tokyo core / ward-belt (incl. publish K-ku in the eastern lowland band)
G25–G40   Kanagawa urban–bay belt
G41–G60   Saitama corridor / river belt
G61–G80   Chiba urban–bay / logistics belt
```

### 首都圏 totals (arithmetic)

| Install class | Formula | Physical QPU boxes |
|---|---|---:|
| **Minimum** | 80 × 1 (P only) | **80** |
| **Recommended** | 80 × 3 (P+C+S) | **240** |
| **High availability** | 80 × 4 (+ P spare each) | **320** |
| **+ optional regional Pᵣ** | +2 … +4 | **242–244** / **322–324** |

**Per-box spec:** each cell’s **P/C/S** = K-ku 諸元 table above.  
**Pᵣ:** same NH5_FT_MEGA band as **P**; jobs are **inter-cell mutual-aid only**.

### What this rejects

| Wrong scaling | Why rejected |
|---|---|
| 1 QPU for all 首都圏 | Job width explodes |
| Population ÷ 10k → idle box farm | Ignores HQ job lanes |
| One QS-2 “solves 首都圏” | Not this product’s promise |

### Provenance

Tickets name **cell id (Gnn) + box P/C/S** or SIM fallback. Cross-cell aid
names **Pᵣ** when used. Live submit still needs separate technology selection
+ CredentialPort before production wiring.

---

## Field continuous expressiveness seats (deferred — Lane B)

**Not** city-wide continuous QC. **Not** tonight-spine Continuous. These seats
lock **proper mid-program Continuous demand** so language expressiveness can be
scored the same way as constellation chapters (Ideal form vs shipped path).

Authoritative inventory + Ideal chalk + Class/actions:

[`staqex-v1-continuous-lane-b-expressiveness-scenarios.md`](staqex-v1-continuous-lane-b-expressiveness-scenarios.md)
([LISS-0315](../issues/LISS-0315-continuous-lane-b-expressiveness-scenarios.md)).

| Seat ID | Story (K-ku) | Why not “just Host” | Runtime today |
|---|---|---|---|
| **CH-field-compose** | Damage × flood/fire weight × impassable mask → zone priority field → finite bins for tonight pressure | Multi-step continuous algebra before discrete plan | **Baseline frozen weak** (LISS-0319): Ideal §2A; Host `field_compose_inject.py` (0317); H→E `field_compose_to_tonight_plan.py` (0318). **no** mid-program Continuous; **do not mark seat Y**. |

| **CH-field-fork** | Same damage/demand field → coarse bins (capital fairness) + fine bins (K-ku tonight) | Shared continuous root; dual finiteize provenance | Dual Host inject / dual `finiteize`; formulas not one typed Continuous |
| **CH-field-theory** | Theory continuous_operator + contract aligned with notebook continuous vocabulary → finite evolve | One continuous type world vs split Theory/Host paths | Theory bridge + Host MC separate (ADR 0074 / 0163) |

**Hard gates (all three):** no `measure` on continuous; no QPU continuous;
explicit finiteize (ADR 0162); spine `main_disaster_response.sqx` stays finite
dialect.

**Ship gate:** mid-program Continuous requires a **future** ship ADR beyond
[ADR 0185](../architecture/adr/0185-kernel-continuous-value.md) Lane A. This
section is expressiveness seating only.

---

## Reality checklist (hard)

Minimum system content (must remain readable in S01):

- **Ops roles:** command, field units, shelters, depots, comms/info (typed /
  modular separation)
- **Phases:** mainshock aftermath → tonight plan → field run → morning collect
  → day-2 recovery → next-night carryover (same math may reappear)
- **Finite resources:** vehicles, people, fuel, meds, bandwidth (SI-tagged)
- **Failure / degradation:** road closure, comms loss, delay, aftershock,
  fire / firestorm pressure (`when` / evolve / Host noise)
- **Auditability:** provenance for why the plan won (fail-closed / honesty)

Toy “1 node / 3 edge” graphs alone are not enough. Shrink for runtime cost —
never as an excuse for a thin domain model.

---

## Constellation chapters (scenario seats)

Pedagogy: [Accepted minimal dialect](../architecture/physicist-minimal-dialect.md).
Expressiveness review (triage Accepted 2026-08-02):
[2026-08-02-s01-expressiveness-scenario-review.md](../collaboration/reviews/2026-08-02-s01-expressiveness-scenario-review.md)
([LISS-0245](../issues/LISS-0245-s01-expressiveness-review-scenario-expansion.md) /
[LISS-0247](../issues/LISS-0247-s01-e1-locked-scenario-seats.md)).

**Spine sentence (E-lane):** Tonight corridor-vs-shelter planning tension as a
**small** spin system under named constraint Hamiltonians; one terminal plan
sample. Path: `main_disaster_response.sqx`. Coverage surfaces that are not this
sentence live in **named chapters** below — not unlabeled orphans.

### CH-tonight-spine — Tonight plan (E / Hamiltonian)

**Who / when:** K-ku HQ planning cell; Tonight (T0) and ~15 min rolls.  
**Object:** Corridor reachability vs shelter capacity tension under damage /
flood / drive Hamiltonians (`physics/constraint_h`).  
**Language:** `when` (phase / shelter), ket, Suzuki `evolve for`, sparse
`expect(ZZ)`, typed ration Classical⊕State, `impl` readiness/haul, pipe
composition, singular `measure plan0`.  
**Honesty:** No `inspect` museum on spine; no identity `evolve times`. LINEAR
sibling `|0>` discharge remains a documented language residual until a
`tracing_out` ADR. Classical `domain/` boards are **ops library objects**, not
evolving quantum systems (SE-10).

### CH-morning — Morning observation set

**Who / when:** Field command + HQ; Morning after tonight execute.  
**Object:** Official morning artifacts (shelter remaining, block pressure,
hazard, honesty/provenance tags) that feed day-2.  
**Language:** `when` / typed state / `expect` as needed; **`inspect` allowed
only as chapter peek** — preferred long-term sink is Host logs / ticket notes
(SE-01). Path: `main_morning_collect.sqx`.

### CH-day2 — Day-2 recovery

**Who / when:** All units; T+1 recovery queue.  
**Object:** Continued rescue / redeploy under updated constraint H (Suzuki S4).  
**Language:** Operator + evolve + `expect`; same inspect honesty as morning.
Path: `main_day2_recovery.sqx`.

### CH-comms — Noisy order channel (open / Lindblad)

**Who / when:** Comms desk; Tonight–Morning (C-box narrative).  
**Object:** Intermittent tower / order-channel degradation → priority list
(locked C-box toy, not full CPTP city model).  
**Language:** Lindblad-class open evolution. Path: `main_comms_channel.sqx`
(SE-07). Soft / limited placeability — label in README when running.

### CH-burst — Sensor / RF burst spectrum (circuit lane)

**Who / when:** Sensor / 119-adjacent analysis; Tonight (S-box narrative).  
**Object:** Burst spectrum → classical replan hint (not a city-wide QFT OS).  
**Language:** Circuit sub-lane — register `forEach`, QFT/IQFT/cqft Joint apply
(SE-08, SE-12). Path: `main_burst_spectrum.sqx`. Do not mix unmarked with
Hamiltonian spine teaching.

### CH-tri — Multi-command registers

**Who / when:** Multi-branch command (rescue × logistics × fire); Tonight.  
**Object:** Coupled command registers as contention / coordination carriers.  
**Language:** Multi-register / CNOT-style joint binds.
Path: `main_tri_register.sqx` (SE-09).

### CH-route — Competing corridor phases

**Who / when:** Route desk; Tonight / morning.  
**Object:** Competing corridor phase interference (secondary-disaster routing).  
**Language:** `phase` / interference / `expect`. Path:
`main_route_interference.sqx`.

### CH-lattice — Zone damage / flood field

**Who / when:** District cells; Tonight + morning.  
**Object:** Indexed zone aggregates (damage / openness / flood pressure) over
a small lattice — showcase shrink of ops-grade graph, not a toy without zones.  
**Language:** `sum`/`product`+`Index`, `Basis<N>`, lattice evolve.
Path: `main_lattice_four.sqx` + `grid/block_costs.sqx` (SE-02).

### CH-fidelity — Prior vs proposal fidelity

**Who / when:** Planning cell; Tonight roll commit gate.  
**Object:** Fidelity between prior tonight plan and new proposal before
accepting a roll.  
**Language:** `inner` / `outer` (runnable). Path:
`main_fidelity_inner_check.sqx` (SE-03).

### CH-fuel — Fuel / resource search (Non-placeable)

**Who / when:** Logistics; Tonight.  
**Object:** Fuel search / pump-until-converged under a max-step budget.  
**Language:** `evolve … until converged(…) max N`.  
**Honesty:** **Writeable ≠ placeable** on static QPU IR — soft
`E_QPU_UNSUPPORTED_CAPABILITY` expected; not a production QPU job
(SE-04, SE-11). Path: `main_fuel_search.sqx`.

### CH-host — OS shell (H-lane)

**Who / when:** Classical hosts; all phases.  
**Object:** Demand Monte Carlo inject; agency CredentialPort fail-closed;
rolling replan Job; TonightTicket JSON handoff (structured JobResult — not
stdout scrape).  
**Language:** Host Python ports / Job ABI (SE-01 Host logs; LISS-0243 ticket).
Paths: `host/demand_inject.py`, `agency_share.py`, `rolling_replan_job.py`,
`export_tonight_ticket.py`.

### Dispatch composition (spine-adjacent seats)

**SE-05 / SE-06:** Tonight dispatch desk uses priority **pipe / Partial / poly
Fusion** and Trace-Out local bumps (`protocol/compose`, `local_priority_bump`)
as composition of rescue vs haul order — coded on the tonight entry, named
here so they are not “mystery coverage.”

---

## Mapping to runnable entries

| Scenario beat | Chapter | Entry |
|---|---|---|
| Tonight plan + hazards + evolve | CH-tonight-spine | `main_disaster_response.sqx` |
| Morning observation set | CH-morning | `main_morning_collect.sqx` |
| Day-2 recovery (Suzuki S4) | CH-day2 | `main_day2_recovery.sqx` |
| Noisy order channel | CH-comms | `main_comms_channel.sqx` |
| Sensor / RF burst (circuit) | CH-burst | `main_burst_spectrum.sqx` |
| Multi-command registers | CH-tri | `main_tri_register.sqx` |
| Competing corridor phases | CH-route | `main_route_interference.sqx` |
| Zone Index / Basis lattice | CH-lattice | `main_lattice_four.sqx` |
| Prior vs proposal fidelity | CH-fidelity | `main_fidelity_inner_check.sqx` |
| Fuel search (Non-placeable until) | CH-fuel | `main_fuel_search.sqx` |
| Host MC / credentials / job / ticket | CH-host | `host/*.py` |

Full language coverage index: [scorecard](staqex-v1-s01-coverage-scorecard.md).
SE-13 (non-identity `evolve times` replan tick) remains **optional** and is
**not** locked until a real hop body is specified.
