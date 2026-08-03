# LISS-0077 integrated plan intake (P0 controller/feed-forward)

## Design check

- Scope: reorganize LISS-0077 so P0 delivery is one Dynamic controller /
  feed-forward implementation unit (former A–D as internal dimensions);
  defer E and optional AST parser wire; minimize Adjudicator approvals to
  four for the P0 package.
- Inspected: LISS-0077 Issue, WP-0025 Current next, WP-0029 P0-B, ADR 0071,
  ADR 0106 dynamic refine, LISS-0082 Dynamic marker handoff, LISS-0028
  boundary, LISS-0094/0097 integrated-package pattern, bounded packet,
  Definition of Done, and branch/PR discipline.
- Included: lane/escape diagnostics, finite match + one-merge, reset/reuse
  capability obligations, FakeDynamicExecutor under supplied outcomes.
- Excluded: portable dynamic artifact (E), OpenQASM dynamic emission,
  provider SDKs, mixed-state exec (0096), Static Kernel changes, live submit.
- Decision: A–D are internal dimensions only. Four approvals for P0.
  Preferred write path: `compiler/staqex/dynamic_qpu.py`.
- Verification: Issue, spec, WP, dependency, branch, and status terminology
  synchronized before Phase 1 Red; no implementation or tests authorized by
  this intake.

## Rationale

Controller escape rules, token/merge correlation, capability obligations, and
deterministic Fake execution share one safety boundary: Dynamic feedback must
not weaken Static terminal measurement or silently emulate unsupported target
features. Separate A–D Slice gates would repeat the same isolation review.

## Also synchronized in this intake

- LISS-0097 P0 completion wording: PR #167 merge tip `83b34e7`.

## Next approval

None for the LISS-0077 P0 package after merge. Current next advances to
LISS-0120 design intake (representative program language review gate).

## Artifacts produced by this intake

- [LISS-0077](../../architecture/documentation-compression-map.md)
  rewritten around the P0 integrated package
- [staqex-v1-dynamic-qpu-plan.md](../../specs/staqex-v1-dynamic-qpu-plan.md)
- WP-0025 / local-issue-planning / open-work-register synchronization
- Branch: `feature/liss-0077-dynamic-qpu`

## Phase evidence

- Red/Green/Refactor executed under continuing-remaining-Issues authorization
  2026-07-31; integrated Red `10/10` after Refactor.
