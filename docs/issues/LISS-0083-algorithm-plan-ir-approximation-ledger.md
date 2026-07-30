# LISS-0083: Algorithm Plan IR and approximation ledger

## Metadata

- Local issue ID: LISS-0083
- GitHub issue: not created
- Initial/current planning size: XL / XL
- Owner/agent: unassigned
- Adjudicator decision points: one integrated architecture/Red review, one Green
  review, one Refactor review, and one final PR/merge review
- Status/phase: **complete** / `merged PR #146; CI passed 2026-07-30`
- Type/priority/size: planning IR / P0 / XL
- Parent: WP-0025 E2; depends on LISS-0082 and LISS-0033
- Blocks: LISS-0085–0094 and portable backends
- Branch: `feature/liss-0083-integrated-plan`
- Implementation permission: **none**
- LISS-0082 handoff: consume the verified Semantic module's operation-scoped
  exactness, approximation obligations, Physics/source provenance, and
  symbolic structure. Mapping, discretization, tolerance, error ledger, and
  realization policy begin here and must not leak backward into Semantic IR.

## Summary

Represent explicit realization choices—mapping, discretization, evolution,
state preparation, measurement, error and resources—without changing semantic
meaning or prematurely flattening hierarchy.

## Document topology

This Issue is the single acceptance and approval record for LISS-0083. It is
not a requirement that one Issue contain only one document. The implementation
contract is maintained in the [Algorithm Plan IR specification](../specs/staqex-v1-algorithm-plan-ir.md);
WP-0025 carries roadmap dependencies; dated traces carry design and execution
evidence. There are no slice-specific Issue files, branches, or approval gates.

## Acceptance scenarios

1. Every approximate plan node identifies semantic origin, policy, assumptions,
   bound or estimate, resource effect, and unresolved obligations.
2. Exact and approximate transforms are distinct; missing provenance or error
   disposition is a verifier failure.
3. callable regions, symbolic repetition and exact large resource expressions
   survive until bounded target materialization.
4. `SIM0_EXACT`, `CH0_COMMON_PHYSICAL`, NH5, QP-2 and QS-2 consume one schema;
   profile limits do not enter Quantum Semantic IR.
5. A plan preserves Semantic operation identity, whole-Joint-state lineage,
   Physics/source provenance, and the exactness or approximation obligation it
   discharges. A plan cannot invent a semantic operation or silently detach
   from its source evidence.
6. Mapping, discretization, state preparation, evolution, and measurement
   decisions are explicit immutable records with alternatives, assumptions,
   rejection reasons, and policy provenance. Runtime-adaptive hidden choice is
   invalid.
7. Resource effects remain exact or symbolic: logical dimensions, ancillas,
   depth, operations, measurements, classical latency, simulator memory, and
   target materialization estimates may exceed machine-word ranges without
   eager expansion.
8. A verified plan can be projected to simulator and QPU planning test doubles
   without provider SDK types, target fields in semantic meaning, gate emission,
   or mutation of the source Semantic module.
9. A finite current-hardware witness and compact NH5/QP-2/QS-2 stress fixtures
   exercise the same DTO and verifier laws; the large fixtures measure compact
   structure, not expanded operation count.

## Integrated execution scope

LISS-0083 is one implementation unit. The following six dimensions are
internal review areas, not independent approval gates or branches:

| Slice | Scope |
|---|---|
| A / Foundation | immutable plan identities, provenance, hierarchy, canonical serialization, and verifier |
| B / Ledger | approximation/error obligations, exactness transfer, error disposition, and closure |
| C / Realization | mapping, discretization, encoding boundary, and state-preparation decision records |
| D / Operations | evolution, measurement, alternatives, and policy evidence |
| E / Scale | exact/symbolic resources, multiplicity, estimates, and bounded materialization |
| F / Handoff | Semantic lowering, consumer-neutral projections, current witness, and compact stress fixtures |

The implementation is tested and reviewed as one integrated source-to-plan
boundary. A single Red suite covers A–F, a single minimal Green implements all
reviewed assertions, and one behavior-preserving Refactor follows. Internal
dimensions may be reviewed in parallel by the agent, but they do not create
additional Adjudicator approval points.

## Approval sequence

1. **Architecture + Phase 1 Red:** approve the complete contract, including
   finite-evidence stage ordering, DTOs, verifier diagnostics, and integrated
   A–F Red assertions. Only tests and design traces may change initially.
2. **Phase 2 Green:** approve the reviewed integrated Red suite and implement
   the minimum provider-neutral domain DTOs, verifier, lowering boundary, and
   deterministic witness fixtures needed to make it pass.
3. **Phase 3 Refactor:** approve the Green result, regression evidence, and
   behavior-preserving cleanup/document synchronization as one batch.
4. **Final review / PR / merge:** review the complete LISS-0083 scope once.

This reduces six slice-level approval sequences to four LISS-level decisions;
phase discipline remains unchanged.

## Boundaries and execution

- Candidate writes: new `algorithm_plan_ir.py`; approved
  `tests/test_algorithm_plan_ir_*.py`.
- Read-only: Semantic/Physics IR and existing QPU IR unless a later Slice
  explicitly authorizes a narrow adapter.
- Forbidden: provider types, SDKs, hidden defaults, gate emission, numerical
  solvers, eager expanded-operation allocation.
- The integrated Red must name DTO fields, verifier codes, fixture profiles,
  and expected failures under the [bounded packet](../architecture/bounded-feature-execution-packet.md).
- Candidate writes remain limited to `compiler/staqex/algorithm_plan_ir.py`,
  its focused tests, and synchronized design traces/docs. Existing Semantic IR,
  Physics IR, pipeline, and QPU IR are read-only dependencies.
- No provider SDK, gate emission, numerical solver, runtime-adaptive hidden
  selection, or eager expanded-operation allocation is included.
- LISS-0088 owns concrete Hamiltonian algorithm policy and method-specific
  planners; LISS-0087 owns pass orchestration. Their contracts consume this
  Issue's plan boundary and are not pulled into it.

## Decisions and verification

Architecture review must resolve the finite-evidence stage-ordering ambiguity
within the integrated packet before Red. Verify canonical serialization,
deterministic diagnostics, exact large integers/symbols, provenance/obligation
closure, consumer neutrality, and compact-plan complexity across A–F.

## AI planning record

- AIP-0083-001: proposed; XL; strong reasoning for ledger architecture, code
  assistant for one reviewed Slice; estimate N/A until execution packet.
