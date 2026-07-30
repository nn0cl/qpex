# LISS-0088: Hamiltonian and algorithm planner

## Metadata

- Local issue ID: LISS-0088
- GitHub issue: not created
- Initial/current planning size: XL / XL
- Owner/agent: unassigned
- Adjudicator decision points: integrated Architecture + Red, Green, Refactor,
  and final PR/merge; method policy is reviewed inside the integrated contract
- Status/phase: **complete** / `merged PR #152; CI pending`
- Type/priority/size: algorithm planning / P1 / XL
- Depends on: LISS-0083 and LISS-0087
- Design/implementation branch: `codex/liss-0088-design`

## Acceptance scenarios

1. planner policy evaluates supported candidates and records alternatives,
   costs, rejection reasons and provenance.
2. Suzuki and QDrift bounded methods close their error/resource obligations.
3. state preparation is explicit and does not assume a zero state or oracle.
4. Krylov, QFT, qubitization and LCU remain declared unsupported until their
   mathematical and target prerequisites are reviewed.

## Integrated execution scope

The following are internal review dimensions of one LISS-level execution unit,
not separate slices, branches, Red/Green/Refactor cycles, or approval gates:

| Dimension | Acceptance focus |
|---|---|
| Contract | immutable request/candidate/evaluation/decision/preparation/profile records |
| Policy evidence | alternatives, assumptions, rejection reasons, and policy provenance |
| P1 methods | bounded Suzuki, QDrift, and explicit hardware-efficient preparation |
| Deferred methods | explicit unsupported/deferred Krylov/QFT and qubitization/LCU boundaries |
| Obligation closure | exactness, approximation, resource, preparation, and profile evidence |
| Scale/consumers | compact SIM0/CH1/NH5 witnesses and consumer-neutral projections |

Candidate writes: [Hamiltonian and Algorithm Planner specification](../specs/staqex-v1-hamiltonian-algorithm-planner.md), a future
`compiler/staqex/algorithm_planner.py`, and one integrated
`tests/test_algorithm_planner_integrated_red.py` suite. Runtime-adaptive hidden
selection, target SDKs, numerical solvers, and unsupported “best” heuristics
are forbidden. Profiles: `SIM0_EXACT`, `CH1_DIGITAL_RESEARCH`,
`NH5_NISQ_MODULAR`, and `NH5_FT_MEGA`. Use the [bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0088-001: proposed; XL; strong architecture/method review for the
  integrated contract, followed by code-assistant execution of the reviewed
  Red/Green/Refactor cycle.

## Approval sequence

1. Architecture + Phase 1 Red: approve the integrated planner contract,
   diagnostic vocabulary, P1 method boundary, and failing suite.
2. Phase 2 Green: implement only the reviewed planner behavior.
3. Phase 3 Refactor: preserve behavior and synchronize all documents.
4. Final review / PR / merge: one completion packet and one CI-gated merge.

No implementation or tests are authorized by this design update alone.
