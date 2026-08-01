# S01 coverage scorecard (shipped A+B)

| Field | Value |
|---|---|
| Showcase | `examples/showcase/S01_quantum_disaster_response/` |
| Rule | Every **In** row must cite path + phase; blank = fail |
| Out | Kernel Continuous; Joint rational; trait specialization; live QPU SDK; CUDA |
| Honesty | `inner`/`outer` **runnable** (LISS-0229). `qft`/`iqft`/`cqft` **Joint apply** (LISS-0228) + QPU IR |

## A — Required

| Surface | Phase | Evidence path | Notes |
|---|---|---|---|
| `when` (not `if`) | tonight / morning / day2 | `main_*.sqx` | coin + enum |
| named Float / struct → Operator | tonight / day2 | `physics/constraint_h.sqx` | `ConstraintCoeffs` |
| `expect` / `inspect` | tonight / morning / day2 / phase | `main_*.sqx` | |
| typed `state` | spine | `main_disaster_response.sqx` | `State<Int>` ration |
| multi-file import | all | package imports under S01 | |
| NLTS + `measure` | each runnable main | `main_*.sqx` | |
| ket + `evolve for/times` | tonight / day2 | `main_disaster_response.sqx` | |
| Operator + Suzuki | tonight S2 / day2 S4 | constraint_h + mains | |
| OOP + visibility | domain / physics | `struct` + `_pad` | |
| LINEAR | spine | discharge then measure | |
| Ports | runtime | Kernel `run` + `host/*.py` | |
| fail-closed | host | agency_share / Abort budget | |

## B — Shipped extensions

| Surface | Phase | Evidence path | Notes |
|---|---|---|---|
| `sum`/`product`+`Index` | grid / lattice4 | `grid/block_costs.sqx`, `main_lattice_four.sqx` | 2-wire tonight + **Index\<0..3\>** satellite |
| `Basis<N>` | lattice4 | `basis_zone_sum` | LISS-0230 |
| `inner`/`outer` | fidelity | `main_fidelity_inner_check.sqx` | **run** (LISS-0229) |
| `evolve … until` | fuel | `main_disaster_response.sqx` | soft QPU IR |
| phase / interference | routes / morning | satellite mains | |
| Type-First + SI | domain | quantities + Rankine `.R` / troy `.oz_t` | LISS-0230 |
| pipe / Partial / poly Fusion | compose | `compose_priority` / `compose_pair` / `compose_poly` | |
| Trace-Out fn | compose | `local_priority_bump` | LISS-0230 |
| Lindblad | comms | `main_comms_channel.sqx` | toy |
| QFT / cqft apply | burst | `main_burst_spectrum.sqx` | LISS-0228 |
| Host Job / Credential / MC | host | `host/*.py` | |
| multi-register | tri | `main_tri_register.sqx` | |
| `impl` interface dispatch | tonight | `readiness_of` / `haul_score` | LISS-0231 |
| Classical⊕State | spine | typed ration | |

## Runnable verification (seed 0)

| Entry | Command |
|---|---|
| Tonight | `…/main_disaster_response.sqx` |
| Morning / Day2 | morning / day2 mains |
| Lattice4 | `…/main_lattice_four.sqx` |
| Burst / fidelity | burst + **run** fidelity |
| Host | demand_inject / agency_share / rolling_replan_job |

## Residuals

WP-0072 Issues LISS-0228..0232 **complete** on this batch.
