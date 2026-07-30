# LISS-0089 exact circuit synthesis and optimization design intake

## [DESIGN CHECK]

- **Scope and expected behavior:** open a narrow provider-neutral exact
  optimization track under ADR 0022's design baseline. One integrated pass
  contract covers inverse cancellation, exact rotation merging, witnessed
  commutation, controlled/adjoint specialization, ancilla discharge evidence,
  and bounded exact differential equivalence. Approximate rewrites, target
  routing, and runtime heuristics remain excluded.
- **Specifications and files inspected:**
  `docs/issues/LISS-0089-exact-circuit-synthesis-optimization.md`, ADR 0022,
  `docs/architecture/staqex-compiler-optimizations.md`,
  `docs/specs/staqex-v1-quantum-semantic-ir-plan.md`, LISS-0082/LISS-0087
  boundaries, `compiler/staqex/qpu_ir.py`, QPU IR tests, current delivery
  profiles, bounded packet, AT-TDD process, testing strategy, and readiness.
- **Component boundaries, ports/adapters, and VO/DTO candidates:** candidate
  domain DTOs are `OperationNode`, `OperationGraph`,
  `OptimizationCandidate`, `ProofWitness`, and `OptimizationResult`. The pass
  is pure and provider-neutral; no ports or adapters are needed. Differential
  execution uses deterministic exact test doubles, not a runtime simulator or
  provider SDK.
- **Applicable constraints:** Never Leave the State; denotational
  preservation; no silent repair; provenance closed; no eager expansion;
  source order changes only with a proof witness; LISS-0087 owns pass
  orchestration; LISS-0092+ own routing and scheduling.
- **Decisions, assumptions, and unresolved ambiguities:** exact symbolic
  parameter laws, operation vocabulary, witness identity/digest shape,
  diagnostic codes/detail keys, and the exact differential oracle fixture are
  Phase 1 Red review decisions. ADR 0022 remains accepted as a design
  baseline, but its implementation Hold must be explicitly narrowed before
  Red. Numeric tolerance and approximate optimization are not permitted.
- **Included and omitted AI context:** included ADR 0022, optimizer baseline,
  Semantic/Plan/pass boundaries, QPU IR inspection, and profile contracts.
  Omitted provider SDKs, routing/scheduling implementation, numerical backend
  internals, credentials, and unrelated source modules.
- **Task routing:** strong reasoning review for proof and architecture
  boundaries; code assistant for deterministic Red/Green/Refactor after
  approval; deterministic tools for test execution, compilation, and diff
  checks. AI suggestions are advisory until represented in reviewed tests and
  specification text.
- **Input/output evidence contract:** inputs are repository-local contracts and
  immutable literals. Outputs are proof witnesses, provenance, diagnostics,
  explicit rejection reasons, and differential evidence. No AI-generated
  runtime value is trusted; hidden reasoning is not recorded.
- **Verification plan:** cross-reference and scope audit, `git diff --check`,
  and later direct execution of one integrated Red suite. This design phase
  changes no compiler or test implementation.

## Design decisions recorded

1. LISS-0089 uses one integrated execution unit rather than transform-specific
   approval gates.
2. The optimizer returns a graph plus proof witness; it does not mutate source
   Semantic/Plan IR or select a target.
3. Exactness means algebraic/proof-backed equality, not numerical closeness.
4. Current evidence uses `SIM0_EXACT`, with compact `CH1_DIGITAL_RESEARCH` and
   `NH5_NISQ_MODULAR` fixtures; these profiles do not become semantic limits.

## Stop condition

Design intake is complete. The next safe action is Architecture approval for
the exact-pass boundary and Phase 1 Red approval. Until then, no optimizer
source or test file may be changed.

## Phase 1 Red evidence

- Approval: Architecture + Phase 1 Red received 2026-07-30.
- Changed: `tests/test_exact_optimization_integrated_red.py` and Issue status
  only; `compiler/staqex/exact_optimization.py` was not created.
- Coverage: twelve deterministic tests for inverse cancellation, rotation
  merging, witnessed commutation, controlled/adjoint specialization, ancilla
  discharge, provenance, operand/axis safety, source-order preservation,
  approximate/provider policy rejection, differential mismatch, and compact
  deterministic evidence.
- Expected Red: import failure because the reviewed optimizer API is absent.
- Verification: test source compilation and direct execution were run;
  `git diff --check` is clean.
- Stop condition: Phase 2 Green is not authorized by this Red approval and
  remains gated pending review of the test assertions.

## Phase 2 Green evidence

- Approval: Phase 2 Green received 2026-07-30.
- Changed: `compiler/staqex/exact_optimization.py`; the reviewed Red suite
  was not changed.
- Implemented: immutable operation graph, exact candidate/proof/result DTOs,
  witnessed cancellation/rotation/commutation/controlled-adjoint/ancilla
  transformations, provenance and policy diagnostics, and exact differential
  mismatch blocking.
- Excluded: approximate rewrites, numerical tolerance, provider or topology
  selection, routing, scheduling, and runtime mutation.
- Verification: integrated optimizer suite, Algorithm Plan IR, Verified Pass,
  and QPU IR boundary suites passed; compile and `git diff --check` are clean.
- Stop condition: Phase 3 Refactor remains gated pending Green review.

## Phase 3 Refactor evidence

- Approval: Phase 3 Refactor received 2026-07-30.
- Changed: implementation-only cleanup in
  `compiler/staqex/exact_optimization.py`; the Red suite and its assertions
  were not changed.
- Refactor: extracted candidate diagnostic evaluation and witness enrichment,
  preserving diagnostic codes/order, transformed graph behavior, provenance,
  and exact/rejection semantics.
- Verification: integrated optimizer, Algorithm Plan IR, Verified Pass, and
  QPU IR boundary suites remain green; compile and `git diff --check` are
  clean.
- Stop condition: final review and completion status synchronization remain
  pending.

## Final review packet preparation

- Implementation, reviewed tests, and related regressions are green.
- Issue, work-plan row, and this trace are synchronized to
  `final-review-ready`; no PR number or `complete` claim is recorded before
  the PR exists.
- Required next action: open the single completion PR. After its number is
  known, update these same artifacts to `complete`, run the completion packet
  check and CI, then merge.
