# QPex compiler (Phase 2–4)

| Module | Role |
|--------|------|
| `qpex/lexer.py` / `parser.py` / `typecheck.py` | Frontend |
| `qpex/runtime/` | Joint Kernel evaluator |
| `qpex/stdlib/` | Prelude, `Math.*`, I/O sinks |
| `qpex/ir/` | Computation DAG IR (ADR 0032) |
| `qpex/codegen/` | OpenQASM 3 emit scaffold (ADR 0036) |
| `qpex/cli.py` | `run` / `check` / `inspect` / `dag` / `emit-qasm` / `repl` |

```bash
python3 -m compiler.qpex run --target cpu -e 'state x = coin()
state y = x + x
measure y' --seed 0

python3 -m compiler.qpex emit-qasm examples/03_quantum_information/portable_bell_qpu.qpex
python3 -m compiler.qpex run --target qpu:ibm_eagle \
  examples/03_quantum_information/portable_bell_qpu.qpex

python3 tests/spec_verification/run_all.py
```
