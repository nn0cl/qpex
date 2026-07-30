# LISS-0082 Slice D — Phase 1 Red

- Date: 2026-07-30
- Worktree: `/private/tmp/qpex-liss-0082-slice-d`
- Branch: `feature/liss-0082-slice-d-red-codex`
- Operating path: Feature Path
- Issue: LISS-0082
- Scope/phase: Slice D lanes, measurement, parameters, resources / Phase 1 Red
- Approval: Adjudicator approval of all five Slice D design decisions and one
  combined D1–D3 Red review unit
- Implementation permission: tests only; no production implementation
- Post-review required: review the Red API and assertions before Phase 2 Green

## Red result

Added `tests/test_quantum_semantic_ir_slice_d_red.py` with sixteen acceptance
tests in the three approved groups:

- D1: closed Static/Dynamic lanes, coherent factor-selected control, no generic
  control/static-selection node, and Dynamic marker rejection from Static;
- D2: terminal measurement without reusable output, post-measure use
  rejection, Dynamic state/token pairing, and exactly one merge;
- D3: parameter shape independence, four explicit ancilla discharge variants,
  missing-discharge rejection, uncompute evidence without inverse synthesis,
  and Slice D identity/provenance participation.

## Observed failure

The existing module correctly has no generic control or static-selection API,
so that guard is already green. The remaining tests fail because the reviewed
Slice D API does not exist:

```text
cannot import name 'AncillaDischarge'
from 'compiler.staqex.quantum_semantic_ir'
```

Observed summary:

```text
1 passed, 15 failed
```

The one pass is a guard against adding an ambiguous control node; it is not
evidence that Slice D is implemented.

## Verification

- Slice D: expected Red, 1 passed / 15 failed;
- Slice A: passed;
- Slice B: passed;
- Slice B follow-up 1: 10 passed / 0 failed;
- Slice B gap 3: 4 passed / 0 failed;
- Slice C: 10 passed / 0 failed;
- `py_compile` for the new Red test: passed;
- `git diff --check`: passed;
- `compiler/`: unchanged.

## Stop condition

Stop after Phase 1 Red. Do not modify `compiler/`, do not begin Green, and do
not begin Slice E. Phase 2 requires explicit review and approval of this Red
API and all sixteen tests.
