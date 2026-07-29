# Phase 4.1 — QPU OpenQASM transpiler

Status: **Scaffold implemented** (2026-07-23).

| Path | Role |
|------|------|
| `compiler/staqex/backend/qasm/` | `QASM3Emitter`, lower, router, topology |
| CLI | `staqex run --target qpu:openqasm3 [-o out.qasm]` |
| Tests | `SV-11` (prompt's "SV-09_qasm" — numbering offset: examples already own SV-09) |

```bash
python3 -m compiler.staqex run --target qpu:openqasm3 \
  examples/03_quantum_information/portable_bell_qpu.staqex -o /tmp/bell.qasm
```

Next: Phase 4.2 GPU backend interface.
