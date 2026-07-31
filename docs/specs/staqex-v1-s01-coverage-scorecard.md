# S01 coverage scorecard (shipped A+B)

| Field | Value |
|---|---|
| Showcase | `examples/showcase/S01_quantum_disaster_response/` |
| Rule | Every **In** row must cite path + phase; blank = fail |
| Out | Kernel Continuous; Joint rational; trait specialization; live QPU SDK; CUDA |
| Honesty | `inner`/`outer` = **compile-surface** (`check`); Joint runtime Call not yet green — runnable fidelity uses `expect(ZZ,…)` |

## A — Required

| Surface | Phase | Evidence path | Notes |
|---|---|---|---|
| `when` (not `if`) | tonight / morning / day2 | `main_disaster_response.sqx`, `main_morning_collect.sqx`, `main_day2_recovery.sqx` | |
| named Float / struct → Operator | tonight / day2 | `physics/constraint_h.sqx` | congestion/fairness coeffs |
| `expect` / `inspect` | tonight / morning / day2 / phase | `main_*.sqx` | ZZ / Z monitors |
| typed `state` | spine | `main_*.sqx` | |
| multi-file import | all | package imports under S01 | |
| NLTS + `measure` | each runnable main | `main_*.sqx` | one terminal measure each |
| ket + `evolve for/times` | tonight / day2 | `main_disaster_response.sqx`, `main_day2_recovery.sqx` | |
| Operator + Suzuki | tonight S2 / day2 S4 | `physics/constraint_h.sqx` + mains | |
| OOP + visibility | domain | `domain/*.sqx` | |
| LINEAR | spine | uncompute then measure in mains | |
| Ports | runtime | Kernel `run` + `host/*.py` | Rng/Source/MeasureSink via CLI |
| fail-closed | host | `host/agency_share.py`, Abort budget in `host/rolling_replan_job.py` | |

## B — Shipped extensions

| Surface | Phase | Evidence path | Notes |
|---|---|---|---|
| `sum`/`product`+`Index` | grid | `grid/block_costs.sqx` | Index\<0..3\> |
| `inner`/`outer` | fidelity (check) | `main_fidelity_inner_check.sqx` | `staqex check` only; runtime Call NYI |
| `evolve … until` | fuel narrative | `main_disaster_response.sqx` | QPU IR soft unsupported; Joint runs |
| phase / interference | routes | `main_route_interference.sqx`, `physics/interference.sqx` | |
| Type-First L,M,T,I,Θ | domain | `domain/quantities.sqx`, shelters/roads/comms | |
| SI `to` + mixed promote | domain | `domain/quantities.sqx`, recovery/roads | |
| pipe / Partial / Fusion | compose | `protocol/compose.sqx` | free fn `compose_priority` |
| Lindblad / DensityState | comms | `main_comms_channel.sqx` | toy only |
| QFT / cqft | burst | `main_burst_spectrum.sqx` | |
| static QPU lane / honesty | provenance | `provenance/honesty.sqx` | no live submit |
| soft Physics / QSEM | provenance | soft diags on run (non-hard) | |
| Host Job API | host | `host/rolling_replan_job.py` | |
| Resource profile | host | `STAQEX_S01_ABORT_BUDGET=1` path | |
| multi-register | physics | `main_tri_register.sqx`, `physics/tri_register.sqx` | |
| static forEach | burst | `main_burst_spectrum.sqx` | |
| classical Fraction→f64 | rations | `domain/rations.sqx` (`2/3`, `1/4`) | |
| CredentialPort | host | `host/agency_share.py` | |
| Host MC inject + labels | host | `host/demand_inject.py` | bin_midpoint |
| basic `impl` | domain | `domain/capabilities.sqx` | no specialization |
| Classical⊕State | spine | ration/med wires in primary | |
| CPU data-parallel workers | host CLI | `STAQEX_DATA_PARALLEL_WORKERS` in rolling job | |

## Runnable verification (seed 0)

| Entry | Command |
|---|---|
| Tonight | `python3 -m compiler.staqex run …/main_disaster_response.sqx --seed 0` |
| Morning | `…/main_morning_collect.sqx` |
| Day2 | `…/main_day2_recovery.sqx` |
| Phase | `…/main_route_interference.sqx` |
| Comms / QFT / tri | satellite mains |
| inner check | `python3 -m compiler.staqex check …/main_fidelity_inner_check.sqx` |
| Host | `host/demand_inject.py`, `agency_share.py`, `rolling_replan_job.py` |
