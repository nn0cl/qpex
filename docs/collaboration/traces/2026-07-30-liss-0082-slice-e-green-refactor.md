# LISS-0082 Slice E Green/Refactor trace

Date: 2026-07-30
Branch: `feature/liss-0082-slice-e-red-codex`

## Green

Phase 2 added the minimum provider-neutral exactness and lowering surface to
`compiler/staqex/quantum_semantic_ir.py`: `Exact`,
`ApproximationRequired`, `FiniteCarrierEvidence`, `QuantumSemanticInput`, and
an immutable lowering result. The lowering retains only reviewed finite acting
spaces and provenance, and emits named diagnostics for missing evidence,
incomplete provenance, and absent approximation obligations. No AST, evaluator,
pipeline, numerical method, mapping, encoding, or provider boundary was added.

## Refactor

The behavior-preserving cleanup extracted finite-evidence diagnostics and
exactness diagnostics into two focused pure helpers. The lowering function now
coordinates input validation, immutable module construction, and the two
diagnostic passes without changing their order, keys, messages, or codes.

The six reviewed Slice E assertions were not changed. Existing Slice A–D and
gap 3 behavior remains covered by the same deterministic suites.

## Verification gap

The finite-carrier evidence DTO and lowering result are new local vocabulary
chosen from the accepted contract because the contract specifies the boundary
but not a shipped Python signature. Their public names and whether the
lowering result should later be folded into a broader compile result require
human review before Slice F or pipeline work. No implementation chooses a
discretization or numerical approximation policy.
