# LISS-0017: Higher-order Suzuki decomposition and error control

## Metadata

- Local issue ID: LISS-0017
- GitHub issue: none
- Status: proposed
- Phase: Architecture Path first
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

- [ ] Supported Suzuki orders and coefficient conventions are specified.
- [ ] Error estimate or bound inputs/outputs are specified.
- [ ] Step-count selection and user override semantics are specified.
- [ ] Unsupported Hamiltonian diagnostics remain explicit.
- [ ] Numerical and QASM regression cases are accepted before implementation.

## Dependencies

- Parent: none
- Depends on: ADR 0050, ADR 0063
- Blocks: higher-accuracy QASM evolution
- Related: LISS-0008, ADR 0041

## Adjudicator Decision Points

- [ ] Which order is the first supported follow-on?
- [ ] Is an a priori bound required, or an empirical estimate sufficient?
- [ ] Which tolerance and cost tradeoff is user-visible?

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
