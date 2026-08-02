# Staqex Basics examples

Language axioms, syntax, and policy — **one concept per folder**.

## Who is this for?

- **Students** learning why Staqex forbids classical `if`, early collapse, and
  script-style top-level code.
- **Physicists** checking that Hamiltonians, evolution, and measurement stay on
  the `State<T>` boundary before reading Applied toys.

Complete **B01 → B08** before jumping to [Applied](../applied/). Multi-file
linking (B09) and QPU lanes (B10–B11) assume that foundation.

**Surface face (WP-0088 + WP-0089):** single-file basics use
`// staqex-profile: experiment` (ADR 0176) — physics lines first, not package /
`main` theater. B08 is the chalk north star. Prefer `struct`/`enum` for
parameters; keep `class` for systems that own evolving physics.
**B09** is multi-file on purpose (`package examples.basics…`); that is the
module lesson, not the default notebook face.
See [surface modernization north star](../../docs/architecture/surface-modernization-north-star.md)
and [package-root-naming](../../docs/architecture/package-root-naming.md).

**Failure kinds (B03):** world-line `Err` labels ≠ Host Job failure ≠ QPU
capability reject — [ADR 0175](../../docs/architecture/adr/0175-failure-glossary.md).

## Curriculum

| ID | Topic | You will see |
|----|--------|--------------|
| [B01](B01_never_leave_the_state/) | Never Leave the State | `State<T>`, `dirac`, terminal `measure` |
| [B02](B02_when_not_if/) | `when` not `if` | mixture branches, no classical collapse |
| [B03](B03_failure_worldline/) | Failure as world-line | `Err` paths without exceptions |
| [B04](B04_evolve_not_loops/) | `evolve` not loops | unitary repetition, `expect` |
| [B05](B05_phase_interference/) | Phase and interference | `phase`, `interfer`, Born rule |
| [B06](B06_type_first_dimensions/) | Type-First dimensions | `(L,M,T)` tags on classical floats |
| [B07](B07_structure_visibility/) | Structure and visibility | `struct`/`enum` packs; `class` as physical system (not DTO) |
| [B08](B08_operators_hamiltonians/) | Operators and Hamiltonians | `evolve under H`, `expect`, `measure … tracing_out` |
| [B09](B09_multi_file_modules/) | Multi-file `import` | `domain/` + `operators/` layout |
| [B10](B10_static_qpu_lane/) | Static QPU lane | `QubitRegister`, `forEach` |
| [B11](B11_qft_registers/) | QFT on a register | `qft` / `iqft` |
| [B12](B12_open_systems/) | Open systems | `DensityState`, `lindblad`, `JumpSet` |
| [B13](B13_host_job_api/) | Host Job API | `submit_source`, `JobResult` |
| [B14](B14_resource_profile/) | Resource profile | `staqex.toml`, simulator budget |
| [B15](B15_multi_register/) | Multi-register | `system`, `RegisterSet`, qualified sites |

**Complete:** B01–B15 Basics track (catalog v2).

## Suggested paths

| Audience | Order |
|----------|--------|
| Student | B01 → … → B10 → [A06](../applied/A06_topological_edge_memory/) → [A09](../applied/A09_qkd_corridor/) → [A10](../applied/A10_mission_observatory/) |
| Theorist | B08 → B11 → B12 → A06 → [A07](../applied/A07_open_system_sensor/) → [A03](../applied/A03_h2_vqe/) → A10 |

Authority: [`docs/specs/staqex-examples-catalog-v2.md`](../../docs/specs/staqex-examples-catalog-v2.md) §7.

## Run

```bash
python3 -m compiler.staqex run examples/basics/B01_never_leave_the_state/never_leave_the_state.sqx --seed 0
```
