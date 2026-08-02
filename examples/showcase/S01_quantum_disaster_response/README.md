# S01 — Ops-inspired language experiment (disaster story)

**Not a city OS.** This tree is a **language-specification / expressiveness
experiment** on a reality-first ops narrative — not a claim that a ward or
首都圏 was “solved,” optimized, or run on live QPU.

Pedagogy ruler: **[Accepted minimal dialect](../../../docs/architecture/physicist-minimal-dialect.md)**
(Experiment Kernel **E** vs Host/classical **H**). Redesign toward that dialect:
[S01 redesign sketch](../../../docs/specs/staqex-v1-s01-redesign-toward-minimal-dialect.md)
([LISS-0244](../../../docs/issues/LISS-0244-s01-r1-dialect-honesty-readme-scorecard.md) = this honesty slice).

| Field | Link |
|---|---|
| Example tree | [`examples/showcase/S01_quantum_disaster_response/`](./) |
| Examples index (last row) | [`examples/README.md`](../../README.md) |
| **Locked scenario (full story + constellation seats)** | [`staqex-v1-s01-locked-scenario.md`](../../../docs/specs/staqex-v1-s01-locked-scenario.md) |
| Mission lock | [`staqex-v1-showcase-mission-lock.md`](../../../docs/specs/staqex-v1-showcase-mission-lock.md) |
| S0 | [`staqex-v1-showcase-s0-disaster-response.md`](../../../docs/specs/staqex-v1-showcase-s0-disaster-response.md) |
| Coverage scorecard | [`staqex-v1-s01-coverage-scorecard.md`](../../../docs/specs/staqex-v1-s01-coverage-scorecard.md) (**constellation index**) |
| Issue / program | [LISS-0222](../../../docs/issues/LISS-0222-s01-quantum-disaster-response.md) · [WP-0070](../../../docs/work-plans/WP-0070-s01-quantum-disaster-response.md) |
| Coverage residuals (intake) | [WP-0072](../../../docs/work-plans/WP-0072-s01-coverage-residuals.md) · LISS-0228..0232 |

**Tonight spine (E-lane / CH-tonight-spine):**
[`main_disaster_response.sqx`](main_disaster_response.sqx) — small Joint /
Hamiltonian sketch. Dialect strip [LISS-0246](../../../docs/issues/LISS-0246-s01-r2-spine-dialect-pass.md).
Leftovers use `measure … tracing_out …`
([LISS-0251](../../../docs/issues/LISS-0251-s01-spine-tracing-out.md) /
[ADR 0173](../../../docs/architecture/adr/0173-measure-tracing-out-leftover-policy.md)).
Chapters aligned to locked seats ([LISS-0248](../../../docs/issues/LISS-0248-s01-r3-chapter-align.md)).

**Constellation chapters:** named seats in the
[locked scenario](../../../docs/specs/staqex-v1-s01-locked-scenario.md) — not
“the OS.”

## Scenario (summary)

Full text: **[locked scenario](../../../docs/specs/staqex-v1-s01-locked-scenario.md)**.

**Stage (publish):** **K-ku**（K区）— eastern Tokyo lowland ward-class HQ
(~**450,000** residents; ~**100k–120k** acute overnight). Liquefaction +
zero-meter inundation + wooden dense-area fire / firestorm risk + aftershocks.
Runtime shrinks graph; roles/data kinds stay real. *(Design archetype ward is
not named in public copy.)*

**Trigger:** Strong late-night mainshock → liquefaction / inundation / wooden
fires → outages and intermittent towers → simultaneous rescue / shelter /
supply / firefighting surge → aftershock re-damage.

**Field pain (story motivation):** fragmented info, resource contention,
unfair allocation, secondary disasters, time pressure.

**What `.sqx` actually carries today:** a **small** spin / constraint-H
experiment plus classical `domain/` packs and Host jobs — not a full
deployment MIP or city-wide QC.

**Realtime honesty:** event / rolling replan **Host jobs** — not magical
continuous city-wide quantum control.

**Machines — narrative scale (locked scenario):** K-ku / 首都圏 QPU counts in
the locked scenario are **planning fiction for hardware honesty**, not a claim
that this tree places that workload.

**Note:** shipping path today is SIM-only.

**Cycle outputs (Host / story):** tonight tickets → morning observation set
(missing stays missing) → day-2 recovery. No victim PII dumps, no live QPU
submit, no “optimal city” proof.

```text
TonightPlan → FieldExecution → MorningCollect → Day2Replan → Carryover
```

When reality and a syntax demo conflict, **reality wins**. When scorecard
coverage and the minimal dialect conflict, **dialect wins** for teaching
claims (coverage stays as an index).

## Run

```bash
# CH-tonight-spine (E-lane)
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_disaster_response.sqx --seed 0

# CH-morning / CH-day2
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_morning_collect.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_day2_recovery.sqx --seed 0

# Constellation chapters (separate terminal measure)
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_comms_channel.sqx --seed 0          # CH-comms
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_burst_spectrum.sqx --seed 0         # CH-burst (circuit)
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_tri_register.sqx --seed 0           # CH-tri
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_route_interference.sqx --seed 0     # CH-route
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_lattice_four.sqx --seed 0           # CH-lattice
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_fuel_search.sqx --seed 0            # CH-fuel (Non-placeable)
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_fidelity_inner_check.sqx --seed 0   # CH-fidelity
```

## Host companions (H-lane)

```bash
python3 examples/showcase/S01_quantum_disaster_response/host/demand_inject.py
STAQEX_AGENCY_TOKEN=demo python3 examples/showcase/S01_quantum_disaster_response/host/agency_share.py
python3 examples/showcase/S01_quantum_disaster_response/host/agency_share.py   # fail-closed
python3 examples/showcase/S01_quantum_disaster_response/host/rolling_replan_job.py
STAQEX_S01_ABORT_BUDGET=1 python3 examples/showcase/S01_quantum_disaster_response/host/rolling_replan_job.py

# Tonight ticket from Host JobResult (LISS-0243 A→B→C) — no stdout scrape
python3 examples/showcase/S01_quantum_disaster_response/host/export_tonight_ticket.py \
  --seed 0 \
  --out /tmp/tonight_ticket.json
```

`export_tonight_ticket.py` maps `JobResult.measurements` into `TonightTicket`
JSON (`schema_version: 1`). Honesty: **sim-only**, `live_qpu: false`, no
optimality claim. Vacuum / incomplete measurement exits non-zero (fail-closed;
never invents `sample_value`). Soft QPU diagnostics may still appear on the
ticket. Not a live field-dispatch system. Logs belong on Host — not as an
`inspect` flood in the spine.

## Layout

| Path | Chapter | Role |
|---|---|---|
| `main_disaster_response.sqx` | CH-tonight-spine | Tonight E-lane spine |
| `main_morning_collect.sqx` | CH-morning | Morning observation set (sparse inspect) |
| `main_day2_recovery.sqx` | CH-day2 | Day-2 recovery (Suzuki S4) |
| `main_comms_channel.sqx` | CH-comms | Noisy order channel (Lindblad toy) |
| `main_burst_spectrum.sqx` | CH-burst | Circuit / QFT burst spectrum |
| `main_tri_register.sqx` | CH-tri | Multi-command registers |
| `main_route_interference.sqx` | CH-route | Competing corridor phases |
| `main_lattice_four.sqx` | CH-lattice | Zone Index / Basis lattice |
| `main_fidelity_inner_check.sqx` | CH-fidelity | Prior vs proposal fidelity |
| `main_fuel_search.sqx` | CH-fuel | Non-placeable `evolve … until` |
| `host/` | CH-host | MC inject, CredentialPort, rolling job, ticket export |
| `domain/` | — | Classical ops packs (H-adjacent library) |
| `grid/` / `physics/` / `protocol/` / `provenance/` | — | Shared modules for chapters |

Kernel ports used by `run`: `RngPort`, `MeasureSinkPort`, `SourcePort`
(ADR 0166 / WP-0082–0084). CI gates root pytest + spec-verification
(WP-0080 / WP-0086). No live QPU SDK. Soft IR / SIM honesty only. No urban
“optimal proof” claims.
