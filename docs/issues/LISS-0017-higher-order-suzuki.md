# LISS-0017: Higher-order Suzuki decomposition and error control

## Metadata

- Local issue ID: LISS-0017
- GitHub issue: none
- Status: **Phase 3 reviewed**
- Phase: Feature Path Phase 3 Refactor complete
- Type: feature + numerical architecture
- Priority: P2
- Initial planning size: L
- Current planning size: TBD
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

## Summary

Extend the first-order Pauli Trotter QASM lowering in ADR 0063 with optional
higher-order Suzuki formulas and an explicit error/tolerance contract.

## Acceptance Notes

- [x] Supported Suzuki orders and coefficient conventions are specified.
- [x] Error estimate or bound inputs/outputs are specified.
- [x] Step-count selection and user override semantics are specified.
- [x] Unsupported Hamiltonian diagnostics remain explicit.
- [x] Numerical and QASM regression cases are accepted before implementation.

## Dependencies

- Parent: none
- Depends on: ADR 0050, ADR 0063
- Blocks: higher-accuracy QASM evolution
- Related: LISS-0008, ADR 0041

## Adjudicator Decision Points

- [x] Which order is the first supported follow-on?
- [x] Is an a priori bound required, or an empirical estimate sufficient?
- [x] Which tolerance and cost tradeoff is user-visible?

## Context

- Included: Pauli Hamiltonians, QASM gates, fixed-N first-order baseline.
- Omitted: Fock/grid lowering, pulse control, vendor transpilation.
- Assumptions: first-order behavior remains the compatibility baseline.

## AI Planning Records

### AIP-0017-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: L
- Intended execution route: Architecture Path, then Feature Path AT-TDD.
- Intended scope: numerical contract and QASM lowering only.
- Estimation basis: formula correctness, error reporting, and regression tests.
- Assumptions: no vendor SDK.
- Confidence: medium

## Verification

- Mathematical reference cases plus `tests/test_qasm3_codegen.py` extensions after approval.

## Design Note

- Target behavior: add an explicit higher-order Suzuki codegen policy without
  changing exact Kernel evolution or silently claiming an error guarantee.
- Phase to execute next: Architecture review; Phase 1 Red is blocked on the
  numerical contract decisions below.
- Context included: ADR 0063, current first-order Trotter lowering, sparse
  Pauli support, QASM tests, and numeric policy ADR 0076.
- Context omitted: Fock/grid lowering, pulse control, vendor transpilers, and
  adaptive runtime evolution.
- VO/DTO candidates: immutable `SuzukiPolicy`, `ErrorContract`, and
  `TrotterPlan` carrying order, step count, tolerance, and provenance.
- Ports/adapters: none; this is a deterministic QASM lowering policy.
- Suggested task routing: strong reasoning plus mathematical reference cases;
  deterministic QASM regression tests after acceptance.
- Ambiguities requiring Adjudicator decision: first supported order, a priori
  versus empirical error contract, and user-visible tolerance/cost policy.

## Proposed architecture direction

1. Keep first-order Lie-Trotter as the compatibility default.
2. Prefer second-order symmetric Suzuki `S2` as the first follow-on because it
   has a simple palindromic composition and does not require a new operator
   family. Higher orders remain separate extensions.
3. Make approximation policy explicit in the QASM lowering request; never infer
   a higher order from a tolerance alone.
4. Treat an a priori bound and an empirical estimate as distinct contracts. A
   backend must not label an empirical estimate as a mathematical guarantee.
5. Require an explicit step-count or an accepted policy for deriving it, and
   preserve order, steps, tolerance, and estimate provenance in lowering
   metadata.

## Architecture decision record

Proposed [ADR 0084](../architecture/decision-themes/dec-0006-host-qpu-and-external-ports.md).

Adjudicator decision (2026-07-24): S2/order 2 only; `using Suzuki(...)` syntax;
exclusive `steps` versus `tolerance`; and explicit `Bound`/
`EmpiricalEstimate` modes. ADR 0084 is Accepted and Phase 1 Red is authorized.

## Phase 1 Red record

- Added [`test_higher_order_suzuki_red.py`](../../tests/test_higher_order_suzuki_red.py).
- The Red contract covers `using Suzuki(order = 2, steps = N)`, static
  tolerance plus explicit error mode, order rejection, and exclusive
  `steps`/`tolerance` validation.
- The suite is intentionally Red because evolve parsing, AST policy storage,
  and diagnostics do not yet implement the accepted syntax. No production code
  was changed.

## Phase 2 Green record

- Added `SuzukiPolicy` to the AST and parsed `using Suzuki(...)` after
  Hamiltonian evolve duration.
- Added static validation for order 2, exclusive `steps`/`tolerance`, required
  error mode, positive values, and `Bound`/`EmpiricalEstimate` names.
- Added scientific-notation numeric literal support required by the accepted
  `tolerance = 1e-4` example.
- Added the ADR 0084 S2 palindromic QASM lowering: forward half steps, a full
  central term, and reverse half steps for each fixed slice.
- Added static step derivation using `alpha = sum(abs(coefficients))` with the
  accepted Bound and EmpiricalEstimate formulas. Direct `steps` is not clamped
  or silently rewritten.
- Added provider-neutral QPU IR `lowering_policy` provenance with algorithm,
  order, resolved steps, error mode, and tolerance target.
- The existing first-order lowering remains the compatibility default.

The Phase 1 Red contract is Green and the Phase 3 refactor is reviewed. S4,
adaptive selection, and provider-specific resource planning remain deferred by
ADR 0084.

### Phase 3 review record

- Shared AST-policy step resolution between QASM lowering and QPU IR
  provenance; behavior and assertions are unchanged.
- Reviewer empathy: the mathematical policy is isolated in named helpers, and
  the lowering path remains readable without hiding resource or error-mode
  decisions in the emitter.
- Verification: Green checks, Spec Verification 165/165, `compileall`, and
  `git diff --check` passed.
