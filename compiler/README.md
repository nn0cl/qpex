# QPex compiler (Phase 2–3)

| Module | Role |
|--------|------|
| `qpex/lexer.py` / `parser.py` / `typecheck.py` | Frontend |
| `qpex/runtime/` | Joint Kernel evaluator |
| `qpex/stdlib/` | Prelude, `Math.*`, I/O sinks |
| `qpex/ir/` | Computation DAG IR (ADR 0032) |
| `qpex/cli.py` | `run` / `check` / `inspect` / `dag` / `repl` |

```bash
python3 -m compiler.qpex run -e 'state x = coin()
state y = x + x
measure y' --seed 0

python3 -m compiler.qpex check main.qpex
python3 -m compiler.qpex inspect main.qpex
python3 -m compiler.qpex dag --dot main.qpex
python3 -m compiler.qpex repl

python3 tests/spec_verification/run_all.py
```
