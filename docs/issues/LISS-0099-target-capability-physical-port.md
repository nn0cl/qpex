# LISS-0099: Target capability profile and physical target port

## Metadata

- Local issue ID: LISS-0099
- GitHub issue: not created
- Initial/current planning size: L / L
- Owner/agent: unassigned
- Adjudicator decision points: integrated schema/port contract;
  Architecture + Red, Green, Refactor, and final PR/merge
- Status/phase: **complete** / `phase-3-refactor` — merged PR #165
  (`ad89d15`); integrated Red/Green/Refactor shipped
- Type/priority/size: port + capability schema / P0 / L
- Depends on: LISS-0082 **complete**, LISS-0067 **complete**; LISS-0092
  **complete** (consumes projected snapshots)
- Blocks: LISS-0100, LISS-0102; supplies live/versioned snapshots that replace
  synthetic-only fixtures from LISS-0092
- Branch: `feature/liss-0099-target-capability`; implementation:
  `compiler/staqex/target_capability.py`; tests:
  `tests/test_target_capability_integrated_red.py`
- Plan: [`docs/specs/staqex-v1-target-capability-plan.md`](../specs/staqex-v1-target-capability-plan.md)
- Intake trace:
  [`docs/collaboration/traces/2026-07-31-liss-0099-integrated-plan-intake.md`](../collaboration/traces/2026-07-31-liss-0099-integrated-plan-intake.md)
- LISS-0082 handoff: target capability data is downstream adapter-owned input
  to planning and rejection. Topology, calibration, deployment, power, QEC,
  and provider fields must remain absent from Semantic IR meaning.

## Acceptance scenarios

1. A versioned snapshot distinguishes native operations, connectivity,
   measurement/reset, timing, dynamic, carrier and computation-model support.
2. logical/physical capacity, calibration age, topology, deployment and
   resource policies are explicit; unknown/stale facts remain unknown/stale.
3. provider data is adapter-owned and no local insufficiency triggers implicit
   remote or simulator fallback.
4. CH0/CH1/NH5 fixtures share one schema and produce deterministic support or
   rejection evidence.

## Integrated scope and boundaries

The former A–E slices are retained as **internal review dimensions** of one
implementation unit. They are not separate approval points, branches, or
phase cycles.

| Review dimension | Scope |
|---|---|
| A — Identity | snapshot identity/version/freshness and unknown values |
| B — Digital | digital operations, topology, timing and dynamic capabilities |
| C — Model | analog/native/computation-model and qudit capabilities |
| D — Policy | deployment, resource, power/memory and consent policies |
| E — Port | physical target port, fake adapter, and CH0/CH1/NH5 fixtures |

Candidate writes (after Red approval):
`compiler/staqex/target_capability.py`,
`tests/test_target_capability_integrated_red.py`, optional pure projection
into `target_routing.TargetSnapshot`, and synchronized design artifacts.

### Boundary vs LISS-0092

LISS-0092 owns the **routing pipeline** and a minimal synthetic
`TargetSnapshot` DTO. LISS-0099 owns the **capability schema + port**. A pure
projection may build a routing snapshot from a capability profile; routing
must not import provider adapters, and capability must not import Semantic IR.

### Forbidden

- provider SDKs in core, credentials, network calls in unit tests
- hidden defaults / implicit remote or simulator fallback
- target fields in Theory / Physics / Semantic IR
- mutating LISS-0092 routing algorithms beyond optional projection helper

Use the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Approval unit

Four approvals only:

1. Plan intake (this document + plan spec) — **complete**
2. Integrated Architecture + Phase 1 Red
3. Phase 2 Green
4. Phase 3 Refactor + final PR/merge

A live provider SDK, credential store, or Semantic IR field addition reopens
Architecture review (and likely Technology selection for LISS-0100).

## Planning

- AIP-0099-001: proposed; L; strong schema/port review for the **integrated**
  packet, then code assistant for deterministic Red/Green/Refactor. Internal
  dimensions are not separate estimates or approval gates.

## Phase 1 Red evidence

- Approval: integrated Architecture + Phase 1 Red, received 2026-07-31.
- Changed: `tests/test_target_capability_integrated_red.py` and status docs
  only; no `compiler/staqex/target_capability.py`.
- Coverage: ten deterministic tests spanning versioned dimensions,
  stale/unknown handling, FakePhysicalTargetPort CH0/CH1/NH5 fixtures,
  support/reject without fallback, policy completeness, LISS-0092 projection
  bridge, IR isolation, and fail-closed unknown profiles.
- Expected result: Red by missing `compiler.staqex.target_capability`;
  `python3 tests/test_target_capability_integrated_red.py` →
  `0 passed, 10 failed` (ModuleNotFoundError).
- Verification: `py_compile` of the Red suite succeeds; implementation
  module absent.
- Stop condition: Phase 2 Green is not authorized by the Red approval.

## Phase 2 Green evidence

- Approval: integrated Phase 2 Green, received 2026-07-31.
- Changed: `compiler/staqex/target_capability.py`; Red assertions unchanged.
- Implemented: TargetCapabilityProfile, Freshness, CapabilityUnknown,
  FakePhysicalTargetPort CH0/CH1/NH5 fixtures, evaluate_support without
  fallback, verify diagnostics, and project_to_routing_snapshot. No
  Physics/Semantic IR imports.
- Integrated Red: 10 passed / 0 failed.
- Related regressions: target routing 11, resource estimate 12 — passed.
- Excluded: live provider SDK, credentials, network.
- Required next approval: Phase 3 Refactor + final PR/merge.

## Phase 3 Refactor evidence

- Approval: Phase 3 Refactor + final PR/merge, received 2026-07-31.
- Split freshness/unknown/policy verification helpers and fixture table
  construction without changing DTOs, diagnostics, or support decisions.
- Integrated Red: 10 passed / 0 failed after Refactor.
- Related regressions remain green: target routing 11, resource estimate 12.
- Final review focus: confirm no provider fallback and that projection into
  LISS-0092 remains a pure mapping.
- Completion evidence: PR #165 merge commit `ad89d15` on `main`.
