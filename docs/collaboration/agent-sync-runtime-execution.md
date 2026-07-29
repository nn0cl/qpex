# Agent sync addendum: runtime execution model (ADR 0032)

Date: 2026-07-23.

## Lock

- No Promise/`async` VM for object-language compute.
- Build DAG → defer → data-parallel eval at `measure`.
- Host async I/O only at lift/sink boundaries.

Canonical: `docs/architecture/staqex-runtime-execution-model.md`.
Kernel PoC may stay eager single-thread.
