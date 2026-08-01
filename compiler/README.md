# Staqex compiler (shipping Kernel)

Python package under `compiler/staqex/` — the runnable implementation of the
language surface exercised by `examples/` and SV suites.

| Module | Role |
|--------|------|
| `lexer.py` / `parser.py` / `typecheck.py` | Frontend |
| `modules.py` / `access.py` | Import linker + `pub` / `_` visibility (ADR 0054 / 0058) |
| `runtime/` | Joint Kernel evaluator (`struct` copy / `class` ref / `fun init`) |
| `stdlib/` | Prelude, `Math.*`, I/O sinks |
| `ir/` | Computation DAG IR (ADR 0032) |
| `codegen/` / `codegen_qasm.py` | OpenQASM 3 (`OpenQASM3Generator`, `StaqexCompiler.compile_to_qasm3`) |
| `backend/qasm/` | Circuit lower / route / emit (ADR 0036) |
| `cli.py` | `run` / `check` / `inspect` / `dag` / `emit-qasm` / `repl` |

```bash
python3 -m compiler.staqex emit-qasm examples/applied/A08_entangled_compute_ancilla/main_entangled_compute_ancilla.sqx
python3 -c "from compiler.staqex import StaqexCompiler; print(StaqexCompiler().compile_to_qasm3('examples/applied/A08_entangled_compute_ancilla/main_entangled_compute_ancilla.sqx'))"
python3 tests/test_qasm3_codegen.py
python3 tests/spec_verification/run_all.py
```

Human entry: repo-root `QUICKSTART.md`. Design harmony:
`docs/architecture/physicist-dx-harmony.md`.
