# LISS-0067: Multi-register acting-space and QPU mapping

## Metadata

- Local issue ID: LISS-0067
- GitHub issue: none
- Status: Phase 3 Refactor complete — review pending
- Phase: Feature Path — Phase 3 Refactor complete
- Type: language type boundary / QPU IR mapping
- Priority: P1
- Initial planning size: L
- Owner/agent: Codex
- Depends on: LISS-0058, LISS-0041, LISS-0065, LISS-0066, ADR 0069,
  ADR 0102
- Related work plan: WP-0004

## Summary

Define the semantic boundary for systems containing more than one named
quantum register. The design must preserve each register's identity and size
through operator values, tensor-product composition, simulator materialisation,
QPU IR, resource accounting, and Host result provenance.

This is a language and provider-neutral design task. It does not select a
cloud provider, physical-qubit routing algorithm, authentication mechanism, or
SDK.

## [DESIGN CHECK]

- Scope and expected behavior: represent a finite collection of statically
  sized named registers, compose their Hilbert spaces in a deterministic
  tensor-product order, type-check operators acting on one or more registers,
  and preserve logical register identity through QPU IR and Host result
  metadata.
- Specifications and files inspected: LISS-0058, ADR 0102, ADR 0069,
  LISS-0041, LISS-0065, LISS-0066, `compiler/qpex/static_hilbert.py`, QPU IR
  DTOs, and the existing observation/result contracts.
- Component boundaries, ports/adapters, and VO/DTO candidates: candidate
  semantic values are `RegisterId`, `RegisterShape`, `RegisterSet`,
  `TensorProductShape`, and `LogicalQubitRef`. The Kernel owns shape and
  operator compatibility; QPU IR carries resolved logical references and
  provenance; Host/provider adapters may later resolve physical topology but
  do not redefine logical meaning.
- Applicable constraints: no bare integer acting-space fallback, no implicit
  register merging, no dynamic register allocation, no provider SDK, and no
  physical routing policy in the Kernel. Existing single-register
  `QubitRegister<N>` semantics must remain stable.
- Decisions, assumptions, and unresolved ambiguities: ADR 0105 accepts a
  declarative `system` shape, `RegisterSet<SystemName>`, register-qualified
  indexing, source declaration order, logical-plus-flat QPU IR identity,
  split shape checks, and invariant composite acting spaces. Remaining
  implementation details must not introduce implicit register selection.
- Included and omitted AI context: included LISS-0058/ADR 0102, static
  Hilbert and QPU IR boundaries, Host orchestration, and observation results;
  omitted provider SDK documentation, credentials, physical device topology,
  and live execution data.
- Task routing: strong architectural review for type and mapping boundaries;
  deterministic compiler/IR contract tests only after Phase 1 approval.
- Input/output evidence contract: the design output is a semantic boundary
  map, candidate value objects, accepted invariants, and explicit open
  decisions. No provider-specific or AI-derived mapping claim is trusted
  without human review.
- Verification plan: compare candidate representations against the existing
  single-register type and QPU IR contracts, then request Phase 1 Red only
  after ADR 0105 is accepted.

## Proposed invariants

1. Every register has a stable source-level identity and a positive static
   size.
2. A multi-register system has one explicit tensor-product ordering; consumers
   must not infer ordering from declaration hash or source traversal accident.
3. A cross-register operator records all registers it acts on.
4. Flattening logical qubits for QPU IR is a derived mapping with provenance,
   never a replacement for register identity.
5. Total logical qubit count is the sum of register sizes; Hilbert dimension is
   the product of their dimensions.
6. Unknown register identity, ambiguous ordering, or incompatible acting space
   is a hard diagnostic. No one-register fallback is permitted.

## Resolved decisions

See [ADR 0105](../architecture/adr/0105-multi-register-acting-space-and-qpu-mapping.md):
declarative system shape, `RegisterSet<SystemName>`, qualified indexing,
source-order tensor products, provenance-preserving logical/flat QPU identity,
split shape checks, and invariant composite acting spaces.

## Non-goals

- Provider SDK, credentials, authentication, network transport, or live QPU.
- Physical-qubit placement, routing, coupling-map optimization, or calibration.
- Dynamic register creation or runtime-sized Hilbert spaces.
- New operator algebra, Dirac notation, POVM, or dynamic measurement syntax.
- Phase 2 implementation, provider selection, or physical routing.

## Approval gate

Architecture Path, Phase 1 Red, Phase 2 Green, and Phase 3 Refactor are
complete. The Green
slice implements the named system shape, `RegisterSet` acting-space identity,
qualified-site ambiguity checks, static composite Hilbert shape, and
provider-neutral logical/flat QPU identity. Provider selection and physical
routing remain out of scope. Human review of the completed feature unit
remains required.

## Phase 1 Red record

- Acceptance specification: `docs/specs/qpex-multi-register-acting-space.md`.
- Test file: `tests/test_multi_register_acting_space_red.py`.
- Verification: all five targeted tests fail against the current compiler,
  because the reviewed multi-register surface and diagnostics are not yet
  implemented. The failures are the expected Red state.
- At Red entry: production implementation was intentionally absent.

## Phase 2 Green record

- Parser accepts the declarative `system` register shape and records named
  static widths.
- Type checking preserves `RegisterSet<SystemName>`, rejects unqualified
  sites in multi-register expressions, rejects unknown register names, and
  rejects implicit single-register lifts.
- QPU IR records total logical width, Hilbert dimension, declaration-order
  tensor provenance, register offsets, and register-local/derived flat
  logical qubit identities.
- Verification: the five LISS-0067 acceptance tests pass. Full regression
  testing still reports eight pre-existing failures outside this slice.

## Phase 3 Refactor record

- QPU IR now uses one helper to resolve the accepted system declaration,
  avoiding duplicated shape-selection logic.
- Type-checking restores the active composite acting-space context in a
  `finally` block, preventing context leakage if a nested check fails.
- No new language behavior or provider behavior was introduced.
