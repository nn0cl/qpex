# LISS-0094: Simulator port and capability profiles

## Metadata

- Local issue ID: LISS-0094
- GitHub issue: not created
- Initial/current planning size: L / L
- Owner/agent: unassigned
- Adjudicator decision points: port placement/result vocabulary; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: port contract / P0 / L
- Depends on: LISS-0082, LISS-0083; blocks LISS-0095, LISS-0096, LISS-0104
- Branch: `feature/liss-0094-simulator-port`
- Implementation permission: **none**

## Acceptance scenarios

1. Core use cases submit verified plans through a simulator port using fake
   adapters; no engine type enters Domain or planning IR.
2. Capability negotiation rejects unsupported carrier, operation, memory,
   observation or dynamic requirements before allocation.
3. RNG/seed, tolerance, budgets and observation plan are explicit and results
   identify simulation rather than physical execution.
4. `SIM0_EXACT` supports the bounded oracle and rejects over-budget plans
   deterministically.

## Slices

| Slice | Scope |
|---|---|
| A | capability, request, result and rejection VOs |
| B | port plus fake adapter and deterministic seed contract |
| C | observation plan and exact-oracle result contract |
| D | budget estimator and pre-allocation rejection |
| E | `SIM0_EXACT`/`SIM1_MIXED` fixtures |

## Boundaries and execution

- Candidate writes: new `ports/simulator.py`, fake test adapter, approved
  `tests/test_simulator_port_*.py`; placement confirmed during Red intake.
- Forbidden: choosing an engine, importing simulator packages into core,
  implicit fallback, unbounded allocation, physical-result labels.
- Use the [bounded packet](../architecture/bounded-feature-execution-packet.md).

## Decisions, verification, planning

Approve port placement and result vocabulary before Red. Test only fakes until
LISS-0095; verify deterministic rejection, seed propagation and no provider or
engine imports.

- AIP-0094-001: proposed; L; code assistant for closed port slices; estimate
  N/A until packet.
