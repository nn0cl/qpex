# LISS-0088 Hamiltonian and algorithm planner design intake

## [DESIGN CHECK]

- **Scope and expected behavior:** consolidate LISS-0088 into one integrated
  planner contract and one AT-TDD cycle. The planner records deterministic
  candidate decisions, alternatives, policy evidence, approximation/resource
  obligations, explicit preparation evidence, and honest unsupported results.
  P1 implementation covers bounded Suzuki, QDrift, and explicit
  hardware-efficient preparation; advanced Krylov/QFT and fault-tolerant
  qubitization/LCU remain declared boundaries.
- **Specifications and files inspected:**
  `docs/issues/LISS-0088-hamiltonian-algorithm-planner.md`,
  `docs/specs/staqex-v1-algorithm-plan-ir.md`,
  `compiler/staqex/algorithm_plan_ir.py`,
  `tests/test_algorithm_plan_ir_integrated_red.py`, WP-0025, WP-0029,
  `docs/architecture/current-hardware-delivery-envelope.md`, bounded packet,
  AT-TDD process, testing strategy, implementation readiness, and
  collaboration scheme.
- **Component boundaries, ports/adapters, and VO/DTO candidates:** the
  planner remains provider-neutral domain/application code and depends only on
  verified Algorithm Plan IR values. Candidate DTOs are
  `PlannerRequest`, `AlgorithmCandidate`, `CandidateEvaluation`,
  `PlannerDecision`, `PreparationContract`, and `PlannerProfile`. No provider,
  network, simulator, numerical solver, credential, or QPU adapter is used.
- **Applicable constraints:** Never Leave the State; no silent repair; exact
  and approximate obligations stay explicit; profile limits are fixtures and
  never language semantics; no eager expansion; no hidden runtime adaptation;
  LISS-0083 owns plan IR; LISS-0087 owns pass orchestration; LISS-0089 onward
  own optimization, measurement, routing, and target projection.
- **Decisions, assumptions, and unresolved ambiguities:** Suzuki and QDrift
  are the first P1 method families. “Hardware-efficient preparation” means a
  declared preparation contract, not a provider gate set. Exact error formulas,
  tolerance units, candidate parameter vocabulary, and the final diagnostic
  codes/detail keys remain Phase 1 Red review decisions. QFT/Krylov scope is
  bounded to explicit unsupported or reviewed finite witnesses; qubitization/
  LCU remain P2-gated. No new dependency is selected.
- **Included and omitted AI context:** included the Algorithm Plan IR contract
  and implementation, current delivery profiles, relevant planning documents,
  and test conventions. Omitted unrelated compiler modules, provider SDKs,
  credentials, network data, and numerical-library internals.
- **Task routing:** strong reasoning review for mathematical/policy boundaries;
  code assistant for deterministic DTO/test conversion after Red approval;
  shell/compiler/test tools for verification. AI output is advisory and must
  be represented by reviewed repository artifacts before implementation.
- **Input/output evidence contract:** inputs are repository-local specs and
  deterministic literals. Outputs are immutable DTO proposals, diagnostics,
  explicit alternatives/rejection evidence, and traceable provenance. No AI
  generated value is trusted as runtime input; no hidden reasoning is recorded.
- **Verification plan:** documentation links and cross-references, Markdown
  consistency, `git diff --check`, and later Phase 1 direct test execution.
  This design phase changes no compiler or test implementation.

## Design decisions recorded

1. One integrated LISS-0088 execution unit replaces method-specific approval
   gates. Internal dimensions remain visible in the specification.
2. LISS-0083 `AlgorithmPlanModule` and its verifier remain the stable plan
   boundary; LISS-0088 adds policy evaluation rather than a second plan IR.
3. Current execution evidence uses `SIM0_EXACT` and `CH1_DIGITAL_RESEARCH`;
   NH5 fixtures stress compact symbolic plans without claiming hardware
   availability.
4. Unsupported methods produce explicit, provenance-preserving decisions; they
   are not silently selected or implemented by fallback.

## Stop condition

Design intake is complete. The next safe action is Architecture + Phase 1 Red
approval. Until that approval, no planner source or test file may be changed.

## Phase 1 Red evidence

- Approval: integrated Architecture + Phase 1 Red received 2026-07-30.
- Changed: `tests/test_algorithm_planner_integrated_red.py` and Issue status
  only; `compiler/staqex/algorithm_planner.py` does not exist and was not
  created.
- Coverage: twelve deterministic tests for exact Suzuki, bounded Suzuki and
  QDrift, explicit preparation, provenance, obligation closure, decision
  evidence, policy rejection, deferred methods, compact profiles, and stable
  diagnostics/serialization.
- Expected Red: import failure because the reviewed planner API is absent.
- Verification: test source compilation and direct execution were run;
  `git diff --check` is clean.
- Stop condition: Phase 2 Green is not authorized by this Red approval and
  remains gated pending review of the test assertions.

## Phase 2 Green evidence

- Approval: Phase 2 Green received 2026-07-30.
- Changed: `compiler/staqex/algorithm_planner.py`; the reviewed Red suite was
  not changed.
- Implemented: immutable planner request/candidate/evaluation/decision/profile
  and preparation records, deterministic evidence validation, explicit
  unsupported handling, and a serializable provider-neutral result.
- Excluded: gate emission, simulator execution, numerical solving, provider or
  target selection, runtime adaptation, and backend adapters.
- Verification: the integrated Red suite is expected to pass; compile and
  `git diff --check` results follow in this trace.
- Stop condition: Phase 3 Refactor remains gated pending Green review.

## Phase 3 Refactor evidence

- Approval: Phase 3 Refactor received 2026-07-30.
- Changed: implementation-only cleanup in
  `compiler/staqex/algorithm_planner.py`; the Red suite and its assertions
  were not changed.
- Refactor: extracted provenance, approximation, decision-evidence,
  preparation, and policy predicates; simplified result construction without
  changing diagnostic codes, ordering, or accepted/rejected behavior.
- Verification: the integrated planner suite and LISS-0083/LISS-0087
  regression suites remain green; compile and `git diff --check` are clean.
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
