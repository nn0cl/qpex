# 09 — Complex simulations (module layout)

## Import / class status (honest)

| Feature | Spec (ADR 0024) | Kernel today |
|---------|-----------------|--------------|
| `package` / `import` syntax | Yes | **Parsed only** |
| User `.qpex` → `.qpex` symbol resolution | Designed | **Not implemented** |
| `class` fields / methods | Designed | **Stub** (body skipped) |
| `public fun` library calls | Designed | **Only `main` runs** |
| `import qpex.math.*` | Prelude facade | Works as no-op / Math facade |

So: **you cannot yet split classes/constants across files and `import` them into `main`.**
The files under `models/` and `operators/` are **layout + API contracts** for the
forthcoming module linker (ADR 0054). The **runnable** program is
`main_quantum_walk.qpex` (self-contained, ADR 0053 surface).

## Layout

```text
examples/09_complex_simulations/
├── README.md
├── models/
│   ├── walk_environment.qpex   # API contract (class stub)
│   └── coin_parameters.qpex
├── operators/
│   └── walk_operators.qpex     # API contract (fun stubs)
└── main_quantum_walk.qpex      # runnable DTQW (coin ⊗ Int position)
```

## Physics in `main_quantum_walk.qpex`

Discrete-time quantum walk (not continuous $x$-grid + `walk_shift` — those
carriers do not compose in MVP):

\[
U_{\mathrm{step}} = S\,(C\otimes I),\quad
C = R_y(\pi/2)\ \text{via}\ \tfrac{1}{\sqrt2}(X+Z),\quad
S=\texttt{walk\_shift}
\]

Fifty unitary steps, then terminal `measure` on position. `expect` is
inspected only (never measured).
