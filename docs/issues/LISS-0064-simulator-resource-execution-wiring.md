# LISS-0064: SimulatorResourceBudget execution wiring

## Metadata

- Local issue ID: LISS-0064
- GitHub issue: none
- Status: Phase 3 Refactor complete; provider submission remains deferred
- Phase: Feature Path — Phase 0 Design Intake → Phase 1 Red → Phase 2 Green → Phase 3 Refactor
- Type: simulator execution safety
- Priority: P1
- Initial planning size: M
- Owner/agent: Codex
- Depends on: LISS-0062, LISS-0063, ADR 0100
- Related work plan: WP-0004

## Summary

Connect the provider-neutral `SimulatorResourceBudget` decision boundary from
LISS-0063 to the actual local simulator and QASM execution entry points. The
resource estimate must be evaluated before state allocation, numerical
evolution, QASM emission, or provider submission crosses its protected
boundary.

This issue does not add provider SDKs, credentials, network submission, CPU
time prediction, benchmark calibration, or new language syntax.

## [DESIGN CHECK]

- Scope and expected behavior: accept a representation-aware execution
  request and `ResourceProfile`, invoke the existing estimator and enforcement
  decision, and stop or continue before the relevant execution boundary.
- Specifications and files inspected: ADR 0100, LISS-0062, LISS-0063,
  `compiler/staqex/resource_profile.py`, `compiler/staqex/resource_enforcement.py`,
  `compiler/staqex/run.py`, and the QASM compiler boundary.
- Component boundaries, ports/adapters, and VO/DTO candidates: the Host
  configuration adapter remains responsible for loading the manifest;
  `ResourceProfile`, `SimulationResourceEstimate`, and
  `SimulatorBudgetDecision` remain immutable provider-neutral DTOs. `run` and
  QASM delivery code may consume the decision but must not reimplement its
  policy. Provider SDKs remain outside the Kernel.
- Applicable constraints: local Simulator `Warn` may continue only with an
  explicit structured warning; local Simulator `Abort` stops before state
  allocation or evolution. QASM and QPU lanes always reject an exceeded
  simulator budget with `SIMULATOR_RESOURCE_ERROR`, regardless of manifest
  policy. No truncation, normalization, state reduction, symbolic fallback,
  or silent continuation is permitted.
- Decisions, assumptions, and unresolved ambiguities: the existing decision
  function is the single policy authority. Phase 1 must determine the
  smallest adapter seam in `run` and QASM emission without changing public
  language syntax. Provider submission remains a separate follow-up. The
  exact execution-request DTO shape is intentionally unresolved until the
  implementation boundary is inspected in Phase 0.
- Included and omitted AI context: included ADR 0100, LISS-0062/0063, the
  resource DTOs, local run path, and QASM boundary; omitted provider SDKs,
  credentials, cloud execution, and unrelated numerical models.
- Task routing: Codex with deterministic repository inspection and local
  tests; no external provider or model is required.
- Input/output evidence contract: Phase 0 produces a reviewed boundary map
  and acceptance scenarios. Future Phase 1 tests must observe whether
  execution continues with `SIMULATOR_RESOURCE_WARNING` or stops with
  `SIMULATOR_RESOURCE_ERROR`, and must prove that no protected downstream
  action occurs after rejection.
- Verification plan: inspect existing execution seams, record the selected
  test locations, and identify any new ADR or ambiguity before requesting
  Phase 1 Red. The Phase 1 test contract uses explicit `resource_profile` and
  `resource_estimate` inputs at the existing `run_source` and QASM generation
  seams; this is a candidate implementation boundary for Green review.

## Accepted baseline from ADR 0100 and LISS-0063

| Lane | Within budget | Over budget |
|---|---|---|
| Local Simulator / `Warn` | Continue | Continue with `SIMULATOR_RESOURCE_WARNING` |
| Local Simulator / `Abort` | Continue | Stop with `SIMULATOR_RESOURCE_ERROR` |
| QASM | Continue | Always stop with `SIMULATOR_RESOURCE_ERROR` |
| QPU / Provider | Continue | Always stop with `SIMULATOR_RESOURCE_ERROR` |

The policy is checked before allocation, evolution, QASM emission, or
submission. A rejected operation produces no partial result and no silently
reduced state.

## Non-goals

- No provider SDK, credentials, retry, session, or network adapter.
- No CPU-time or wall-clock prediction.
- No benchmark recalibration of ADR 0100 factors.
- No changes to binder expansion budgets or static Hilbert limits.
- No new `staqex.toml` fields beyond the accepted LISS-0062 manifest contract.
- No language syntax or source-level resource annotations.

## Approval gate

Phase 1 Red is complete and requests review of the failing tests below.
Phase 2 Green, production implementation, and Phase 3 status promotion require
separate explicit approvals.

## Phase 1 Red record

Added `tests/test_simulator_resource_execution_wiring_red.py` with three
acceptance tests:

- local `Warn` continues and preserves `SIMULATOR_RESOURCE_WARNING`;
- local `Abort` stops before `Evaluator.run_unit`;
- QASM emission rejects before lowering even when the manifest policy is
  `Warn`.

The focused suite fails 3/3 because `run_source` and
`OpenQASM3Generator.generate_detailed` do not yet accept the explicit resource
inputs. This is the intended Red state. No production code, provider adapter,
manifest file, or test assertion was changed to create the failure.

## Phase 2 Green record

- Added optional immutable `ResourceProfile` and
  `SimulationResourceEstimate` inputs to the existing local run and QASM
  generation seams.
- Local simulation checks the budget before `Evaluator.run_unit`; an exceeded
  `Abort` decision returns a failed result without evaluation, while `Warn`
  appends the structured warning and continues.
- QASM checks the budget before `lower_unit_to_circuit`; an exceeded estimate
  returns a rejected circuit with `SIMULATOR_RESOURCE_ERROR`, including when
  the profile policy is `Warn`.
- Supplying only one of the two resource inputs is rejected explicitly; when
  neither is supplied, existing behavior is unchanged.
- Focused verification: 11 tests passed across LISS-0062, LISS-0063, and
  LISS-0064.
- Full verification: 326 passed and 8 pre-existing unrelated failures remain
  unchanged (example/runtime, operator-factory, and oversized-QFT cases).

## Phase 3 Refactor record

- Extracted the shared optional-input validation and lane decision call into
  `enforce_optional_budget`, keeping policy ownership in the resource
  enforcement module.
- Preserved the existing public behavior, diagnostics, rejection timing, and
  no-input compatibility at both execution seams.
- Reviewer empathy: `run` and QASM now expose the same short boundary flow;
  neither delivery path contains a second copy of resource policy.
- Provider submission remains a separate Host adapter follow-up and is not
  implied by this completion.
