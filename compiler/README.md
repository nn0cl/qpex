# QPex compiler (shipping Kernel)

Python package under `compiler/qpex/` — the runnable implementation of the
language surface exercised by `examples/` and SV suites.

| Module | Role |
|--------|------|
| `lexer.py` / `parser.py` / `typecheck.py` | Frontend |
| `modules.py` / `access.py` | Import linker + `pub` / `_` visibility (ADR 0054 / 0058) |
| `runtime/` | Joint Kernel evaluator (`struct` copy / `class` ref / `fun init`) |
| `stdlib/` | Prelude, `Math.*`, I/O sinks |
| `ir/` | Computation DAG IR (ADR 0032) |
| `codegen/` / `codegen_qasm.py` | OpenQASM 3 (`OpenQASM3Generator`, `QPexCompiler.compile_to_qasm3`) |
| `backend/qasm/` | Circuit lower / route / emit (ADR 0036) |
| `cli.py` | `run` / `check` / `inspect` / `dag` / `emit-qasm` / `repl` |

```bash
python3 -m compiler.qpex emit-qasm examples/03_quantum_information/portable_bell_qpu.qpex
python3 -c "from compiler.qpex import QPexCompiler; print(QPexCompiler().compile_to_qasm3('examples/03_quantum_information/portable_bell_qpu.qpex'))"
python3 tests/test_qasm3_codegen.py
python3 tests/spec_verification/run_all.py
```

Human entry: repo-root `QUICKSTART.md`. Design harmony:
`docs/architecture/physicist-dx-harmony.md`.
