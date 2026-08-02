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
Tonight spine passed LISS-0246 dialect strip (no inspect flood; no identity
`evolve times`; fuel `until` → `main_fuel_search.sqx`). LINEAR leftovers use
`measure … tracing_out …` (ADR 0173) — not ritual `|0>` discharge. Type-First
fields retain units (ADR 0174). Residual Class **E** is mostly pedagogy noise
(FQN length, multi-lane labeling), not missing Kernel seats. New showcase PRs
must not *increase* dialect debt.

## A — Required (indexed)

| Surface | Phase | Evidence path | Notes |
|---|---|---|---|
| `when` (not `if`) | tonight / morning / day2 | `main_*.sqx` | coin + enum |
| named Float / struct → Operator | tonight / day2 | `physics/constraint_h.sqx` | `ConstraintCoeffs` |
| `expect` / `inspect` | tonight / morning / day2 / chapters | spine `expect`; morning/day2/satellites sparse `inspect` on expect peeks | Float-tag inspect floods removed (LISS-0248); Host preferred (SE-01) |
| typed `state` | spine | `main_disaster_response.sqx` | `State<Int>` ration |
| multi-file import | all | package imports under S01 | |
| NLTS + `measure` | each runnable main | `main_*.sqx` | |
| ket + `evolve for` | tonight / day2 | `main_disaster_response.sqx` | Identity `evolve times` **removed** from spine (LISS-0246) |
| Operator + Suzuki | tonight S2 / day2 S4 | constraint_h + mains | |
| OOP + visibility | domain / physics | `struct` + `_pad` | classical packs ≠ blackboard dialect |
| LINEAR | all runnable mains | `measure … tracing_out …` | Kernel + S01 constellation ([LISS-0250](../issues/LISS-0250-measure-tracing-out-red.md)–[0252](../issues/LISS-0252-s01-chapters-tracing-out.md) / [ADR 0173](../architecture/adr/0173-measure-tracing-out-leftover-policy.md)); prep `|0>` ket binds remain |
| Ports | runtime | Kernel `RngPort` / `MeasureSinkPort` / `SourcePort` (ADR 0166) + `host/*.py` | shipped WP-0082–0084 |
| fail-closed | host | agency_share / Abort budget | **H-lane** |

## B — Shipped extensions (satellites / libraries)

| Surface | Phase | Evidence path | Notes |
|---|---|---|---|
| `sum`/`product`+`Index` | grid / lattice4 | `grid/block_costs.sqx`, `main_lattice_four.sqx` | satellite / grid — not “the OS” |
| `Basis<N>` | lattice4 | `basis_zone_sum` | LISS-0230 |
| `inner`/`outer` | fidelity | `main_fidelity_inner_check.sqx` | **run** (LISS-0229); satellite |
| `evolve … until` | fuel chapter | `main_fuel_search.sqx` | Non-placeable satellite (LISS-0246); soft QPU IR |
| phase / interference | routes / morning | satellite mains | |
| Type-First + SI | domain | quantities + Rankine `.R` / troy `.oz_t` | field units retained ([ADR 0174](../architecture/adr/0174-type-first-field-units.md) **Accepted**; [LISS-0254](../issues/LISS-0254-type-first-field-units-red.md) **complete**) |
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

**Pedagogy residuals (Accepted dialect):** LISS-0244 / 0245 triage / 0246 / 0247 /
0248 (R3 chapter align) **complete**. [ADR 0173](../architecture/adr/0173-measure-tracing-out-leftover-policy.md)
+ Kernel [LISS-0250](../issues/LISS-0250-measure-tracing-out-red.md) + S01 samples
[LISS-0251](../issues/LISS-0251-s01-spine-tracing-out.md)–[0252](../issues/LISS-0252-s01-chapters-tracing-out.md)
**complete** (ritual `|0>` discharge removed via `measure … tracing_out …`).
[ADR 0174](../architecture/adr/0174-type-first-field-units.md) Type-First fields
**Accepted** ([LISS-0253](../issues/LISS-0253-adr-0174-type-first-field-units.md));
Kernel + S01 heal [LISS-0254](../issues/LISS-0254-type-first-field-units-red.md)
**complete** (Phase 3 2026-08-02). Docs sync [LISS-0255](../issues/LISS-0255-s01-docs-hygiene-post-0254.md).
Expressiveness brush-up: [WP-0087](../work-plans/WP-0087-s01-expressiveness-brushup.md)
**complete + post_reviewed** (LISS-0255–0260; Adjudicator「承認」2026-08-02).
Failure glossary [ADR 0175](../architecture/adr/0175-failure-glossary.md)
**Accepted**.
