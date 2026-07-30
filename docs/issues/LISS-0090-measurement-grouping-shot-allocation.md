# LISS-0090: Measurement grouping and shot allocation

## Metadata

- Local issue ID: LISS-0090
- GitHub issue: not created
- Initial/current planning size: L / L
- Owner/agent: unassigned
- Adjudicator decision points: integrated statistical contract; Architecture +
  Red, Green, Refactor, and final PR/merge
- Status/phase: **complete** / `phase-3-refactor` — PR #155 merged; CI passed;
  post-merge audit passed
- Type/priority/size: measurement planning / P1 / L
- Depends on: LISS-0083 and LISS-0087; blocks LISS-0093 and LISS-0103
- Branch: `codex/liss-0090-integrated-plan`; implementation:
  `compiler/staqex/measurement_plan.py`; tests:
  `tests/test_measurement_plan_integrated_red.py`

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
- Required next approval after Red: authorize Phase 2 Green; this gate has
  been satisfied and is recorded by the Green evidence below.

## Phase 2 Green evidence

- `compiler/staqex/measurement_plan.py` implements the immutable DTOs,
  deterministic grouping verification, statistical-policy validation,
  budget-conserving allocation, and provenance checks required by the reviewed
  Red suite.
- Integrated Red: 11 passed / 0 failed.
- Related measurement and planning regressions: POVM 3 passed, local
  observation execution 4 passed, Algorithm Plan IR 10 passed, Verified Pass
  10 passed.
- `py_compile` and `git diff --check`: passed.
- Reviewed Red assertions were not changed.
- Required next approval after Green: authorize Phase 3 Refactor; this gate has
  been satisfied and is recorded by the Refactor evidence below.

## Phase 3 Refactor evidence

- Verification responsibility was split into identity, group, statistical
  policy, allocation, and provenance helpers without changing the DTOs,
  diagnostics, or allocation behavior.
- Integrated Red: 11 passed / 0 failed after Refactor.
- Related regression suites remain green: POVM 3, local observation 4,
  Algorithm Plan IR 10, and Verified Pass 10.
- Final review focus: confirm that equal-weight allocation is an explicit
  first-contract policy and that later covariance estimators remain outside
  this implementation until separately specified.
- Completion evidence: PR #155 (`feat: add LISS-0090 measurement planning`)
  merged into `main` as `aa3a094`; CI passed and the post-merge completion
  packet audit passed.
