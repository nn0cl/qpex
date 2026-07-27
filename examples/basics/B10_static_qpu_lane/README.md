# B10 — Static QPU lane

Teaches `QubitRegister<N>`, `system()`, and `forEach` static elaboration (ADR 0069).

```bash
python3 -m compiler.qpex run examples/basics/B10_static_qpu_lane/main_static_qpu_lane.qpex --seed 0
python3 -m compiler.qpex emit-qasm examples/basics/B10_static_qpu_lane/main_static_qpu_lane.qpex
```

Legacy source: `examples/17_static_register_foreach/`.
