# LISS-0084: General mixed states, channels, and POVMs

## Metadata

- Local issue ID: LISS-0084
- GitHub issue: not created
- Initial/current planning size: XL / XL
- Owner/agent: unassigned
- Adjudicator decision points: mathematical representation; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: quantum semantics / P1 / XL
- Depends on: LISS-0081, LISS-0082, LISS-0011 and LISS-0037
- Blocks: LISS-0096; branch: `feature/liss-0084-mixed-channels`
- Implementation permission: **none**
- LISS-0082 handoff: extend the existing density carrier and channel/measurement
  signatures without changing the integrated Semantic provenance, whole-Joint
  identity, or Static/Dynamic lane contract. Execution mathematics remains in
  this Issue, not in Slice E.

## Acceptance scenarios

1. Density-state acting spaces and channel signatures preserve whole-Joint
   identity, dimensions and provenance.
2. Kraus/Choi/superoperator forms are explicit representations with named
   conversion obligations, never assumed interchangeable without evidence.
3. Positivity, trace preservation, effect completeness and partial trace never
   silently repair invalid input.
4. Pure/mixed terminal measurement agrees on shared cases under `SIM1_MIXED`.

## Slices and boundaries

| Slice | Scope |
|---|---|
| A | mixed carrier/effect DTOs and verifier |
| B | Kraus channels and composition |
| C | Choi/superoperator evidence boundaries |
| D | POVMs, partial trace and measurement agreement |
| E | small exact fixtures and LISS-0096 handoff |

Candidate writes: new mixed semantic module or approved extension plus
`tests/test_general_mixed_*.py`. Runtime numerics, engines and hidden
purification are forbidden until their own Slices. Use the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0084-001: proposed; XL; strong mathematical/architecture review, code
  assistant only on closed DTO/verifier slices.
