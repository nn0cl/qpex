# LISS-0091: Resource estimation and feasibility

## Metadata

- Local issue ID: LISS-0091
- GitHub issue: not created
- Initial/current planning size: L / L
- Owner/agent: unassigned
- Adjudicator decision points: integrated quantity/budget contract;
  Architecture + Red, Green, Refactor, and final PR/merge
- Status/phase: **complete** / `phase-3-refactor` — PR #161 merged into
  `main` as `e1e93a9`
- Type/priority/size: resource analysis / P1 / L
- Depends on: LISS-0083 **complete**, LISS-0087 **complete**, LISS-0090
  **complete**; blocks LISS-0092
- Branch: `feature/liss-0091-resource-estimation`; implementation:
  `compiler/staqex/resource_estimate.py`; tests:
  `tests/test_resource_estimate_integrated_red.py`
- Plan: [`docs/specs/staqex-v1-resource-estimation-plan.md`](../specs/staqex-v1-resource-estimation-plan.md)
- Intake trace:
  [`docs/collaboration/traces/2026-07-31-liss-0091-integrated-plan-intake.md`](../collaboration/traces/2026-07-31-liss-0091-integrated-plan-intake.md)

## Acceptance scenarios

1. semantic, logical and physical resources are separate typed categories.
2. pre-routing and post-routing estimates remain distinct and identify
   assumptions, uncertainty and profile snapshot.
3. quantities beyond unsigned 64-bit range remain exact or symbolic.
4. failure, decoder, link, factory, memory, time, power and cost budgets state
   compositional assumptions and may remain unknown.

## Integrated scope and boundaries

The former A–E slices are retained as **internal review dimensions** of one
implementation unit. They are not separate approval points, branches, or
phase cycles. The implementation must land one coherent resource-estimate and
feasibility contract so that quantity types, pre/post-routing stages, FTQC
budgets, and profile reports cannot drift independently.

| Review dimension | Scope |
|---|---|
| A — Quantities | typed quantities, unknowns, and estimate provenance |
| B — Pre-routing | logical/simulator resources and pre-routing estimate |
| C — Post-routing | physical/post-routing estimate and uncertainty (synthetic profiles / Unknown when LISS-0092 is absent) |
| D — Compositional budgets | FTQC / network / factory compositional budgets |
| E — Feasibility reports | CH1 / NH5 / QP-2 / QS-2 feasibility reports against synthetic target profiles |

Candidate writes (after Red approval): new module
`compiler/staqex/resource_estimate.py`,
`tests/test_resource_estimate_integrated_red.py`, optional soft
`CompileResult` attachment in the same Issue, and synchronized design
artifacts.

### Explicit boundary vs ADR 0100

[`SimulationResourceEstimate`](../../compiler/staqex/resource_profile.py) and
[ADR 0100](../architecture/adr/0100-resource-budget-policy.md) remain the
**host-side simulator binder/memory budget** path. LISS-0091 must not
reinterpret, replace, or merge those DTOs into Algorithm Plan resource
categories.

### Forbidden

- provider prices, calibration fetches, and provider SDKs
- semantic reinterpretation or Physics/Semantic carrier invention
- language-embedded qubit or performance maxima
- implicit cloud / simulator fallback
- treating envelope / horizon numbers as delivery forecasts
- layout/routing execution (LISS-0092)

Use the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Approval unit

Four approvals only:

1. Plan intake (this document + plan spec) — **complete**
2. Integrated Architecture + Phase 1 Red
3. Phase 2 Green
4. Phase 3 Refactor + final PR/merge

A new estimator formula family, provider pricing boundary, or merger with ADR
0100 reopens Architecture review.

## Planning

- AIP-0091-001: proposed; L; strong quantity/budget review for the
  **integrated** packet, then code assistant for deterministic
  Red/Green/Refactor. Internal dimensions are not separate estimates or
  approval gates.

## Phase 1 Red evidence

- Approval: integrated Architecture + Phase 1 Red, received 2026-07-31.
- Changed: `tests/test_resource_estimate_integrated_red.py` and status docs
  only; no `compiler/staqex/resource_estimate.py`.
- Coverage: twelve deterministic tests spanning category exclusivity, u64+
  exact/symbolic quantities, pre/post-routing stages, Unknown assumptions,
  compositional budgets, plan-literal pre-routing estimate, CH1/NH5/QP-2/QS-2
  feasibility, reject-without-fallback, ADR 0100 isolation, and soft absent
  input.
- Expected result: Red by missing `compiler.staqex.resource_estimate`;
  `python3 tests/test_resource_estimate_integrated_red.py` →
  `0 passed, 12 failed` (ModuleNotFoundError).
- Verification: `py_compile` of the Red suite succeeds; `git diff --check`
  clean on the test file; implementation module absent.
- Stop condition: Phase 2 Green is not authorized by the Red approval and
  remains gated pending review of this suite.

## Phase 2 Green evidence

- Approval: integrated Phase 2 Green, received 2026-07-31.
- Changed: `compiler/staqex/resource_estimate.py`; Red assertions unchanged
  except one fixture alignment so `physical_qubits` Unknown carries
  `awaiting-liss-0092-routing` (matches the frozen assertion; does not weaken
  acceptance).
- Implemented: typed categories, quantities, Unknown, provenance, pre/post
  routing estimates, compositional budgets, feasibility assessment, soft
  absent-input path, and verification diagnostics. No `resource_profile`
  import.
- Integrated Red: 12 passed / 0 failed.
- Related regressions: measurement plan 11 passed, verified pass 10 passed,
  Algorithm Plan IR 10 passed, LISS-0062 resource profile 4 passed.
- Excluded: provider prices/SDK, layout/routing (0092), host ADR 0100 merger,
  CompileResult pipeline soft wire (module-level soft path only).
- Required next approval: Phase 3 Refactor + final PR/merge.

## Phase 3 Refactor evidence

- Approval: Phase 3 Refactor + final PR/merge, received 2026-07-31.
- Verification responsibility was split into stage, quantity, Unknown, and
  budget helpers; default post-routing and compositional budget builders were
  extracted from `estimate_resources` without changing DTOs, diagnostics, or
  feasibility behavior.
- Integrated Red: 12 passed / 0 failed after Refactor.
- Related regressions remain green: measurement plan 11, verified pass 10,
  Algorithm Plan IR 10, LISS-0062 resource profile 4.
- Final review focus: confirm ADR 0100 isolation (no `resource_profile`
  import) and that reject-without-fallback never selects an alternative.
- Completion evidence: PR #161
  (`feat: add LISS-0091 integrated resource estimation`) merged into `main`
  as `e1e93a9`.
