# LISS-0092 integrated plan intake

## Design check

- Scope: reorganize LISS-0092 from five independently gated slices into one
  target-routing implementation unit with five internal review dimensions;
  minimize Adjudicator approvals to four.
- Inspected: LISS-0092 Issue, WP-0025 Current next and E3 row, WP-0029 P1-A,
  LISS-0099 (live port still proposed), LISS-0091 post-routing Unknown
  handoff, LISS-0087/0090/0091 integrated-package pattern, bounded packet,
  Definition of Done, and branch/PR discipline.
- Included: ordered layout/routing/native/schedule stages, synthetic
  versioned TargetSnapshot fixtures, logical identity survival, explicit
  infeasibility, CH1/NH5 fixtures, Theory/Physics/Semantic isolation.
- Excluded: LISS-0099 live capability ports, provider SDKs/credentials,
  calibration fetch, semantic rewrites, implicit fallback, non-deterministic
  routing without reviewed policy.
- Decision: A–E are internal dimensions only. The LISS uses four approvals:
  plan intake, integrated Architecture + Red, Green, Refactor + final
  PR/merge. LISS-0099 dependency is satisfied for Red/Green by synthetic
  snapshots; live ports remain separately gated.
- Verification: Issue, spec, WP, dependency, branch, and status terminology
  are synchronized before Phase 1 Red; no implementation or tests are
  authorized by this intake.

## Rationale

The five dimensions share one safety boundary: target constraints enter only
through a versioned snapshot, stages remain ordered with provenance, and
infeasibility never mutates upstream IR or silently falls back. Separate
Slice gates would repeat the same isolation review and invite incompatible
stage vocabularies.

## Next approval

None for LISS-0092. Merged via PR #163 (`afdbfa9`). Current next is
LISS-0099 design intake.

## Phase 1 Red evidence

- Approval: integrated Architecture + Phase 1 Red, received 2026-07-31.
- Changed: `tests/test_target_routing_integrated_red.py` and Issue/status
  docs only.
- Coverage: eleven deterministic tests spanning ordered stages, snapshot
  validation, identity survival, infeasibility, SWAP determinism, native
  rejection, schedule, CH1/NH5 fixtures, IR isolation, and post-route
  verification.
- Expected result: Red by missing `compiler.staqex.target_routing`;
  `0 passed, 11 failed` with ModuleNotFoundError.
- Stop condition: Phase 2 Green is not authorized by the Red approval.

## Phase 2 Green evidence

- Approval: integrated Phase 2 Green, received 2026-07-31.
- Changed: `compiler/staqex/target_routing.py`; Red suite
  `11 passed, 0 failed`.
- Excluded: LISS-0099 live ports, provider SDK, Theory mutation.
- Stop condition: Refactor not authorized by Green alone.

## Phase 3 Refactor evidence

- Approval: Phase 3 Refactor + final PR/merge, received 2026-07-31.
- Changed: split routing/native/schedule/verify helpers; clarified SWAP
  application; behavior unchanged.
- Integrated Red: 11 passed / 0 failed after Refactor.

## Artifacts produced by this intake

- [LISS-0092](../../issues/LISS-0092-layout-routing-native-scheduling.md)
  rewritten as integrated package
- [staqex-v1-target-routing-plan.md](../../specs/staqex-v1-target-routing-plan.md)
- WP-0025 / local-issue-planning / open-work-register synchronization
- Branch: `feature/liss-0092-target-routing`
