# A08 — Entangled compute–ancilla link

Demonstrates **named registers** and `RegisterSet` acting space (LISS-0067 / ADR 0105)
alongside a portable Bell-prep narrative.

Pedagogy draws on `examples/03_quantum_information/portable_bell_qpu.qpex` and
`examples/13_deep_space_qkd_toy/`.

## Honesty

| Claim | Status |
|-------|--------|
| Physical routing / provider qubit mapping | **No** |
| `system` + qualified `Z[data[0]]` sites in composite operator | **Yes** |
| Full distributed quantum compute–ancilla protocol | **No** |

## Run

```bash
python3 -m compiler.qpex check examples/applied/A08_entangled_compute_ancilla/main_entangled_compute_ancilla.qpex
python3 -m compiler.qpex run examples/applied/A08_entangled_compute_ancilla/main_entangled_compute_ancilla.qpex --seed 0
python3 -m compiler.qpex emit-qasm examples/applied/A08_entangled_compute_ancilla/main_entangled_compute_ancilla.qpex
```
