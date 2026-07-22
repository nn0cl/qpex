# ADR 0054: User-module import resolution (planned)

## Status

**Proposed** (2026-07-23). Not yet implemented in Kernel.

Companions: ADR 0024 (packages / `import` surface).

## Context

`import` and `class` are parsed (ADR 0024 DX) but:

1. Import paths are not resolved to other `.qpex` files.
2. `class` bodies are skipped (no fields / methods).
3. Only `public fun main` is executed — library `fun` is not callable.

Example layout `examples/09_complex_simulations/` anticipates this ADR;
`main_quantum_walk.qpex` is self-contained until the linker lands.

## Decision (target)

1. Entry `compile_path(file)` walks `import` edges under a package root.
2. Library units export `Operator` / typed `fun` into a module env.
3. `class` gains Type-First fields (no classical islands mid-`main`).
4. Cross-file calls remain measure-free by default.

## Consequences

Until shipped: multi-file physics demos must inline into `main`, or keep
sibling files as **API contracts** only.

## Verification

Future SV-31 — import graph, symbol merge, example `09_*` linked run.
