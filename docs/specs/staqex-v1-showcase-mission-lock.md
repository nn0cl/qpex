# Staqex showcase mission lock (Gate P2)

| Field | Value |
|---|---|
| Status | **Superseded lock** (2026-08-01) — Adjudicator authorized Disaster Emergency OS retheme |
| Prior lock | Noether Forge / quantum-matter (2026-07-31) — **superseded** |
| Issue | [LISS-0222](../issues/LISS-0222-s01-quantum-disaster-response.md) |
| Program | [WP-0070](../work-plans/WP-0070-s01-quantum-disaster-response.md) |
| Prerequisites | P0/P1 complete; prior S1 matter slice salvage only |
| Authority | [rebaseline](staqex-v1-representative-program-rebaseline.md) Gate P2 reopen |
| Review | [2026-08-01-s01-disaster-architecture-approval.md](../collaboration/reviews/2026-08-01-s01-disaster-architecture-approval.md) |

## Locked mission

**Theme:** **Quantum Disaster Response OS** — **K-ku** (K区) ward-class
emergency command after a major capital-region earthquake (liquefaction,
zero-meter inundation, wooden dense-area fire / firestorm risk, aftershocks,
outages, competing rescue / shelter / supply / comms). **首都圏（1都3県）**
scale-out is **80** K-ku-class grid cells (not one mega-job; not 関東七県同一粒度).

**Purpose:** This path is a **language-specification / expressiveness
benchmark** on a reality-first product story.

**One-sentence public brief:** A command-room OS that explores many response
plans at once under physical constraints, inspects without collapsing mid-plan,
ingests demand noise via Host finiteization, confirms one executable plan per
planning window, and carries morning data into next-day recovery — with
honest simulator / slightly-future QPU targeting.

**Path:** [`examples/showcase/S01_quantum_disaster_response/`](../../examples/showcase/S01_quantum_disaster_response/)

**Locked scenario (full story):**
[`staqex-v1-s01-locked-scenario.md`](staqex-v1-s01-locked-scenario.md)

**Not locked (rejected / out):**
- Kernel `Continuous` mid-program values (Host MC inject only);
- Joint rational masses (classical Fraction path only);
- trait specialization / effect-row expansion (basic `impl` OK);
- live QPU provider SDK / CUDA GPU workers;
- kitchen-sink syntax tourism without operational spine;
- claiming a city-wide proven optimum.

**Salvage:** `examples/showcase/quantum_matter_discovery/` and
`examples/applied/A11_noether_forge/` are optional salvage only — not
authoritative.

## Bounded contexts (DDD / CA)

| Context | Responsibility | Ports |
|---|---|---|
| Domain / ops model | Districts, units, shelters, depots, SI quantities | none external |
| Physics / planning | Constraint Hamiltonians, evolve, expect, interference | Kernel only |
| Application / protocol | Tonight → morning collect → next-day replan windows | Host Job / inject |
| Provenance / honesty | SIM vs slightly-future static CH*/NH5; soft IR | MeasureSink |
| Inter-agency | External inventory gated by CredentialPort | Host credentials |

## Coverage binding

**All shipped surfaces** in the language coverage ledger **A+B rows** of the
S0 scorecard must appear in S01 (or be explicitly demoted). Usage count is
unlimited. Design-boundary rows remain out.

See [S0 specification](staqex-v1-showcase-s0-disaster-response.md).

## Size / honesty / realtime

- Reality-first domain model; shrink graph for runtime, not for thin domain.
- Target scale: ~1k–3k LOC coherent spine (pad-free).
- Operational near-real-time = event / rolling replan jobs — not continuous
  global quantum optimality.
- Soft `QSEM_*` / Physics IR allowed; not hard failure.

## Exit of this lock

- [x] Theme locked (Disaster Emergency OS)
- [x] Prior Noether Forge lock superseded
- [x] Path `S01_quantum_disaster_response` named
- [x] Coverage = full shipped A+B scorecard
- [x] Successor S0 issued
