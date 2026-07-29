# LISS-0090: Measurement grouping and shot allocation

## Metadata

- Local issue ID: LISS-0090
- GitHub issue: not created
- Initial/current planning size: L / L
- Owner/agent: unassigned
- Adjudicator decision points: statistical contract; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: measurement planning / P1 / L
- Depends on: LISS-0083 and LISS-0087; blocks LISS-0093 and LISS-0103
- Branch: `feature/liss-0090-measurement-planning`; implementation: **none**

## Acceptance scenarios

1. every declared observable maps to reconstructable raw measurement groups.
2. grouping records commutation evidence and never groups incompatible terms.
3. shot allocation records confidence target, covariance assumptions, bounds,
   rounding and total budget.
4. raw and derived provenance survives result reconstruction.

## Slices and boundaries

| Slice | Scope |
|---|---|
| A | observation/group/result-map DTOs |
| B | commuting-group verifier and deterministic grouping |
| C | basic shot allocation and confidence evidence |
| D | covariance-aware allocation and rejection |

Candidate writes: new measurement planning module and
`tests/test_measurement_plan_*.py`. Physical sampling, mitigation and provider
jobs are forbidden. Use `SIM0_EXACT` and `CH1_DIGITAL_RESEARCH` fixtures through
the [bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0090-001: proposed; L; strong statistical contract review, code
  assistant per Slice.
