# LISS-0082 Slice E cross-cutting redesign

Date: 2026-07-30
Branch: `feature/liss-0082-slice-e-red-codex`
Status: design draft; implementation paused pending Architecture review

## Design check

- **Scope and expected behavior:** expand Slice E from a narrow DTO/lowering
  proof into a cross-cutting proof that Physics evidence, provenance,
  exactness, linear resources, execution lanes, the Semantic verifier, and
  consumer-neutral planning projections preserve one meaning.
- **Specifications and files inspected:** LISS-0082 Issue and plan, Quantum
  Semantic IR contract §§8–10 and §14, ADR 0108, existing Physics IR/Equation
  DTOs and lowering, `quantum_semantic_ir.py`, Slice A–D tests, and testing/
  branch-discipline rules.
- **Component boundaries and candidates:** existing HIR→Physics IR lowering,
  Equation/Unit DTO and source-backed golden boundary as upstream fixtures;
  `PhysicsEvidenceRef`, finite evidence classification, operation-scoped
  exactness marker, `QuantumSemanticInput`, lowering result, resource evidence
  projection, and deterministic verifier pass. No pipeline, provider, RNG,
  sink, or adapter.
- **Constraints:** no silent discretization, no raw AST fallback, closed
  provenance, no dropped resource evidence, one diagnostic authority, no
  provider/target fields, compact hierarchy without eager expansion.
- **Ambiguities requiring Architecture decision:** whether evidence belongs in
  Physics IR or a separate boundary DTO; the identity of an exact semantic
  operation; whether `QuantumSemanticLoweringResult` is public; and how
  reviewed finite evidence is represented without trusting a free-form string.
- **Included context:** existing Physics/Semantic DTOs, accepted contract,
  current Slice E implementation, and deterministic test patterns.
- **Omitted context:** provider SDKs, numerical solvers, mapping algorithms,
  pipeline integration, controller runtime, and deployment profiles.
- **Routing:** architecture review by a strong reasoning agent; DTO/test
  conversion by a coding assistant after approval; verification by deterministic
  Python tests and golden comparison.

## Findings that caused the redesign

The first Slice E pass accepts `physics_module` and
`linear_resource_evidence` but does not consume them, treats exactness as a
module-wide marker rather than an operation obligation, and validates only the
evidence item's immediate origin. Its tests therefore prove API existence but
not source/evidence identity preservation or cross-slice verifier closure.
They also use an empty hand-built PhysicsModule, so they do not exercise the
actual HIR→Physics IR lowering, Equation/Unit provenance, or source-backed
golden loading.

## Proposed integrated work

The E0–E7 dimensions are implemented and tested together as one integrated
Slice E packet: one cross-boundary Red suite, one minimum Green implementation,
and one behavior-preserving Refactor. The arrows describe implementation
ordering inside the packet, not separate approval gates.

E0–E7 together form the expanded Slice E acceptance boundary. E6–E7 are part
of the same completion review before Slice F is reconsidered. The intended
approval sequence is one integrated Architecture approval, then Red, Green,
Refactor, and final PR/merge approvals. No implementation or test phase is
authorized by this design draft.

The integrated path is: source fixture → HIR → existing Physics IR lowering →
Equation/Unit and source-backed golden verification → `QuantumSemanticInput` →
Semantic IR lowering → one deterministic verifier result. The Semantic
lowering itself must not reparse source or inspect AST/HIR; HIR is an upstream
fixture only.
