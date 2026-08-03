# B17 — Pipeline `|>`

Teaches pipe composition on State wires:

```text
state a = 3 |> bump |> dbl
state b = 5 |> add(10, _)
```

- RHS is a free function call or unary free-fn name (not `this.method`).
- Partial `_` holes: ADR 0123 / 0149 lineage.
- Showcase (S01 compose) uses the same surface with domain names.

## Run

```bash
python3 -m compiler.staqex run examples/basics/B17_pipeline_pipe/pipeline_pipe.sqx --seed 0
```
