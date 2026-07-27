# ADR 0054: User-module import resolution

## Status

**Accepted** (2026-07-23). Implemented in Kernel.

Companions: ADR 0024 (packages / `import` surface). Verification: **SV-31**.

## Context

`import` and `class` were parsed (ADR 0024 DX) but not linked:

1. Import paths were not resolved to other `.qpex` files.
2. `class` bodies were skipped (no fields).
3. Only `pub fn main` is executed — library `fn` is callable only through
   the defined module-linking contract.

## Decision

1. Entry `compile_path(file)` / `run_path(file)` walks `import` edges under the
   entry package directory (stdlib `qpex.*` skipped).
2. Library units export declarations and Type-First `class` fields. Function
   locals, including `Operator` binds, remain inside their lexical function
   scope (ADR 0068).
3. `class` bodies accept Type-First fields only (`Length`, `Delta<Time>`, …).
4. Cross-file `pub fn` calls are measure-free Joint transformers; usable
   from `main` binds and as `evolve … times N { fn(…) }` results.
5. Cycles → `MODULE_CYCLE_ERROR`; missing files → `MODULE_NOT_FOUND_ERROR`.

## See also

- **[ADR 0061](0061-classical-module-config-harvest.md)** — historical
  function-local harvest, superseded by ADR 0068.
- **[ADR 0060](0060-joint-coordinate-preservation.md)** (**Accepted**) — Joint
  coordinate preservation under `grover_diffuse`.

## Consequences

`examples/basics/B09_multi_file_modules/` is a real multi-file DTQW program.
Single-string `compile_source` remains for tests / REPL (no import linking).
Values produced by library functions cross the module boundary only through
explicit parameters and return values.

## Verification

SV-31 — import graph, symbol merge, class fields, library fun call,
`main_quantum_walk.qpex` linked run.
