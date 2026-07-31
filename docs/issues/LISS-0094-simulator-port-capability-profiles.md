# LISS-0094: Simulator port and capability profiles

## Metadata

- Local issue ID: LISS-0094
- GitHub issue: not created
- Initial/current planning size: L / L
- Owner/agent: unassigned
- Adjudicator decision points: integrated port/result vocabulary;
  Architecture + Red, Green, Refactor, and final PR/merge
- Status/phase: **complete** / `phase-3-refactor` — merged PR #166
  (`b6d2dda`); integrated Red/Green/Refactor shipped
- Type/priority/size: port contract / P0 / L
- Depends on: LISS-0082 **complete**, LISS-0083 **complete**; blocks
  LISS-0095, LISS-0096, LISS-0104
- Branch: `feature/liss-0094-simulator-port`
- Implementation permission: complete pending merge evidence
- Implementation: `compiler/staqex/simulator_port.py`; tests:
  `tests/test_simulator_port_integrated_red.py`
- Plan: [`docs/specs/staqex-v1-simulator-port-plan.md`](../specs/staqex-v1-simulator-port-plan.md)
- Intake trace:
  [`docs/collaboration/traces/2026-07-31-liss-0094-integrated-plan-intake.md`](../collaboration/traces/2026-07-31-liss-0094-integrated-plan-intake.md)
- LISS-0082 handoff: accept only a verified Semantic/Algorithm Plan
  projection; simulator capability limits, RNG, budgets, and observation
  plans must not alter shared semantic meaning or introduce provider/engine
  types upstream.

## Acceptance scenarios

1. Core use cases submit verified plans through a simulator port using fake
   adapters; no engine type enters Domain or planning IR.
2. Capability negotiation rejects unsupported carrier, operation, memory,
   observation or dynamic requirements before allocation.
3. RNG/seed, tolerance, budgets and observation plan are explicit and results
   identify simulation rather than physical execution.
4. `SIM0_EXACT` supports the bounded oracle and rejects over-budget plans
   deterministically; `SIM1_MIXED` loads as a fixture with fail-closed
   unsupported modes.

## Integrated scope and boundaries

The former A–E slices are retained as **internal review dimensions** of one
implementation unit. They are not separate approval points, branches, or
phase cycles.

| Review dimension | Scope |
|---|---|
| A — Vocabulary | capability, request, result and rejection VOs |
| B — Port | SimulatorPort + FakeSimulatorPort + deterministic seed contract |
| C — Observation | observation plan ref and exact-oracle result contract |
| D — Budgets | budget estimator and pre-allocation rejection |
| E — Fixtures | `SIM0_EXACT` / `SIM1_MIXED` capability fixtures |

Candidate writes (after Red approval):
`compiler/staqex/simulator_port.py`,
`tests/test_simulator_port_integrated_red.py`, and synchronized design
artifacts. Placement follows Shipping Kernel peers (`target_capability.py`)
rather than a new top-level `ports/` tree unless Architecture review
overrides.

### Boundary vs later Issues

| Later Issue | Owns |
|---|---|
| LISS-0095 | concrete engine Technology selection behind this port |
| LISS-0096 | dynamic / mixed execution semantics beyond fixture flags |
| LISS-0097 | OpenQASM emission |
| LISS-0099 | physical target capability (already **complete**, PR #165) |

### Forbidden

- choosing or importing a simulator engine package into core
- implicit fallback to another profile or physical backend
- unbounded allocation or silent budget clamp
- labelling simulation results as physical execution
- provider SDKs, credentials, or network in unit tests
- mutating Semantic / Physics / Theory / Algorithm Plan meaning

Use the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Approval unit

Four approvals only:

1. Plan intake (this document + plan spec) — **complete** (this step)
2. Integrated Architecture + Phase 1 Red
3. Phase 2 Green
4. Phase 3 Refactor + final PR/merge

Engine selection, live provider adapters, or Semantic IR field additions
reopen Architecture review (and Technology selection where applicable).

## Planning

- AIP-0094-001: proposed; L; strong port/result review for the **integrated**
  packet, then code assistant for deterministic Red/Green/Refactor. Internal
  dimensions are not separate estimates or approval gates.

## Phase 1 Red evidence

- Approval: integrated Architecture + Phase 1 Red, received 2026-07-31.
- Changed: `tests/test_simulator_port_integrated_red.py` and status docs only;
  no `compiler/staqex/simulator_port.py`.
- Coverage: eleven deterministic tests spanning versioned capability
  dimensions, SIM0/SIM1 fixtures, validate accept/reject, over-budget
  fail-closed execute, unsupported carrier/dynamic/observation, seed and
  simulation labels, observation-plan refs, missing budget fields, IR/engine
  isolation, and unknown-profile fail-closed.
- Expected result: Red by missing `compiler.staqex.simulator_port`;
  `python3 tests/test_simulator_port_integrated_red.py` →
  `0 passed, 11 failed` (ModuleNotFoundError).
- Verification: `py_compile` of the Red suite succeeds; implementation
  module absent.
- Stop condition: Phase 2 Green is not authorized by the Red approval.

## Phase 2 Green evidence

- Approval: integrated Phase 2 Green, received 2026-07-31.
- Changed: `compiler/staqex/simulator_port.py`; Red assertions unchanged.
- Implemented: SimulatorCapabilityProfile, SimulationBudget,
  ObservationPlanRef, SimulationRequest, ValidationReport,
  SimulationResult, SimulatorPort protocol, FakeSimulatorPort with
  SIM0_EXACT/SIM1_MIXED fixtures, validate/execute fail-closed before
  allocation, seed echo, and simulation-labelled canned oracle payload.
- Integrated Red: 11 passed / 0 failed.
- Related regressions: target capability 10, target routing 11, resource
  estimate 12 — passed.
- Excluded: engine packages, live adapters, credentials, network.
- Required next approval: none for this Issue after merge.

## Phase 3 Refactor evidence

- Approval: Phase 3 Refactor + final PR/merge, received 2026-07-31.
- Split fixture-table construction, missing-budget checks, exceeded-dimension
  collection, and rejection messaging without changing DTOs, validate/
  execute decisions, or canned payloads.
- Integrated Red: 11 passed / 0 failed after Refactor.
- Related regressions remain green: target capability 10, target routing 11,
  resource estimate 12.
- Final review focus: confirm simulation labelling and fail-closed budget
  rejection without engine imports.
- Completion evidence: PR #166 merge commit `b6d2dda` on `main`.
