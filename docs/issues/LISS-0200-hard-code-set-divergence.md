# LISS-0200: Two diverged hard-diagnostic sets let 72 hard codes bypass the execution gate

## Metadata

- Local issue ID: LISS-0200
- Status: **complete** — 2026-08-01 (WP-0074)
- Phase: phase-0-design
- Type: bug
- Priority: P1
- Planning size: M
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Code: `compiler/staqex/run.py`, `compiler/staqex/pipeline.py`, `compiler/staqex/cli.py`

## Intent

The Kernel maintains two independent "which diagnostics are fatal" sets. They
have drifted, so a program the compiler calls hard-failed can still be executed.

## Evidence (reproduced 2026-08-01)

| Set | Location | Size | Gates |
|---|---|---|---|
| `_HARD_CODES` | `pipeline.py` | 110 | `CompileResult.ok`, module-link short circuit, `host.submit_*` |
| `HARD_CODES` | `run.py` | 42 | `run.run_source` / `run.run_path`, `cmd_inspect`, `cmd_emit_qasm`, `cmd_run --emit-qasm` |

- **72 codes are in `pipeline` but not in `run`** — including the whole
  `EFFECT_*`, `PIPE_*`, `BINDER_*`, `PHASE_SCOPE_*`, `DISCRETIZATION_*`,
  POVM / mixed-state, and `LINEAR_DUPLICATE_USE` / `LINEAR_IMPLICIT_DISCARD` /
  `UNCOMPUTE_WITNESS_MISSING` families, plus `HOST_TYPE_IN_KERNEL_ERROR`,
  `UNSUPPORTED_QPEX_VERSION`, `RETIRED_OPERATOR_INDEX_SYNTAX`.
- **`CONFIG_HARVEST_COLLISION_ERROR` is in `run` but not `pipeline`** — the
  divergence runs both ways.

Reproduction, using the `EFFECT_VIOLATION_ERROR` program from
[LISS-0199](LISS-0199-check-command-false-ok.md):

- `compile_source(src).ok` → `False`
- `run.run_source(src, seed=0)` → `compile_ok=True`, and returns
  `MeasureResult(value=0.0, …)` — the rejected program ran to a measurement.

`compiler.staqex.host.run_source` (what the `staqex run` CLI actually calls)
gates on `compiled.ok` and is correct. The exposed hole is the
`compiler.staqex.run` entry point.

## Why this matters beyond the API surface

The spec-verification harness imports the under-gated entry point directly:

- `tests/spec_verification/suites/sv07_kernel_eval.py` → `run_source`
- `tests/spec_verification/suites/sv09_examples.py` → `run_path`, `run_source`
- `tests/spec_verification/suites/sv31_module_linker.py` → `run_path`

so SV can execute and PASS a program carrying a hard diagnostic. The published
SV report is therefore weaker than it reads.

## Adjudicator decision points

1. Single source of truth: derive both from one module, or from
   [`staqex-v1-diagnostic-catalog.md`](../specs/staqex-v1-diagnostic-catalog.md)?
2. Tightening the gate will newly fail programs and suites that pass today.
   Confirm that is accepted, and confirm the ordering against the regression
   Issues (LISS-0202…LISS-0207) so the delta stays measurable.
3. Is `CONFIG_HARVEST_COLLISION_ERROR` genuinely hard? It must land in exactly
   one answer, not two.

## Exit

- [x] One authoritative hard-code set; no second literal set in the tree
- [x] Consistency check that fails when a code is hard in one place only
- [x] SV suites gate on the same judgement as the compiler
- [x] Red test asserts `run_source` refuses a program with any hard code

## Non-goals

Changing `check` reporting (LISS-0199); reclassifying individual diagnostics as
hard or soft beyond the single `CONFIG_HARVEST_COLLISION_ERROR` question.
