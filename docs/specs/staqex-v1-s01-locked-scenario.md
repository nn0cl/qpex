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

## Mapping to runnable entries

| Scenario beat | Entry |
|---|---|
| Tonight plan + hazards + evolve | `main_disaster_response.sqx` |
| Morning observation set | `main_morning_collect.sqx` |
| Day-2 recovery (Suzuki S4) | `main_day2_recovery.sqx` |
| Comms noise / burst / registers / phase | satellite `main_*.sqx` |
| Host MC / credentials / rolling job | `host/*.py` |

Full language coverage: [scorecard](staqex-v1-s01-coverage-scorecard.md).
