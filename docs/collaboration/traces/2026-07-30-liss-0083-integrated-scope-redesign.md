# LISS-0083 integrated scope redesign

## Design check

- Scope: widen LISS-0083 from six independently gated slices to one integrated
  Algorithm Plan IR implementation unit with six internal review dimensions.
- Inspected: LISS-0083 Issue, WP-0025 E3 planning row, LISS-0082 integrated
  handoff, LISS-0087 pass-manager boundary, LISS-0088 planner boundary, and
  the bounded execution packet.
- Included: plan identity/provenance, approximation ledger, realization
  decisions, operation/measurement plans, exact/symbolic resources, bounded
  materialization, Semantic lowering, and consumer-neutral witnesses.
- Excluded: concrete algorithm policy (0088), pass orchestration (0087), mixed
  channel mathematics (0084), simulator/provider/backend implementations, and
  pipeline changes.
- Decision: A–F remain named internal dimensions for traceability but do not
  create approval gates. The LISS receives four approvals: integrated
  Architecture + Red, Green, Refactor, and final PR/merge.
- Verification: issue/plan/WP terminology, dependency, scope, and approval
  consistency; no implementation or tests in this design-only change.

## Rationale

The six existing slices form one DTO/verifier boundary. Splitting their
approvals would repeatedly review the same provenance, exactness, resource,
and consumer-neutrality laws. Keeping them as internal dimensions preserves
review precision while reducing coordination overhead.

## Phase 1 Red evidence

- Approval: integrated Architecture + Phase 1 Red, received 2026-07-30.
- Changed: `tests/test_algorithm_plan_ir_integrated_red.py` only, plus this
  Issue/status synchronization.
- Coverage: ten deterministic tests spanning identity/provenance, exactness
  and approximation obligations, realization evidence, symbolic resources,
  consumer-neutral projection, policy neutrality, witnesses, and diagnostics.
- Expected result: Red by missing `compiler.staqex.algorithm_plan_ir`; no
  implementation module was created and no reviewed assertion was weakened.
- Verification: test source compiles; direct execution fails at the expected
  missing-API import; `git diff --check` is clean.
- Stop condition: Phase 2 Green is not authorized by the Red approval and
  remains gated pending review of this suite.

## Phase 2 Green evidence

- Approval: integrated Phase 2 Green, received 2026-07-30.
- Changed: `compiler/staqex/algorithm_plan_ir.py`; Red assertions remain
  unchanged.
- Implemented: immutable provider-neutral DTOs, deterministic verifier
  diagnostics, and a non-mutating consumer-neutral projection boundary.
- Excluded: algorithm policy, pass orchestration, gate emission, numerical
  solving, provider SDKs, and Semantic IR mutation.
- Verification: `10 passed, 0 failed`; both test and implementation modules
  compile; `git diff --check` is clean.
- Stop condition: Phase 3 Refactor and publication remain gated pending review
  of the Green behavior and residual risks.

## Phase 3 Refactor evidence

- Approval: integrated Phase 3 Refactor, received 2026-07-30.
- Changed: implementation-only cleanup in `algorithm_plan_ir.py`; Red
  assertions were not changed.
- Refactor: extracted shared evidence predicates and a diagnostic type alias;
  verifier responsibilities remain separated into provenance, obligation, and
  realization-policy checks.
- Verification: `10 passed, 0 failed`; both modules compile; Red assertion diff
  is zero bytes; `git diff --check` is clean.
- Status: implementation is complete and awaits final review before commit,
  push, PR, and merge.
