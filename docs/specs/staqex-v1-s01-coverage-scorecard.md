# S01 coverage scorecard (constellation index)

| Field | Value |
|---|---|
| Showcase | `examples/showcase/S01_quantum_disaster_response/` |
| Role | **Constellation index** — each row cites where a surface appears. This is **not** proof that one `main` is a disaster OS |
| Pedagogy | [Accepted minimal dialect](../architecture/physicist-minimal-dialect.md); [S01 redesign](staqex-v1-s01-redesign-toward-minimal-dialect.md); honesty slice [LISS-0244](../issues/LISS-0244-s01-r1-dialect-honesty-readme-scorecard.md) |
| Rule | Every **In** row must cite path + phase; blank = fail |
| Out | Kernel Continuous; Joint rational; trait specialization; live QPU SDK; CUDA |
| Runtime honesty | `inner`/`outer` **runnable** (LISS-0229). `qft`/`iqft`/`cqft` **Joint apply** (LISS-0228) + QPU IR |

**Dialect vs scorecard:** green rows do not equal dialect-clean teaching.
Tonight spine still carries Class **E** sample debt (inspect flood; LINEAR
`|0>` kills; identity / soft `until` on spine) until S01-R2+. New showcase PRs
must not *increase* that debt (destructive-simplification sample policy).

## A — Required (indexed)

| Surface | Phase | Evidence path | Notes |
|---|---|---|---|
| `when` (not `if`) | tonight / morning / day2 | `main_*.sqx` | coin + enum |
| named Float / struct → Operator | tonight / day2 | `physics/constraint_h.sqx` | `ConstraintCoeffs` |
| `expect` / `inspect` | tonight / morning / day2 / phase | `main_*.sqx` | `inspect` flood on spine = Class E (demote per dialect) |
| typed `state` | spine | `main_disaster_response.sqx` | `State<Int>` ration |
| multi-file import | all | package imports under S01 | |
| NLTS + `measure` | each runnable main | `main_*.sqx` | |
| ket + `evolve for/times` | tonight / day2 | `main_disaster_response.sqx` | identity `times` on spine = Class E |
| Operator + Suzuki | tonight S2 / day2 S4 | constraint_h + mains | |
| OOP + visibility | domain / physics | `struct` + `_pad` | classical packs ≠ blackboard dialect |
| LINEAR | spine | discharge then measure | hand `|0>` kill = Class E until `tracing_out` ADR |
| Ports | runtime | Kernel `RngPort` / `MeasureSinkPort` / `SourcePort` (ADR 0166) + `host/*.py` | shipped WP-0082–0084 |
| fail-closed | host | agency_share / Abort budget | **H-lane** |

## B — Shipped extensions (satellites / libraries)

| Surface | Phase | Evidence path | Notes |
|---|---|---|---|
| `sum`/`product`+`Index` | grid / lattice4 | `grid/block_costs.sqx`, `main_lattice_four.sqx` | satellite / grid — not “the OS” |
| `Basis<N>` | lattice4 | `basis_zone_sum` | LISS-0230 |
| `inner`/`outer` | fidelity | `main_fidelity_inner_check.sqx` | **run** (LISS-0229); satellite |
| `evolve … until` | fuel | `main_disaster_response.sqx` | soft QPU IR — Non-placeable; spine debt |
| phase / interference | routes / morning | satellite mains | |
| Type-First + SI | domain | quantities + Rankine `.R` / troy `.oz_t` | sell demoted until fields carry units |
| pipe / Partial / poly Fusion | compose | `compose_priority` / `compose_pair` / `compose_poly` | |
| Trace-Out fn | compose | `local_priority_bump` | LISS-0230 |
| Lindblad | comms | `main_comms_channel.sqx` | toy satellite |
| QFT / cqft apply | burst | `main_burst_spectrum.sqx` | **circuit sub-lane** satellite (LISS-0228) |
| Host Job / Credential / MC | host | `host/*.py` | **H-lane** |
| multi-register | tri | `main_tri_register.sqx` | satellite |
| `impl` interface dispatch | tonight | `readiness_of` / `haul_score` | LISS-0231 |
| Classical⊕State | spine | typed ration | |

## Runnable verification (seed 0)

| Entry | Command |
|---|---|
| Tonight spine | `…/main_disaster_response.sqx` |
| Morning / Day2 | morning / day2 mains |
| Lattice4 | `…/main_lattice_four.sqx` |
| Burst / fidelity | burst + **run** fidelity |
| Host | demand_inject / agency_share / rolling_replan_job |

## Residuals

WP-0072 Issues LISS-0228..0232 **complete**. Post-S01 Kernel hygiene used by
this tree: multi-hole Partial pipe lhs move (LISS-0238), Qutrit `apply(I)`
(LISS-0239), observe-sink `to` vs unit convert (LISS-0240), blocking pytest +
spec-verification CI (WP-0080 / WP-0086).

**Pedagogy residuals (Accepted dialect):** LISS-0244 (R1 honesty) **complete**;
spine strip S01-R2+ still open per redesign sketch.
