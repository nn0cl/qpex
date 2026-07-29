# LISS-0096: Dynamic and mixed-state simulator execution

## Metadata

- Local issue ID: LISS-0096
- GitHub issue: not created
- Initial/current planning size: XL / XL
- Owner/agent: unassigned
- Adjudicator decision points: conformance tolerances; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: simulator adapter / P1 / XL
- Depends on: LISS-0077, LISS-0084, LISS-0094 and accepted LISS-0095 engine
- Branch: `feature/liss-0096-dynamic-mixed-simulation`; implementation:
  **none**

## Acceptance scenarios

1. dynamic measurement/feed-forward is reproducible under supplied outcomes
   or seed and respects controller correlation/lifetime.
2. density/channel, trajectory and Lindblad executions preserve the accepted
   mixed-state contracts.
3. equivalent small cases agree across exact pure, density and trajectory
   paths within declared tolerance/statistical acceptance.
4. unsupported combinations reject without pure-state, static or engine
   fallback.

## Slices and boundaries

| Slice | Scope |
|---|---|
| A | dynamic adapter execution and supplied outcomes |
| B | density/channel execution |
| C | trajectory execution and seeded sampling |
| D | Lindblad plans and conformance corpus |
| E | `SIM1_MIXED` budgets and combined rejection matrix |

Writes are limited to selected simulator adapters and
`tests/test_dynamic_mixed_simulator_*.py`; core semantics and engine-independent
ports are read-only. Use the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0096-001: proposed; XL; strong conformance review, code assistant per
  selected-engine adapter Slice.
