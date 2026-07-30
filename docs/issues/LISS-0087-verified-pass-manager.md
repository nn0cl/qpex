# LISS-0087: Verified pass manager

## Metadata

- Local issue ID: LISS-0087
- GitHub issue: not created
- Initial/current planning size: L / L
- Owner/agent: unassigned
- Adjudicator decision points: integrated pass/result contract and four LISS-level
  approvals (Architecture + Red, Green, Refactor, final PR/merge)
- Status/phase: **complete** / `final review approved; merge candidate`
- Type/priority/size: compiler infrastructure / P0 / L
- Depends on: LISS-0080–0083; blocks LISS-0088–0093 and LISS-0097
- Branch: `codex/liss-0087-integrated-plan`
- Implementation permission: **none**
- LISS-0082 handoff: use the integrated Semantic module and its deterministic
  verifier diagnostics as the immutable pass pre/post boundary. Pass ordering,
  optimization policy, and hard-stop orchestration belong here.

## Document topology

This Issue is the single acceptance and approval record for LISS-0087. The
implementation contract is maintained in the [verified pass manager
specification](../specs/staqex-v1-verified-pass-manager.md); WP-0025 carries
roadmap dependencies; dated traces carry design and execution evidence. The
internal dimensions below do not create separate Issue files, branches, PRs,
or approval gates.

## Acceptance scenarios

1. A pass consumes an immutable verified input and returns output plus
   provenance; it cannot mutate or bypass verification.
2. Precondition, postcondition, exactness class, configuration identity and
   diagnostics are deterministic.
3. Invalid output never reaches a later pass or backend.
4. CH0 and NH5 compact plans use the same pass evidence contract.

## Integrated execution scope

| Slice | Scope |
|---|---|
| A / Foundation | pass/result/configuration DTOs and identity |
| B / Safety | pre/post verifier orchestration and hard stop |
| C / Obligations | exact/approximate classification and obligation propagation |
| D / Composition | deterministic pipeline composition and provenance report |
| E / Evidence | compact CH0/NH5 integration fixtures |

These are internal review dimensions only. One integrated Red suite, Green
implementation, and Refactor cover A–E.

## Approval sequence

1. Architecture + Phase 1 Red: vocabulary, DTOs, verifier laws, diagnostics,
   and integrated A–E tests.
2. Phase 2 Green: minimum immutable pass manager implementation.
3. Phase 3 Refactor: behavior-preserving cleanup and documentation sync.
4. Final review / PR / merge: one completion packet and one CI-gated merge.

## Boundaries and execution

- Candidate writes: new `verified_pass.py`; `tests/test_verified_pass_*.py`.
- Read-only: individual optimization/lowering modules.
- Forbidden: pass-specific business policy, mutable global registries,
  swallowing diagnostics, backend fallback.
- Use one approved LISS-level phase through the
  [bounded packet](../architecture/bounded-feature-execution-packet.md).

## Decisions, verification, planning

Approve pass failure/result vocabulary and finite evidence boundaries before
Red. Verify deterministic order, no downstream call after failure, obligation
preservation, CH0/NH5 parity, and existing compiler regressions.

- AIP-0087-001: proposed; L; code assistant after contract review; strong
  reasoning only for cross-IR conflicts; estimate N/A until packet.
