# 09 — Complex simulations (module layout)

## Import / class status (ADR 0054)

| Feature | Spec | Kernel |
|---------|------|--------|
| `package` / `import` syntax | Yes | Parsed |
| User `.qpex` → `.qpex` symbol resolution | ADR 0054 | **`compile_path` / `run_path`** |
| `class` Type-First fields | ADR 0054 | Linked into entry `main` |
| `public fun` library calls | ADR 0054 | Measure-free calls from `main` / `evolve` |
| `import qpex.math.*` | Prelude facade | No-op / Math facade |

Runnable entry: `main_quantum_walk.qpex` (multi-file DTQW).

## Layout

```text
examples/09_complex_simulations/
├── README.md
├── models/
│   ├── walk_environment.qpex   # Length / Delta<Time> / n_steps
│   └── coin_parameters.qpex     # Float theta
├── operators/
│   └── walk_operators.qpex     # Coin + step_quantum_walk
└── main_quantum_walk.qpex      # import + evolve times 50
```

## Physics

Discrete-time quantum walk on Int position (not Float grid + `walk_shift`):

\[
U_{\mathrm{step}} = S\,(C\otimes I),\quad
C = R_y(\pi/2)\ \text{via}\ \tfrac{1}{\sqrt2}(X+Z),\quad
S=\texttt{walk\_shift}
\]

Fifty unitary steps via imported `step_quantum_walk`, then terminal
`measure` on position. `expect` is inspected only (never measured).
