# LISS-0082 Slice C — Phase 1 Red

- Date: 2026-07-30
- Branch: `feature/liss-0082-slice-c-red-codex`
- Operating path: Feature Path
- Issue: LISS-0082
- Scope/phase: Slice C transformation regions / Phase 1 Red
- Approval: Adjudicator message `承認` after Slice C design intake
- Implementation permission: tests only; no production implementation
- Post-review required: review the failing assertions before Phase 2 Green

## Red result

Added `tests/test_quantum_semantic_ir_slice_c_red.py` with ten acceptance
tests covering the reviewed Slice C boundary:

- `UnitaryRegion`: pure carrier and same acting-space signature;
- invalid unitary space/carrier changes;
- `IsometryRegion`: finite non-decreasing dimension relation;
- explicit environment/ancilla validity obligation;
- `ChannelRegion`: pure or density input and density output;
- rejection of pure channel output / hidden purification;
- distinct `Declared`, `Verified`, and `Required` validity states;
- no promotion of an unverified declaration to `Verified`;
- region identity/provenance participation at definition sites.

The tests deliberately contain no matrices, amplitudes, density payloads,
execution, proof synthesis, measurement, control, lowering, pipeline, or
provider behavior.

## Observed failure

The suite fails before assertions because the new Slice C API is not yet
implemented:

```text
cannot import name 'ChannelRegion'
from 'compiler.staqex.quantum_semantic_ir'
```

The same missing-API failure is reported for all ten test entry points:

```text
0 passed, 10 failed
```

This is an authentic Red state. No assertion was weakened to manufacture the
failure, and no production file was changed.

## Verification

- `python3 tests/test_quantum_semantic_ir_slice_c_red.py`: expected Red,
  0 passed / 10 failed;
- `python3 -m py_compile tests/test_quantum_semantic_ir_slice_c_red.py`:
  passed;
- `git diff --check`: passed;
- `git diff -- compiler/ tests/`: no production-file change; only the new Red
  test is present.

## Stop condition

Stop after Phase 1 Red. Do not modify `compiler/`, do not begin Green, and do
not begin Slice D. Phase 2 requires explicit review and approval of these
acceptance tests.
