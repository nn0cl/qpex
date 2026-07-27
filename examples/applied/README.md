# Applied examples (v2 catalog)

Applied track entries under `examples/applied/` per
[`docs/specs/qpex-examples-catalog-v2.md`](../../docs/specs/qpex-examples-catalog-v2.md).

Each folder includes a README with an **Honesty** table. Bibliography sections cite
**verified** primary references only.

## Status

| ID | Folder | Status |
|----|--------|--------|
| A06 | `A06_topological_edge_memory` | **done** |
| A08 | `A08_entangled_compute_ancilla` | **done** |
| A09 | `A09_qkd_corridor` | **done** |
| A10 | `A10_mission_observatory` | **done** |
| A01 | `A01_quantum_attention_toy` | planned (P2, gated) |
| A02 | `A02_robot_graph_planner` | planned (P1) |
| A03 | `A03_h2_vqe` | planned (P1) |
| A04 | `A04_hp_protein_folding` | planned (P2) |
| A05 | `A05_qaoa_portfolio` | planned (P1) |
| A07 | `A07_open_system_sensor` | planned (P2) |

## Run

```bash
python3 -m compiler.qpex run examples/applied/A06_topological_edge_memory/main_topological_edge_memory.qpex --seed 0
```
