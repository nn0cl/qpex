# LISS-0087 integrated plan intake

## Design check

- Scope: reorganize LISS-0087 from five independently gated slices into one
  verified pass-manager implementation unit with five internal review
  dimensions.
- Inspected: LISS-0087 Issue, WP-0025 E3 row and Current next issue,
  LISS-0083 Algorithm Plan IR specification, Semantic IR handoff, bounded
  execution packet, Definition of Done, and branch/PR discipline.
- Included: immutable pass/result/configuration DTOs, pre/post verification,
  hard-stop orchestration, exactness/obligation propagation, deterministic
  composition, provenance reporting, and CH0/NH5 evidence fixtures.
- Excluded: algorithm selection (0088), circuit synthesis (0089), measurement
  grouping (0090), resource estimation (0091), target/backend adapters, and
  Semantic or Algorithm Plan mutation.
- Decision: A–E are internal dimensions only. The LISS uses four approvals:
  integrated Architecture + Red, Green, Refactor, and final PR/merge.
- Verification: Issue, spec, WP, dependency, branch, and status terminology
  are synchronized before Phase 1 Red; no implementation or tests are
  authorized by this intake.

## Rationale

The five dimensions share one safety boundary: a pass is allowed to produce a
downstream value only after immutable input verification, output verification,
and evidence propagation. Separate slice gates would repeat the same hard-stop
and provenance review while making it easier to introduce incompatible result
vocabularies.

## Next approval

The next requested decision is the integrated Architecture + Phase 1 Red
approval for LISS-0087. Until that approval, source and test files remain
unchanged.

## Phase 1 Red evidence

- Approval: integrated Architecture + Phase 1 Red, received 2026-07-30.
- Changed: `tests/test_verified_pass_integrated_red.py` and Issue status only.
- Coverage: ten deterministic tests spanning immutable pass records,
  pre/post safety, hard-stop behavior, obligation propagation, provenance,
  deterministic composition, CH0/NH5 parity, and policy neutrality.
- Expected result: Red by missing `compiler.staqex.verified_pass`; no
  implementation module was created and no assertion was weakened.
- Verification: test source compiles; direct execution fails at the expected
  missing-API import; `git diff --check` is clean.
- Stop condition: Phase 2 Green is not authorized by the Red approval and
  remains gated pending review of this suite.

## Phase 2 Green evidence

- Approval: integrated Phase 2 Green, received 2026-07-30.
- Changed: `compiler/staqex/verified_pass.py`; Red assertions remain
  unchanged.
- Implemented: immutable pass/configuration/input/output/result DTOs,
  deterministic pre/post verification, hard-stop orchestration, provenance
  checks, obligation/exactness preservation, and policy rejection.
- Excluded: algorithm policy, optimization logic, backend fallback, provider
  SDKs, and target selection.
- Verification: `10 passed, 0 failed`; implementation and test modules compile;
  `git diff --check` is clean.
- Stop condition: Phase 3 Refactor remains gated pending review of Green
  behavior and residual risks.

## Phase 3 Refactor evidence

- Approval: integrated Phase 3 Refactor, received 2026-07-30.
- Changed: implementation-only cleanup in `verified_pass.py`; Red assertions
  were not changed.
- Refactor: extracted final-result construction and simplified failure metadata
  assembly without changing diagnostic codes, ordering, or hard-stop behavior.
- Verification: `10 passed, 0 failed`; implementation and test modules compile;
  Red assertion diff is zero bytes; `git diff --check` is clean.
- Status: implementation and final review are complete; the branch is ready for
  the completion-bearing PR and CI-gated merge.

## Completion packet

- Issue state: `complete` pending the merge of this status-bearing branch.
- Work-plan state: LISS-0087 complete; Current next issue advanced to LISS-0088.
- Completion evidence: integrated tests, compile checks, and `git diff --check`
  are recorded above; the PR description will carry the final review and CI
  evidence before merge.
