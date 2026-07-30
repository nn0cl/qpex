# LISS-0087: Verified pass manager

## Metadata

- Local issue ID: LISS-0087
- GitHub issue: not created
- Initial/current planning size: L / L
- Owner/agent: unassigned
- Adjudicator decision points: pass result/failure vocabulary; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: compiler infrastructure / P0 / L
- Depends on: LISS-0080–0083; blocks LISS-0088–0093 and LISS-0097
- Branch: `feature/liss-0087-verified-passes`
- Implementation permission: **none**
- LISS-0082 handoff: use the integrated Semantic module and its deterministic
  verifier diagnostics as the immutable pass pre/post boundary. Pass ordering,
  optimization policy, and hard-stop orchestration belong here.

## Acceptance scenarios

1. A pass consumes an immutable verified input and returns output plus
   provenance; it cannot mutate or bypass verification.
2. Precondition, postcondition, exactness class, configuration identity and
   diagnostics are deterministic.
3. Invalid output never reaches a later pass or backend.
4. CH0 and NH5 compact plans use the same pass evidence contract.

## Slices

| Slice | Scope |
|---|---|
| A | pass/result/configuration DTOs and identity |
| B | pre/post verifier orchestration and hard stop |
| C | exact/approximate classification and obligation propagation |
| D | deterministic pipeline composition and provenance report |
| E | compact CH0/NH5 integration fixtures |

## Boundaries and execution

- Candidate writes: new `verified_pass.py`; `tests/test_verified_pass_*.py`.
- Read-only: individual optimization/lowering modules.
- Forbidden: pass-specific business policy, mutable global registries,
  swallowing diagnostics, backend fallback.
- Use one approved Slice/phase through the
  [bounded packet](../architecture/bounded-feature-execution-packet.md).

## Decisions, verification, planning

Approve pass failure/result vocabulary before Red. Verify deterministic order,
no downstream call after failure, obligation preservation and existing
compiler regressions.

- AIP-0087-001: proposed; L; code assistant after contract review; strong
  reasoning only for cross-IR conflicts; estimate N/A until packet.
