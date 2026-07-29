# LISS-0091: Resource estimation and feasibility

## Metadata

- Local issue ID: LISS-0091
- GitHub issue: not created
- Initial/current planning size: L / L
- Owner/agent: unassigned
- Adjudicator decision points: quantity/budget contract; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: resource analysis / P1 / L
- Depends on: LISS-0083 and LISS-0087; blocks LISS-0092
- Branch: `feature/liss-0091-resource-estimation`; implementation: **none**

## Acceptance scenarios

1. semantic, logical and physical resources are separate typed categories.
2. pre-routing and post-routing estimates remain distinct and identify
   assumptions, uncertainty and profile snapshot.
3. quantities beyond unsigned 64-bit range remain exact or symbolic.
4. failure, decoder, link, factory, memory, time, power and cost budgets state
   compositional assumptions and may remain unknown.

## Slices and boundaries

| Slice | Scope |
|---|---|
| A | typed quantities, unknowns and estimate provenance |
| B | logical/simulator resources and pre-routing estimate |
| C | physical/post-routing estimate and uncertainty |
| D | FTQC/network/factory compositional budgets |
| E | CH1/NH5/QP-2/QS-2 feasibility reports |

Candidate writes: new resource estimate module and
`tests/test_resource_estimate_*.py`. Provider prices, calibration fetches and
semantic reinterpretation are forbidden. Use the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0091-001: proposed; L; strong quantity/budget review, code assistant per
  accepted estimator Slice.
