# LISS-0090: Measurement grouping and shot allocation

## Metadata

- Local issue ID: LISS-0090
- GitHub issue: not created
- Initial/current planning size: L / L
- Owner/agent: unassigned
- Adjudicator decision points: integrated statistical contract; Architecture +
  Red, Green, Refactor, and final PR/merge
- Status/phase: **review** / `phase-1-red` — integrated Red complete; Green
  approval pending
- Type/priority/size: measurement planning / P1 / L
- Depends on: LISS-0083 and LISS-0087; blocks LISS-0093 and LISS-0103
- Branch: `codex/liss-0090-integrated-plan`; implementation: **none**

## Acceptance scenarios

1. every declared observable maps to reconstructable raw measurement groups.
2. grouping records commutation evidence and never groups incompatible terms.
3. shot allocation records confidence target, covariance assumptions, bounds,
   rounding and total budget.
4. raw and derived provenance survives result reconstruction.

## Integrated scope and boundaries

The former A–D slices are retained as internal review dimensions of one
implementation unit. They are not separate approval points, branches, or
phase cycles. The implementation must land one coherent measurement-plan
contract so that grouping, reconstruction, uncertainty, and allocation cannot
drift independently.

| Review dimension | Scope |
|---|---|
| Observable mapping | immutable observable/group/result-map DTOs and canonical identities |
| Compatibility | commutation witness, deterministic grouping, incompatible-term rejection |
| Statistical target | confidence, bounds, covariance assumptions, rounding, and budget policy |
| Allocation evidence | basic/covariance-aware allocation, budget conservation, raw/derived provenance |

Candidate writes: new measurement planning module,
`tests/test_measurement_plan_integrated_red.py`, and synchronized design
artifacts. Physical sampling, mitigation, provider jobs, and result-report
publication are forbidden. Use `SIM0_EXACT` and `CH1_DIGITAL_RESEARCH` fixtures
through the [bounded packet](../architecture/bounded-feature-execution-packet.md).

## Approval unit

One integrated Architecture/design + Red review covers the full acceptance
surface. After that, one Green, one Refactor, and one final PR/merge sequence
covers the Issue. A new estimator, provider, mitigation, or result-ownership
boundary reopens Architecture review.

## Planning

- AIP-0090-001: proposed; L; strong statistical-contract review for the
  integrated packet, then code assistant for deterministic Red/Green/Refactor.
  Internal dimensions are not separate estimates or approval gates.

## Phase 1 Red evidence

- `tests/test_measurement_plan_integrated_red.py`: 11 tests, 0 passed, 11
  failed as expected because `compiler.staqex.measurement_plan` does not yet
  exist.
- `py_compile` and `git diff --check`: passed.
- `compiler/` and reviewed acceptance assertions were not changed.
- Required next approval: review the integrated Red assertions and authorize
  Phase 2 Green; no implementation has started.
