# S01 — Quantum Disaster Response OS

**This program was written as a language-specification / expressiveness
benchmark** (shipped Staqex surfaces on a reality-first ops story — not a
syntax museum and not a claim that a city was “solved”).

| Field | Link |
|---|---|
| Example tree | [`examples/showcase/S01_quantum_disaster_response/`](./) |
| Examples index (last row) | [`examples/README.md`](../../README.md) |
| **Locked scenario (full story)** | [`staqex-v1-s01-locked-scenario.md`](../../../docs/specs/staqex-v1-s01-locked-scenario.md) |
| Mission lock | [`staqex-v1-showcase-mission-lock.md`](../../../docs/specs/staqex-v1-showcase-mission-lock.md) |
| S0 | [`staqex-v1-showcase-s0-disaster-response.md`](../../../docs/specs/staqex-v1-showcase-s0-disaster-response.md) |
| Coverage scorecard | [`staqex-v1-s01-coverage-scorecard.md`](../../../docs/specs/staqex-v1-s01-coverage-scorecard.md) |
| Issue / program | [LISS-0222](../../../docs/issues/LISS-0222-s01-quantum-disaster-response.md) · [WP-0070](../../../docs/work-plans/WP-0070-s01-quantum-disaster-response.md) |
| Coverage residuals (intake) | [WP-0072](../../../docs/work-plans/WP-0072-s01-coverage-residuals.md) · LISS-0228..0232 |

Primary entry:
[`main_disaster_response.sqx`](main_disaster_response.sqx).

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

**Field pain:** fragmented info, resource contention, unfair allocation,
secondary disasters (routes, fuel, command loss, fire/inundation spread), time
pressure.

**OS decisions (bundled):** reachability-aware deployment; shelter capacity;
supply/fuel order; comms priority; rolling replan into morning → day-2 recovery.

**Realtime honesty:** event / rolling replan **jobs** — not magical continuous
city-wide QC.

**Machines — K-ku:** build **3** QPU (P ~150–300 logical + C + S), or **1**
minimum; optional +1 P-spare. Classical hosts 1–2.

**Machines — 首都圏 cover（1都3県）:** **80** K-ku-class cells → recommended
**240** QPU (80×3), minimum **80**, HA **320**; optional regional Pᵣ **+2–4**.
Not one mega-QPU for all 首都圏.

**Note:** shipping path today is SIM-only. Details: locked scenario.

**Cycle outputs:** tonight execution tickets → morning observation set (missing
stays missing) → day-2 recovery / continued rescue. No victim PII dumps, no live
QPU submit, no “optimal city” proof.

```text
TonightPlan → FieldExecution → MorningCollect → Day2Replan → Carryover
```

When reality and a syntax demo conflict, **reality wins**.

## Run

```bash
# Tonight spine
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_disaster_response.sqx --seed 0

# Morning collect / day-2 recovery
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_morning_collect.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_day2_recovery.sqx --seed 0

# Satellite lanes (separate terminal measure)
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_comms_channel.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_burst_spectrum.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_tri_register.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_route_interference.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_lattice_four.sqx --seed 0

# Fidelity — inner/outer Joint runtime (LISS-0229)
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_fidelity_inner_check.sqx --seed 0
```

## Host companions

```bash
python3 examples/showcase/S01_quantum_disaster_response/host/demand_inject.py
STAQEX_AGENCY_TOKEN=demo python3 examples/showcase/S01_quantum_disaster_response/host/agency_share.py
python3 examples/showcase/S01_quantum_disaster_response/host/agency_share.py   # fail-closed
python3 examples/showcase/S01_quantum_disaster_response/host/rolling_replan_job.py
STAQEX_S01_ABORT_BUDGET=1 python3 examples/showcase/S01_quantum_disaster_response/host/rolling_replan_job.py
```

## Layout

| Path | Role |
|---|---|
| `main_disaster_response.sqx` | Tonight planning spine |
| `main_morning_collect.sqx` | Morning observation set |
| `main_day2_recovery.sqx` | Next-day recovery (Suzuki S4) |
| `domain/` | Ops, shelters, roads, requests, hazards, SI, Fraction, `impl` |
| `grid/` | Indexed binders |
| `physics/` | Constraint H, interference, tri-register |
| `protocol/` | Windows, pipe compose (single- + multi-hole) |
| `provenance/` | Honesty / soft IR / future target tags |
| `host/` | MC inject, CredentialPort, rolling job |
| `main_comms_channel.sqx` | Lindblad toy |
| `main_burst_spectrum.sqx` | QFT/IQFT/cqft Joint apply |
| `main_lattice_four.sqx` | Index\<0..3\> lattice evolve |
| `main_tri_register.sqx` | Multi-register |
| `main_route_interference.sqx` | Phase interference |
| `main_fidelity_inner_check.sqx` | `inner`/`outer` **runnable** |

No live QPU SDK. Soft IR / SIM honesty only. No urban “optimal proof” claims.

