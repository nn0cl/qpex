# LISS-0088: Hamiltonian and algorithm planner

## Metadata

- Local issue ID: LISS-0088
- GitHub issue: not created
- Initial/current planning size: XL / XL
- Owner/agent: unassigned
- Adjudicator decision points: approved methods/policies; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: algorithm planning / P1 / XL
- Depends on: LISS-0083 and LISS-0087
- Branch: `feature/liss-0088-algorithm-planner`; implementation: **none**

## Acceptance scenarios

1. planner policy evaluates supported candidates and records alternatives,
   costs, rejection reasons and provenance.
2. Suzuki and QDrift bounded methods close their error/resource obligations.
3. state preparation is explicit and does not assume a zero state or oracle.
4. Krylov, QFT, qubitization and LCU remain declared unsupported until their
   mathematical and target prerequisites are reviewed.

## Slices and boundaries

| Slice | Scope |
|---|---|
| A | planner port, candidate and decision evidence |
| B | Suzuki family |
| C | QDrift and hardware-efficient preparation |
| D | bounded Krylov/QFT variants |
| E | fault-tolerant qubitization/LCU contract, P2 gated |

Candidate writes: new planner modules and `tests/test_algorithm_planner_*.py`.
Runtime-adaptive hidden selection, target SDKs and unsupported “best”
heuristics are forbidden. Profiles: `SIM0_EXACT`, `CH1_DIGITAL_RESEARCH`, NH5.
Use the [bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0088-001: proposed; XL; strong method review, code assistant per accepted
  method Slice.
