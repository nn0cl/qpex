# LISS-0089: Exact circuit synthesis and optimization

## Metadata

- Local issue ID: LISS-0089
- GitHub issue: not created
- Initial/current planning size: XL / XL
- Owner/agent: unassigned
- Adjudicator decision points: Architecture + Red for the exact-pass boundary,
  then integrated Green, Refactor, and final PR/merge
- Status/phase: **final-review-ready** / `implementation and tests complete;
  PR pending`
- Type/priority/size: verified optimization / P1 / XL
- Depends on: LISS-0082 and LISS-0087
- Design/implementation branch: `codex/liss-0089-design`

## Acceptance scenarios

1. cancellation and rotation merging occur only with exact side conditions.
2. commutation, controlled/adjoint specialization and ancilla reuse retain a
   checkable witness and provenance.
3. differential exact simulation confirms accepted transformations on bounded
   fixtures; a mismatch blocks output.
4. source term order changes only under declared legal policy.

## Integrated execution scope

The following are internal review dimensions of one LISS-level execution unit,
not separate slices, branches, Red/Green/Refactor cycles, or approval gates:

| Dimension | Acceptance focus |
|---|---|
| Exact pass contract | immutable operation graph, candidate, witness, result, and diagnostics |
| Algebraic transforms | inverse cancellation, exact rotation merge, legal commutation |
| Structural transforms | controlled/adjoint specialization and ancilla reuse with discharge evidence |
| Equivalence | bounded exact differential before/after evidence |
| Safety boundary | no approximation, provider routing, unproved reorder, or source mutation |
| Scale | compact symbolic repetition and deterministic profile fixtures |

Candidate writes: [Exact Optimization specification](../specs/staqex-v1-exact-circuit-optimization.md), a future
`compiler/staqex/exact_optimization.py`, and one integrated
`tests/test_exact_optimization_integrated_red.py` suite. Approximate rewrites,
target routing, and unproved heuristic reorderings are forbidden. Use the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0089-001: proposed; XL; strong architecture/proof-policy review for the
  integrated contract, followed by code-assistant execution of one reviewed
  Red/Green/Refactor cycle.

## Approval sequence

1. Architecture + Phase 1 Red: approve the exact-pass boundary, proof laws,
   diagnostics, and integrated failing suite.
2. Phase 2 Green: implement only the reviewed exact transformations.
3. Phase 3 Refactor: preserve behavior and synchronize documentation.
4. Final review / PR / merge: one completion packet and one CI-gated merge.

No implementation or tests are authorized by this design update alone.
