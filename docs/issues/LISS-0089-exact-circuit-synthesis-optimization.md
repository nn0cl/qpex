# LISS-0089: Exact circuit synthesis and optimization

## Metadata

- Local issue ID: LISS-0089
- GitHub issue: not created
- Initial/current planning size: XL / XL
- Owner/agent: unassigned
- Adjudicator decision points: proof policy; each transform/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: verified optimization / P1 / XL
- Depends on: LISS-0082 and LISS-0087
- Branch: `feature/liss-0089-exact-optimization`; implementation: **none**

## Acceptance scenarios

1. cancellation and rotation merging occur only with exact side conditions.
2. commutation, controlled/adjoint specialization and ancilla reuse retain a
   checkable witness and provenance.
3. differential exact simulation confirms accepted transformations on bounded
   fixtures; a mismatch blocks output.
4. source term order changes only under declared legal policy.

## Slices and boundaries

| Slice | Scope |
|---|---|
| A | optimization result/proof-witness contract |
| B | cancellation and rotation merge |
| C | commutation and controlled/adjoint specialization |
| D | ancilla reuse/discharge |
| E | bounded synthesis and differential suite |

Candidate writes: new exact optimization passes and
`tests/test_exact_optimization_*.py`; approximate rewrites, target routing and
unproved heuristic reorderings are forbidden. Use the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0089-001: proposed; XL; strong proof-policy review then code assistant
  per transform.
