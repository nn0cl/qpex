# LISS-0082 integrated Slice E Phase 1 Red trace

Date: 2026-07-30
Branch: `feature/liss-0082-slice-e-red-codex`
Phase: integrated Phase 1 Red only

## Scope

This is the single LISS-level Red packet for Slice E. It crosses the completed
Physics work and the Semantic boundary in one deterministic suite:

```text
source fixture
  -> compile_source / HIR
  -> lower_hir_to_physics_ir
  -> Equation/Unit DTO verification
  -> source-backed Physics golden verification
  -> QuantumSemanticInput
  -> Semantic lowering
  -> one Semantic verifier result
```

The suite covers source/evidence identity, stale golden rejection,
operation-scoped exactness, linear-resource preservation, nested provenance
closure, verifier integration, no silent repair, and raw HIR rejection. These
are integrated acceptance dimensions, not separate phase gates.

## Expected Red

The current provisional Slice E implementation cannot satisfy the integrated
contract. It lacks Physics evidence references, operation-scoped exactness,
linear-resource evidence DTOs, nested provenance checks, and the module-level
verifier handoff. The expected failures are assertion/API failures, not test
editing or production changes.

## Boundaries

The test uses existing LISS-0115/0116/0117 APIs as upstream fixtures but does
not modify them. Semantic lowering must receive Physics IR plus reviewed
evidence and must not inspect raw HIR, AST, pipeline, provider, target, RNG,
or measurement-sink objects.

## Stop condition

Stop after Red verification. Phase 2 Green requires review of this one
integrated LISS-0082 Red suite. No downstream Issue implementation is
authorized by this packet.
