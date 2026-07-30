# LISS-0092: Layout, routing, native translation, and scheduling

## Metadata

- Local issue ID: LISS-0092
- GitHub issue: not created
- Initial/current planning size: XL / XL
- Owner/agent: unassigned
- Adjudicator decision points: integrated target-stage contract;
  Architecture + Red, Green, Refactor, and final PR/merge
- Status/phase: **complete** / `phase-3-refactor` — PR #163 merged into
  `main` as `afdbfa9`
- Type/priority/size: target planning / P1 / XL
- Depends on: LISS-0089 **complete**, LISS-0091 **complete**; LISS-0099
  **deferred for live ports** — this Issue uses synthetic versioned target
  snapshots as fixtures (same pattern as LISS-0091 profiles)
- Blocks: LISS-0093 (partial), post-routing fill-in for LISS-0091 consumers
- Branch: `feature/liss-0092-target-routing`; implementation:
  `compiler/staqex/target_routing.py`; tests:
  `tests/test_target_routing_integrated_red.py`
- Plan: [`docs/specs/staqex-v1-target-routing-plan.md`](../specs/staqex-v1-target-routing-plan.md)
- Intake trace:
  [`docs/collaboration/traces/2026-07-31-liss-0092-integrated-plan-intake.md`](../collaboration/traces/2026-07-31-liss-0092-integrated-plan-intake.md)

## Acceptance scenarios

1. logical-to-physical mapping, inserted operations, native translation and
   schedule are separate, ordered stages with provenance.
2. connectivity, timing, measurement/reset and concurrency constraints come
   only from a versioned target snapshot.
3. logical resource identity survives routing and post-routing validation.
4. infeasible plans fail explicitly; target constraints never flow back into
   Theory, Physics IR or Semantic IR.

## Integrated scope and boundaries

The former A–E slices are retained as **internal review dimensions** of one
implementation unit. They are not separate approval points, branches, or
phase cycles.

| Review dimension | Scope |
|---|---|
| A — Stages | target pipeline stage/result DTOs and ordered provenance |
| B — Layout | layout and topology validation against snapshot connectivity |
| C — Routing | deterministic routing / SWAP insertion records |
| D — Native | native translation and post-route verifier |
| E — Schedule | timing/barrier scheduling and CH1/NH5 synthetic fixtures |

Candidate writes (after Red approval):
`compiler/staqex/target_routing.py`,
`tests/test_target_routing_integrated_red.py`, and synchronized design
artifacts.

### LISS-0099 boundary

LISS-0099 owns the eventual physical target **port** and live/capability
adapter surface. LISS-0092 may define and consume a **synthetic immutable
`TargetSnapshot`** DTO for deterministic tests. That DTO must remain
provider-neutral and must not embed SDK types. When LISS-0099 lands, adapters
project into this (or a reviewed successor) snapshot schema — they do not
push target fields into Theory / Physics / Semantic IR.

### Forbidden

- provider SDKs, credentials, network, calibration fetches
- semantic / Physics / Theory rewrites from target constraints
- implicit cloud or simulator fallback on infeasibility
- non-deterministic routing (seeded/explicit policies only)
- language-embedded topology or qubit maxima

Use the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Approval unit

Four approvals only:

1. Plan intake (this document + plan spec) — **complete**
2. Integrated Architecture + Phase 1 Red
3. Phase 2 Green
4. Phase 3 Refactor + final PR/merge

A new live capability port, provider topology schema, or Theory leakage
reopens Architecture review.

## Planning

- AIP-0092-001: proposed; XL; strong target-stage review for the
  **integrated** packet, then code assistant for deterministic
  Red/Green/Refactor. Internal dimensions are not separate estimates or
  approval gates.

## Phase 1 Red evidence

- Approval: integrated Architecture + Phase 1 Red, received 2026-07-31.
- Changed: `tests/test_target_routing_integrated_red.py` and status docs
  only; no `compiler/staqex/target_routing.py`.
- Coverage: eleven deterministic tests spanning ordered stages, snapshot
  validation, logical identity survival, topology/capacity infeasibility,
  deterministic SWAP insertion, native rejection, schedule/barriers,
  CH1/NH5 fixtures, Theory/Physics/Semantic isolation, and post-route
  identity verification.
- Expected result: Red by missing `compiler.staqex.target_routing`;
  `python3 tests/test_target_routing_integrated_red.py` →
  `0 passed, 11 failed` (ModuleNotFoundError).
- Verification: `py_compile` of the Red suite succeeds; implementation
  module absent.
- Stop condition: Phase 2 Green is not authorized by the Red approval.

## Phase 2 Green evidence

- Approval: integrated Phase 2 Green, received 2026-07-31.
- Changed: `compiler/staqex/target_routing.py`; Red assertions unchanged.
- Implemented: TargetSnapshot, ordered layout/routing/native/schedule
  pipeline, deterministic SWAP insertion, capacity/topology/native rejects,
  schedule barriers, and post-route identity verification. No Physics/Semantic
  IR imports.
- Integrated Red: 11 passed / 0 failed.
- Related regressions: resource estimate 12, measurement plan 11, verified
  pass 10, Algorithm Plan IR 10 — all passed.
- Excluded: LISS-0099 live ports, provider SDK, Theory mutation.
- Required next approval: Phase 3 Refactor + final PR/merge.

## Phase 3 Refactor evidence

- Approval: Phase 3 Refactor + final PR/merge, received 2026-07-31.
- Split routing, native translation, schedule builders, and stage verification
  helpers; clarified deterministic SWAP application without changing DTOs or
  diagnostics.
- Integrated Red: 11 passed / 0 failed after Refactor.
- Related regressions remain green: resource estimate 12, measurement plan 11.
- Final review focus: confirm Theory/Physics/Semantic isolation and that
  infeasibility never sets `selected_alternative`.
- Completion evidence: PR #163
  (`feat: add LISS-0092 integrated target routing`) merged into `main`
  as `afdbfa9`.
