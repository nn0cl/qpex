# LISS-0099 integrated plan intake

## Design check

- Scope: reorganize LISS-0099 from five independently gated slices into one
  target-capability / physical-port implementation unit with five internal
  review dimensions; minimize Adjudicator approvals to four.
- Inspected: LISS-0099 Issue, WP-0025 Current next and E4 row, WP-0029 P0-B,
  LISS-0092 `target_routing.TargetSnapshot`, LISS-0082 Semantic handoff,
  ADR 0110/0111 non-authorizations, LISS-0087/0091/0092 integrated-package
  pattern, bounded packet, Definition of Done, and branch/PR discipline.
- Included: versioned capability schema, freshness/unknown, digital and
  model fields, deployment/resource policies, PhysicalTargetPort + fake
  adapter, CH0/CH1/NH5 fixtures, optional pure projection to routing
  snapshot, no implicit fallback.
- Excluded: live provider SDK (0100), credentials/network in unit tests,
  Semantic/Physics/Theory mutation, routing algorithm changes, job submit.
- Decision: A–E are internal dimensions only. The LISS uses four approvals:
  plan intake, integrated Architecture + Red, Green, Refactor + final
  PR/merge.
- Verification: Issue, spec, WP, dependency, branch, and status terminology
  are synchronized before Phase 1 Red; no implementation or tests are
  authorized by this intake.

## Rationale

Schema, freshness, and port fixtures share one safety boundary: capabilities
enter planning only as versioned immutable profiles, unknowns stay explicit,
and local insufficiency never triggers remote/simulator fallback. Separate
Slice gates would repeat the same isolation review across fixtures and port
shapes.

## Next approval

Final PR/merge for LISS-0099. After merge, Current next advances to
LISS-0094 design intake.

## Phase 1 Red evidence

- Approval: integrated Architecture + Phase 1 Red, received 2026-07-31.
- Changed: `tests/test_target_capability_integrated_red.py` and Issue/status
  docs only.
- Coverage: ten deterministic tests spanning versioned dimensions,
  stale/unknown, fake port fixtures, support/reject, policy completeness,
  LISS-0092 projection, IR isolation, and fail-closed unknown profiles.
- Expected result: Red by missing `compiler.staqex.target_capability`;
  `0 passed, 10 failed` with ModuleNotFoundError.
- Stop condition: Phase 2 Green is not authorized by the Red approval.

## Phase 2 Green evidence

- Approval: integrated Phase 2 Green, received 2026-07-31.
- Changed: `compiler/staqex/target_capability.py`; Red suite
  `10 passed, 0 failed`.
- Excluded: live provider SDK, credentials, network.
- Stop condition: Refactor not authorized by Green alone.

## Phase 3 Refactor evidence

- Approval: Phase 3 Refactor + final PR/merge, received 2026-07-31.
- Changed: split verification helpers and fixture table; behavior unchanged.
- Integrated Red: 10 passed / 0 failed after Refactor.

## Artifacts produced by this intake

- [LISS-0099](../../architecture/documentation-compression-map.md)
  rewritten as integrated package
- [staqex-v1-target-capability-plan.md](../../specs/staqex-v1-target-capability-plan.md)
- WP-0025 / local-issue-planning / open-work-register synchronization
- Branch: `feature/liss-0099-target-capability`
