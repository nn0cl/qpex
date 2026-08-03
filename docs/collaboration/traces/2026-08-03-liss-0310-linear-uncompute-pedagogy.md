# AI work trace: LISS-0310 LINEAR uncompute pedagogy

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `feature/liss-0310-linear-uncompute-pedagogy` |
| Issue | [LISS-0310](../../issues/LISS-0310-linear-uncompute-pedagogy.md) |

## Done

- Converted official ritual `|0>` / vacuum hand-kills to ADR 0173 discharge:
  - **tracing_out live leftovers:** QMD, A01 (targets), A02 (b0/b1/x), A03, A04
    (b0/b1), A05, A10 (site), B15
  - **plain measure** (root already moved): A07, A08, A09, B09, B11, B12,
    S01 comms
- `surface-style-guide.md` §6a + PR checklist bullet
- Re-review residual §5.4 marked done

## Verification

```bash
python3 -m compiler.staqex run --seed 0 \
  examples/showcase/quantum_matter_discovery/main_quantum_matter_discovery.sqx \
  examples/applied/A01_quantum_attention_toy/main_quantum_attention_toy.sqx \
  examples/applied/A02_robot_graph_planner/main_robot_graph_planner.sqx \
  examples/applied/A03_h2_vqe/main_h2_vqe.sqx \
  examples/applied/A04_hp_protein_folding/main_hp_protein_folding.sqx \
  examples/applied/A05_qaoa_portfolio/main_qaoa_portfolio.sqx \
  examples/applied/A07_open_system_sensor/main_open_system_sensor.sqx \
  examples/applied/A08_entangled_compute_ancilla/main_entangled_compute_ancilla.sqx \
  examples/applied/A09_qkd_corridor/main_qkd_corridor.sqx \
  examples/applied/A10_mission_observatory/main_mission_observatory.sqx \
  examples/basics/B09_multi_file_modules/main_multi_file_modules.sqx \
  examples/basics/B11_qft_registers/main_qft_registers.sqx \
  examples/basics/B15_multi_register/main_multi_register.sqx
# all exit 0

.venv/bin/python -m pytest \
  tests/test_qasm3_codegen.py::test_portable_bell_via_compiler -q
# 1 passed
```
