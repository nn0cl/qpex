# LISS-0082 Slice E Phase 1 Red trace

Date: 2026-07-30
Branch: `feature/liss-0082-slice-e-red-codex`
Phase: Phase 1 Red only

## Design boundary

Slice E fixes the exactness and Physics-to-Semantic lowering boundary. The
accepted input is a narrow `QuantumSemanticInput` containing a Physics IR
module, explicit finite-carrier evidence, linear-resource evidence, a semantic
lane, and exactness obligations. Source-native or already-reviewed finite
evidence may be retained with closed provenance. Missing evidence is a named
diagnostic; the lowering must not infer a discretization, encoding, provider,
or numerical method.

`Exact` and `ApproximationRequired` are semantic markers only. The latter keeps
an obligation identity, reason, and provenance. Tolerance, numerical method,
error bound, mapping, resource estimate, and target selection remain outside
LISS-0082.

## Included and omitted context

Included: LISS-0082 Issue acceptance scenarios 1 and 7, plan Slice E, contract
§8–§10, existing Physics IR/lowering DTOs, and the immutable Semantic IR
module from Slices A–D.

Omitted: AST/evaluator/pipeline changes, provider SDKs, OpenQASM/QIR, general
discretization or mapping, numerical execution, and Algorithm Plan IR.

## Red evidence

`tests/test_quantum_semantic_ir_slice_e_red.py` defines six acceptance tests.
They intentionally reference the proposed Slice E API before production
implementation exists. The expected Red is an import failure for the missing
`ApproximationRequired`, `FiniteCarrierEvidence`, `QuantumSemanticInput`, and
lowering symbols. No `compiler/` file is changed in this phase.

## Stop condition

Stop after deterministic Red verification. Phase 2 Green requires review of
these assertions and explicit phase approval. Slice F, pipeline wiring,
provider work, and any implementation are out of scope.
