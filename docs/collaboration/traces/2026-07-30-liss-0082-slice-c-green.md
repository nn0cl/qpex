# LISS-0082 Slice C — Phase 2 Green

- Date: 2026-07-30
- Branch: `feature/liss-0082-slice-c-red-codex`
- Operating path: Feature Path
- Issue: LISS-0082
- Scope/phase: Slice C transformation regions / Phase 2 Green
- Approval: Adjudicator message `承認` after Slice C Phase 1 Red
- Implementation permission: minimum implementation for reviewed Red only
- Tests changed: none
- Post-review required: Phase 3 Refactor approval

## Green result

Implemented the smallest API required by the reviewed Red assertions in
`compiler/staqex/quantum_semantic_ir.py`:

- immutable `RegionValidity` with exactly `Declared`, `Verified`, and
  `Required` states;
- immutable `UnitaryRegion`, `IsometryRegion`, and `ChannelRegion` DTOs with
  provider-neutral value/space signatures and provenance;
- additive `QuantumSemanticModule.regions` tuple;
- region identity definition-site participation;
- deterministic signature checks for known values/spaces, pure/density carrier
  categories, unchanged unitary space, isometry dimension relation, and
  density channel output;
- explicit isometry validity obligation when the output space is larger.

No matrix, amplitude, density payload, execution engine, proof synthesis,
measurement, control, lowering, pipeline, or provider behavior was added.

## Verification

- Slice C Red: **10 passed / 0 failed**;
- Slice A: passed;
- Slice B: passed;
- Slice B follow-up 1: **10 passed / 0 failed**;
- reviewed tests: unchanged (`git diff -- tests/` is empty);
- `py_compile`: passed;
- `git diff --check`: passed.

## Review points

- The implementation uses proposed diagnostic names
  `QSEM_REGION_SIGNATURE_INVALID` and `QSEM_REGION_VALIDITY_INVALID`.
- Mixed-state unitary lifting remains unimplemented because it was not in the
  reviewed Red assertions.
- Channel physicality is represented as a validity boundary only; no proof or
  matrix verification is attempted.
- Region graph ordering, cycle detection, measurement, control, and lowering
  remain outside this phase.

## Stop condition

Stop after Green. Do not begin Phase 3 Refactor or Slice D. Request explicit
Refactor approval after review of the implementation and the two proposed
diagnostic names.
