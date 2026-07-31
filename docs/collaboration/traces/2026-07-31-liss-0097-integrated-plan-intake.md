# LISS-0097 integrated plan intake (P0 static CH0)

## Design check

- Scope: reorganize LISS-0097 so P0 delivery is one static CH0 OpenQASM
  implementation unit (former A–C as internal dimensions); defer D/E/F;
  minimize Adjudicator approvals to four for the P0 package.
- Inspected: LISS-0097 Issue, WP-0025 Current next and E4 row, WP-0029 P0-B,
  delivery envelope CH0, compiler blueprint §6.2, existing
  `backend/qasm/` + `codegen/openqasm.py`, LISS-0049 rejection boundary,
  LISS-0094/0099 integrated-package pattern, bounded packet, Definition of
  Done, and branch/PR discipline.
- Included: subset manifest, fail-closed emit, parameters, measure/result
  metadata, Fake independent parse port, CH0 fixtures, no simulator
  fallback.
- Excluded: subroutine/inlining (D), dynamic (E/0077), timing (F), live
  provider, third-party parser Technology selection, Semantic IR mutation,
  QIR.
- Decision: A–C are internal dimensions only. Four approvals for P0.
  Preferred write path: `compiler/staqex/backend/qasm/ch0_emit.py`.
  Declared OpenQASM version string must be explicit in Red/Green without
  inventing unsupported 3.1 features.
- Verification: Issue, spec, WP, dependency, branch, and status terminology
  synchronized before Phase 1 Red; no implementation or tests authorized by
  this intake.

## Rationale

Static CH0 emission, subset declaration, and fail-closed rejection share one
safety boundary: unsupported programs must not become empty or simulator
artifacts, and parse success must not be confused with target executability.
Separate A/B/C Slice gates would repeat the same adapter isolation review.

## Also synchronized in this intake

- LISS-0094 completion wording: PR #166 merge tip `b6d2dda`.

## Next approval

None for the LISS-0097 P0 package after merge. Current next advances to
LISS-0077 design intake (dynamic QPU controller / feed-forward).

## Artifacts produced by this intake

- [LISS-0097](../../issues/LISS-0097-openqasm-3-backend-completion.md)
  rewritten around the P0 integrated package
- [staqex-v1-openqasm-ch0-plan.md](../../specs/staqex-v1-openqasm-ch0-plan.md)
- WP-0025 / local-issue-planning / open-work-register synchronization
- Branch: `feature/liss-0097-openqasm3`

## Phase 1 Red evidence

- Approval: integrated Architecture + Phase 1 Red, received 2026-07-31.
- Changed: `tests/test_openqasm_ch0_integrated_red.py` and Issue/status
  docs only.
- Coverage: ten deterministic tests spanning manifest, emit accept/reject,
  params/measure, Fake parse, deferred features, isolation, and profile
  mismatch.
- Expected result: Red by missing `compiler.staqex.backend.qasm.ch0_emit`;
  `0 passed, 10 failed` with ModuleNotFoundError.
- Stop condition: Phase 2 Green is not authorized by the Red approval.

## Phase 2 Green evidence

- Approval: integrated Phase 2 Green, received 2026-07-31.
- Changed: `compiler/staqex/backend/qasm/ch0_emit.py`; Red suite
  `10 passed, 0 failed`.
- Excluded: D/E/F emission, third-party parser, credentials, network.
- Stop condition: Refactor not authorized by Green alone.

## Phase 3 Refactor evidence

- Approval: Phase 3 Refactor + final PR/merge, received 2026-07-31.
- Changed: split validation and render helpers; behavior unchanged.
- Integrated Red: 10 passed / 0 failed after Refactor.
