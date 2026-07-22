# ADR 0054: User-module import resolution

## Status

**Accepted** (2026-07-23). Implemented in Kernel.

Companions: ADR 0024 (packages / `import` surface). Verification: **SV-31**.

## Context

`import` and `class` were parsed (ADR 0024 DX) but not linked:

1. Import paths were not resolved to other `.qpex` files.
2. `class` bodies were skipped (no fields).
3. Only `public fun main` executed — library `fun` was not callable.

## Decision

1. Entry `compile_path(file)` / `run_path(file)` walks `import` edges under the
   entry package directory (stdlib `qpex.*` skipped).
2. Library units export `Operator` binds (from `public fun` bodies) and
   Type-First `class` fields into the entry `main` environment.
3. `class` bodies accept Type-First fields only (`Length`, `Delta<Time>`, …).
4. Cross-file `public fun` calls are measure-free Joint transformers; usable
   from `main` binds and as `evolve … times N { fun(…) }` results.
5. Cycles → `MODULE_CYCLE_ERROR`; missing files → `MODULE_NOT_FOUND_ERROR`.

## See also

- **[ADR 0061](0061-classical-module-config-harvest.md)** (Proposed) — classical
  `Float`/`Int` config harvest; closes the DX hole documented by examples
  11–14 sync comments ([LISS-0005](../../issues/LISS-0005-classical-module-config-harvest.md)).

## Consequences

`examples/09_complex_simulations/` is a real multi-file DTQW program.
Single-string `compile_source` remains for tests / REPL (no import linking).
Classical config in library modules is **not** harvested until ADR 0061.

## Verification

SV-31 — import graph, symbol merge, class fields, library fun call,
`main_quantum_walk.qpex` linked run.
