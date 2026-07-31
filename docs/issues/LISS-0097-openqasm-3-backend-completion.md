# LISS-0097: OpenQASM 3 backend completion

## Metadata

- Local issue ID: LISS-0097
- GitHub issue: not created
- Initial/current planning size: XL / L (P0 package) + deferred follow-ups
- Owner/agent: unassigned
- Adjudicator decision points: integrated static CH0 emit contract;
  Architecture + Red, Green, Refactor, and final PR/merge
- Status/phase: **complete** / `phase-3-refactor` — P0 static CH0 package
  complete; final PR/merge on this branch; D/E/F remain deferred
- Type/priority/size: portable backend / P0 / XL (scoped to static CH0 first)
- Depends on: LISS-0082 **complete**, LISS-0083 **complete**, LISS-0087
  **complete**; LISS-0094 **complete**; LISS-0099 **complete** (CH0 fixture)
- Related: existing `backend/qasm/`; LISS-0049 function-call rejection;
  LISS-0077 for deferred dynamic slices
- Branch: `feature/liss-0097-openqasm3`
- Implementation permission: complete pending merge evidence
- Implementation: `compiler/staqex/backend/qasm/ch0_emit.py`; tests:
  `tests/test_openqasm_ch0_integrated_red.py`
- Plan: [`docs/specs/staqex-v1-openqasm-ch0-plan.md`](../specs/staqex-v1-openqasm-ch0-plan.md)
- Intake trace:
  [`docs/collaboration/traces/2026-07-31-liss-0097-integrated-plan-intake.md`](../collaboration/traces/2026-07-31-liss-0097-integrated-plan-intake.md)
- LISS-0082 handoff: consume a verified provider-neutral Semantic/Algorithm
  Plan projection. OpenQASM version, subset, timing, dynamic support, and
  emission policy remain backend-owned and must not enter Semantic IR.

## Acceptance scenarios (P0 package)

1. Static CH0 plans emit a declared OpenQASM version/subset with parameters,
   measurement/result metadata and source-linked diagnostics.
2. Empty or unsupported plans fail; no empty-program or simulator fallback is
   emitted.
3. An independent parse port accepts every success artifact, while capability
   validation remains distinct from syntax validation.
4. Dynamic, timing and subroutine features reject in this package; they are
   deferred, not silently emitted.

## Integrated P0 scope and boundaries

Former slices A–C are **internal review dimensions** of one P0
implementation unit. They are not separate approval points, branches, or
phase cycles.

| Review dimension | Scope |
|---|---|
| A — Manifest | static CH0 subset manifest and failure contract |
| B — Parameters | parameters and deterministic declarations |
| C — Measure | measurement/results and source annotations |

### Deferred (not in this approval unit)

| Slice | Scope | Gate |
|---|---|---|
| D | subroutine/inlining policy | separate Architecture review |
| E | dynamic regions/reset | after LISS-0077 |
| F | timing/barriers and target validation evidence | follow-up after P0 |

Candidate writes (after Red approval):
`compiler/staqex/backend/qasm/ch0_emit.py`,
`tests/test_openqasm_ch0_integrated_red.py`, and synchronized design
artifacts. Existing `codegen/openqasm.py` stays a thin facade unless a
separate migration approval says otherwise.

### Forbidden

- language semantics invented inside the emitter
- provider SDK / live submit
- silent degradation or empty-program success
- unreviewed dynamic/timing/subroutine emission
- claiming parse success as physical executability
- third-party parser Technology selection in this P0 package (Fake parse
  port only)

Use the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Approval unit

Four approvals only for the P0 static CH0 package:

1. Plan intake (this document + plan spec) — **complete** (this step)
2. Integrated Architecture + Phase 1 Red
3. Phase 2 Green
4. Phase 3 Refactor + final PR/merge

D/E/F, a real OpenQASM parser package, or Semantic IR field additions reopen
Architecture review (and Technology selection where applicable).

## Planning

- AIP-0097-001: proposed; L for the P0 package (XL Issue with deferred
  remainder); strong subset/failure-contract review for the **integrated**
  packet, then code assistant for deterministic Red/Green/Refactor.

## Phase 1 Red evidence

- Approval: integrated Architecture + Phase 1 Red, received 2026-07-31.
- Changed: `tests/test_openqasm_ch0_integrated_red.py` and status docs only;
  no `compiler/staqex/backend/qasm/ch0_emit.py`.
- Coverage: ten deterministic tests spanning CH0 manifest, accept emit,
  empty/over-bound/unsupported reject, parameters/measure metadata, Fake
  independent parse, deferred dynamic/timing/subroutine reject, isolation,
  and wrong-profile fail-closed.
- Expected result: Red by missing `compiler.staqex.backend.qasm.ch0_emit`;
  `python3 tests/test_openqasm_ch0_integrated_red.py` →
  `0 passed, 10 failed` (ModuleNotFoundError).
- Verification: `py_compile` of the Red suite succeeds; implementation
  module absent.
- Stop condition: Phase 2 Green is not authorized by the Red approval.

## Phase 2 Green evidence

- Approval: integrated Phase 2 Green, received 2026-07-31.
- Changed: `compiler/staqex/backend/qasm/ch0_emit.py`; Red assertions unchanged.
- Implemented: OpenQasmSubsetManifest, Ch0EmitRequest/Result, EmitDiagnostic,
  FakeIndependentQasmParser, load_ch0_manifest, emit_ch0 with fail-closed
  validation, declared OPENQASM 3.0 / CH0_STATIC_V1 artifact text, and
  `target_executable_claimed=False`.
- Integrated Red: 10 passed / 0 failed.
- Related regressions: simulator port 11, target capability 10 — passed.
- Excluded: D/E/F emission, third-party parser, SDK/live submit.
- Required next approval: none for the P0 package after merge; D/E/F need
  separate Architecture review.

## Phase 3 Refactor evidence

- Approval: Phase 3 Refactor + final PR/merge, received 2026-07-31.
- Split validation helpers (profile/shape, operations, deferred features) and
  render helpers (header/params/ops/measure) without changing DTOs, reject
  codes, or accepted artifact fields.
- Integrated Red: 10 passed / 0 failed after Refactor.
- Related regressions remain green: simulator port 11, target capability 10.
- Final review focus: confirm no empty-program success and that parse success
  never sets `target_executable_claimed`.
- Completion evidence: recorded at merge time on this branch.
