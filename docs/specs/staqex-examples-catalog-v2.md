# Staqex official examples catalog v2

| Field | Value |
|-------|-------|
| Status | Proposed — acceptance spec for [LISS-0106](../issues/LISS-0106-examples-catalog-v2-refresh.md) |
| Normative until | Adjudicator approves LISS-0106 and Phase 1 Red begins |
| Supersedes layout | `examples/01`–`17` numeric folders (content may migrate) |
| Conformance target | Shipping Kernel v0.1 (`docs/specs/staqex-language-specification.md`) |
| Related | [examples-catalog-conventions.md](../collaboration/examples-catalog-conventions.md) |

## 1. Purpose

Provide a two-track official catalog:

1. **Basics** — teach Staqex axioms, syntax, and language policy without
   application narrative.
2. **Applied** — demonstrate research- and industry-themed **toy models** that
   use shipping Kernel surfaces honestly.

This document is the acceptance authority for folder names, learning order,
migration from the legacy catalog, bibliography policy, and Honesty boundaries.
It does **not** authorize Kernel semantic changes.

## 2. Layout

```text
examples/
├── README.md                 # index + learning paths
├── basics/
│   ├── B01_never_leave_the_state/
│   ├── B02_when_not_if/
│   └── …
├── applied/
│   ├── A01_quantum_attention_toy/
│   ├── A02_robot_graph_planner/
│   └── …
└── (no legacy archive by default; rely on git history)
```

### Naming

| Track | Folder pattern | Package pattern |
|-------|----------------|-----------------|
| Basics | `Bnn_snake_topic/` | `com.staqex.examples.basics.<topic>` |
| Applied | `Ann_snake_topic/` | `com.staqex.examples.applied.<topic>` |

Entry file: `main_<topic>.sqx` (multi-file) or `<topic>.sqx` (single-file).

### Multi-file layout (Applied and B09+)

```text
examples/<track>/<ID>_<topic>/
├── domain/
├── operators/
├── main_<topic>.sqx
└── README.md          # required for Applied; required for B09+
```

## 3. Bibliography and citation policy

Applied READMEs MUST include a **Bibliography** subsection.

| Tag | Meaning | May appear in README? |
|-----|---------|----------------------|
| **Verified** | Title, authors, year, and venue checked against primary source | Yes |
| **TBD** | Placeholder until Red-phase literature review | No (catalog spec only) |
| **Survey** | Review/survey used for context, not replication claim | Yes, with scope note |

Rules:

- Do not invent paper titles, author lists, or venue names.
- Do not claim replication of a paper's numerical results unless the example
  README states the exact simplification and a verification note exists.
- A01 attention-specific primary citation remains **TBD** until Adjudicator
  consultation; use only **Verified** survey entries until then.

### Verified references (safe to cite in READMEs)

| ID | Citation | Typical use |
|----|----------|-------------|
| R-VQE-2014 | Peruzzo, A. et al. "A variational eigenvalue solver on a quantum processor." *Nature Communications* **5**, 4213 (2014). | A03 |
| R-MOL-2017 | Kandala, A. et al. "Hardware-efficient variational quantum eigensolver for small molecules." *Nature* **549**, 242–246 (2017). | A03 (context) |
| R-QAOA-2014 | Farhi, E., Goldstone, J., Gutmann, S. "A Quantum Approximate Optimization Algorithm." arXiv:1411.4028 (2014). | A05 |
| R-GROVER-1996 | Grover, L. K. "A fast quantum mechanical algorithm for database search." *STOC* (1996). | A02, A04 |
| R-QWALK-2003 | Kempe, J. "Quantum random walks – an introductory overview." *Contemporary Physics* **44** (4), 307–327 (2003). | A02 |
| R-QWALK-SEARCH-2003 | Childs, A. M. et al. "Exponential algorithmic speedup by a quantum walk." *STOC* (2003). | A02 (graph search context) |
| R-SSH-1979 | Su, W. P., Schrieffer, J. R., Heeger, A. J. "Solitons in polyacetylene." *Phys. Rev. Lett.* **42**, 1698 (1979). | A06 |
| R-HP-1989 | Lau, K. F., Dill, K. A. "A lattice statistical mechanics model of the conformational and sequence spaces of proteins." *Macromolecules* **22**, 3986–3997 (1989). | A04 |
| R-BB84-1984 | Bennett, C. H., Brassard, G. "Quantum cryptography: Public key distribution and coin tossing." *Proceedings of IEEE International Conference on Computers, Systems and Signal Processing* (1984). | A09 (pedagogy only; not full protocol) |
| R-LINDBLAD-1976 | Lindblad, G. "On the generators of quantum dynamical semigroups." *Communications in Mathematical Physics* **48**, 119–130 (1976). | A07 |
| R-VQA-SURVEY-2021 | Cerezo, M. et al. "Variational quantum algorithms." *Nature Reviews Physics* **3**, 625–644 (2021). | A01, A03, A05 (survey) |
| R-PQC-ML-2019 | Benedetti, M. et al. "Parameterized quantum circuits as machine learning models." *Quantum Science and Technology* **4**, 043001 (2019). | A01 (survey) |

### TBD references (do not cite in README until verified)

| ID | Topic | Notes |
|----|-------|-------|
| TBD-A01-ATTN | Quantum attention / self-attention circuits | Select one primary source at A01 Red review; do not claim GPT-scale inference |
| TBD-A05-PORT | Industry portfolio optimization case study | Optional second citation; Farhi QAOA is sufficient for toy demo |
| TBD-A04-QFOLD | Quantum optimization for lattice folding beyond HP model | Out of scope unless Adjudicator expands A04 |

## 4. Basics track (B01–B16)

One concept per folder. No Honesty table unless Adjudicator requests it.

| ID | Folder | Teaches | Primary legacy source |
|----|--------|---------|----------------------|
| B01 | `B01_never_leave_the_state` | `State<T>`, `dirac`, terminal `measure` | new (minimal) |
| B02 | `B02_when_not_if` | Axiom 3, mixture, no classical `if` | `02/double_slit` |
| B03 | `B03_failure_worldline` | `Success`/`Error`, `project`, no exceptions | new |
| B04 | `B04_evolve_not_loops` | `evolve times N`, unitary repetition | `02/ket_evolve_expect` |
| B05 | `B05_phase_interference` | `phase`, `interfer`, `cis`, Born | `02/double_slit`, `08/gauge_symmetry` |
| B06 | `B06_type_first_dimensions` | `(L,M,T)`, `Length`, `Delta<Time>` | `01/phase_space`, `05/classical_oscillator` |
| B07 | `B07_structure_visibility` | `namespace`/`enum`/`struct`/`class`/`pub`/`_` | `10/domain/*` |
| B08 | `B08_operators_hamiltonians` | `hop`, `evolve under H`, Suzuki policy | `10/operators/*`, `06/quantum_ising` |
| B09 | `B09_multi_file_modules` | `import`, `domain/`/`operators/` | `09_complex_simulations` |
| B10 | `B10_static_qpu_lane` | `QubitRegister`, `forEach`, `emit-qasm` | `17_static_register_foreach` |
| B11 | `B11_qft_registers` | `qft`/`iqft` on static register | `16/qpu/portable_observatory_link` |
| B12 | `B12_open_systems` | `DensityState`, `lindblad`, `JumpSet` | `16` Lindblad slice |
| B13 | `B13_host_job_api` | Host `submit_source` / `JobResult` (Python helper) | `16/run_as_job.py` |
| B14 | `B14_resource_profile` | resource manifest / budget (LISS-0062/0063) | new |
| B15 | `B15_multi_register` | `RegisterSet`, named registers (LISS-0067) | new (overlaps A08 pedagogy) |
| B16 | `B16_effect_marking` | `effects { Inspect }` on free helper (ADR 0081) | new (LISS-0306) |

**Optional deferral:** B13–B15 shipped in WP-0027 Wave 2 (2026-07-27); B16 LISS-0306.

## 5. Applied track (A01–A11)

Every folder MUST include:

1. **Story** — one paragraph, toy scale explicit.
2. **Honesty table** — per conventions doc.
3. **Bibliography** — **Verified** entries only.
4. **Kernel surfaces** — bullet list of demonstrated ops/types.
5. **Run** — `check`, `run`, and QPU commands where applicable.

| ID | Folder | Story (toy) | Verified bibliography | Legacy reuse | Priority |
|----|--------|-------------|----------------------|--------------|----------|
| A01 | `A01_quantum_attention_toy` | 2–4 qubit variational circuit inspired by attention-like QML; **not** LLM inference | R-PQC-ML-2019, R-VQA-SURVEY-2021; primary attention paper **TBD** | `03/controlled_unitary`, `03/mixed_control` | P2 |
| A02 | `A02_robot_graph_planner` | Discrete configuration-space graph; DTQW + Grover oracle; not real-time control | R-QWALK-2003, R-QWALK-SEARCH-2003, R-GROVER-1996 | `07`, `09`, `15`, `04` | P1 |
| A03 | `A03_h2_vqe` | Minimal H₂-style VQE / molecular Hamiltonian demo | R-VQE-2014, R-MOL-2017, R-VQA-SURVEY-2021 | `06` patterns + LISS-0032 fermion surface | P1 |
| A04 | `A04_hp_protein_folding` | 2D HP lattice ground-state search | R-HP-1989, R-GROVER-1996 | `14` alphabet narrative → HP lattice | P2 |
| A05 | `A05_qaoa_portfolio` | Small QUBO portfolio selection | R-QAOA-2014, R-VQA-SURVEY-2021 | `06`, `12` graph → financial graph | P1 |
| A06 | `A06_topological_edge_memory` | SSH edge state as pedagogical topological memory | R-SSH-1979 | `10_topological_physics` | P0 |
| A07 | `A07_open_system_sensor` | Lindblad detector / decoherence toy | R-LINDBLAD-1976 | `16` Lindblad + `cpu/continuous_models` | P2 |
| A08 | `A08_entangled_compute_ancilla` | Named registers + Bell link (LISS-0067) | Bell/Grover pedagogy from `03`; optional R-VQA-SURVEY-2021 context | `03/portable_bell_qpu`, `13` | P0 |
| A09 | `A09_qkd_corridor` | Bell correlations / QKD intuition; not full BB84 | R-BB84-1984 (pedagogy), `03` Bell demos | `13_deep_space_qkd` | P0 |
| A10 | `A10_mission_observatory` | Slim integration capstone: modules + lanes | inherits per-module refs from A06–A09 | `16_quantum_observatory` (slim integration) | P0 |
| A11 | `A11_noether_forge` | Static Noether / conservation-law forge slice | inherits Kernel surface refs from A06–A10 pedagogy | new | P1 |

### A01 scope guardrail (fixed)

Always enforce:

- README MUST state **No** for "GPT-scale LLM inference on QPU".
- README MUST state **Yes** for named Kernel surfaces only (e.g. `Param<Angle>`,
  `expect`, `capply`, small register).
- Do not use "transformer", "LLM", or model-parameter counts implying billions
  of weights.
- Preferred wording: "attention-**inspired** variational circuit" or
  "QML feature map demo".

### A10 capstone discipline (from LISS-0020)

Retain LISS-0020 coverage matrix semantics:

- Each row maps to a **named module** and a verification case.
- CPU / QPU / Host lanes remain explicit.
- Keep A10 as an integration read path; avoid re-expanding into a kitchen sink.
- A10 does not become the only place a surface is documented; B01–B15 and
  A01–A11 remain canonical for their topics.

## 6. Legacy migration map

| Legacy path | Disposition |
|-------------|-------------|
| `01_classical_mechanics` | → B06 |
| `02_quantum_basics` | → B02, B04, B05 |
| `03_quantum_information` | → B10/B11 helpers, A08, A09 |
| `04_quantum_algorithms` | → A02, A04 |
| `05_harmonic_oscillator` | → B06 helper; A07 continuous reference |
| `06_statistical_physics` | → B08, A03, A05 |
| `07_quantum_walk` | → **merge** into A02 |
| `08_gauge_symmetry` | → B05 |
| `09_complex_simulations` | → B09 |
| `10_topological_physics` | → A06 |
| `11_shor_rsa_toy` | drop from official v2 unless direct slices are reused in another entry |
| `12_city_route_search` | → **absorb** into A02/A05; do not keep clone |
| `13_deep_space_qkd_toy` | → A09 |
| `14_genome_motif_grover` | → **absorb** into A04 |
| `15_orbital_mesh_walk` | → **absorb** into A02 |
| `16_quantum_observatory` | → A10 (integration capstone) |
| `17_static_register_foreach` | → B10 |

## 7. Learning paths

### Student path

`B01 → B02 → B03 → B04 → B05 → B06 → B07 → B08 → B09 → B10 → A06 → A09 → A10`

### Theorist path

`B08 → B11 → B12 → A06 → A07 → A03 → A10`

### Industry / seminar path

`B10 → B11 → A05 → A08 → A09` (+ Honesty tables required)

### QML path (after A01 gate)

`B10 → B11 → A01` (only after Adjudicator approves A01 bibliography and wording)

## 8. SV registration (successor to SV-09)

During migration, maintain a single allowlist (update `sv09_examples.py` or
successor module) listing every official **entry** `main_*.sqx` or single-file
`.sqx`.

Rules carry forward from [examples-catalog-conventions.md](../collaboration/examples-catalog-conventions.md):

- Multi-file entries use `compile_path` / `run_path`.
- Pedagogy-only files excluded from SV MUST be listed in folder README.
- `examples/README.md` and every track folder README MUST exist before merge.

## 9. Honesty table template (Applied)

```markdown
| Claim | Status |
|-------|--------|
| Production / real-world scale | **No** — toy model (state size here) |
| Replicates cited paper numerically | **No** / **Partial** (explain) |
| Kernel surface demonstrated | **Yes** — list ops |
| QPU execution on real hardware | **No** — OpenQASM sketch / local Job only |
| LLM / clinical / industrial robot control | **No** (when applicable) |
```

## 10. Out of scope for this catalog

- Full Shor factorization at cryptographic scale
- Complete BB84 protocol implementation
- AlphaFold-class protein structure prediction
- GPT-class or frontier LLM inference
- Real-time robot manipulator control loops
- Provider credentials, cloud submit, or benchmark claims against hardware

## 11. Acceptance checklist (LISS-0106)

- [ ] Adjudicator approves this spec as Phase 1 Red authority
- [ ] §5 and §6 decisions reflected in migration PR notes
- [ ] LISS-0107 closed before linked migration
- [ ] All Applied README bibliographies use **Verified** entries only
- [ ] SV successor suite PASS after full migration
