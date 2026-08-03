# AI work trace: LISS-0296 surface adoption residual

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `feature/liss-0296-surface-adoption-residual` |
| Issue | [LISS-0296](../../issues/LISS-0296-surface-adoption-residual.md) |

## Done

- Applied selective import: A02, A04, A06, A07, A09, A10
- A06: `band_gap` / `topological_index` free fns; `SSHSystem.step` remains
- Friction ledger §5 post-0295/0296
- WP-0089 post-WP residual note

## Verification

```bash
for m in \
  A02_robot_graph_planner/main_robot_graph_planner \
  A04_hp_protein_folding/main_hp_protein_folding \
  A06_topological_edge_memory/main_topological_edge_memory \
  A07_open_system_sensor/main_open_system_sensor \
  A09_qkd_corridor/main_qkd_corridor \
  A10_mission_observatory/main_mission_observatory
do
  python3 -m compiler.staqex run --seed 0 "examples/applied/${m}.sqx"
done
```
