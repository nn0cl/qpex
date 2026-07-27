# Applied examples (v2 catalog)

Research- and industry-**themed toys** with explicit **Honesty** tables and
**verified** bibliographies only.

## Who is this for?

- **Seminar / industry** readers who need bounded claims (no “quantum GPT”, no
  production portfolio optimizers).
- **Integrators** tracing how Basics surfaces compose in [A10](A10_mission_observatory/)
  without re-reading a kitchen-sink capstone.

Each folder is canonical for its topic — A10 is a **slim read path**, not the
only place a surface is documented.

## Catalog

| ID | Folder | Theme |
|----|--------|--------|
| [A01](A01_quantum_attention_toy/) | Attention-inspired QML toy | `capply`, `expect` — **not** LLM inference |
| [A02](A02_robot_graph_planner/) | Robot graph planner | DTQW + Grover oracle |
| [A03](A03_h2_vqe/) | H₂ VQE minimal | `FermionOperator` → `JordanWigner` |
| [A04](A04_hp_protein_folding/) | HP lattice search | Grover over conformations |
| [A05](A05_qaoa_portfolio/) | QAOA portfolio toy | one-layer QUBO / Ising |
| [A06](A06_topological_edge_memory/) | SSH edge memory | multi-file OOP + `hop` Hamiltonian |
| [A07](A07_open_system_sensor/) | Open-system sensor | Lindblad detector readout |
| [A08](A08_entangled_compute_ancilla/) | Compute–ancilla link | `RegisterSet`, Bell narrative |
| [A09](A09_qkd_corridor/) | QKD corridor | Bell correlations — not full BB84 |
| [A10](A10_mission_observatory/) | Mission observatory | slim integration capstone |

## Suggested paths

| Audience | Order |
|----------|--------|
| Industry / seminar | [B10](../basics/B10_static_qpu_lane/) → [B11](../basics/B11_qft_registers/) → A05 → A08 → A09 |
| QML curiosity | B10 → B11 → A01 (read Honesty table first) |
| Capstone reader | Basics B01–B10, then A06 → A09 → A10 |

Authority: [`docs/specs/qpex-examples-catalog-v2.md`](../../docs/specs/qpex-examples-catalog-v2.md) §7.

## Run

```bash
python3 -m compiler.qpex run examples/applied/A06_topological_edge_memory/main_topological_edge_memory.qpex --seed 0
python3 -m compiler.qpex run examples/applied/A01_quantum_attention_toy/main_quantum_attention_toy.qpex --seed 0
```
