# LISS-0083: Algorithm Plan IR and approximation ledger

## Metadata

- Local issue ID: LISS-0083
- GitHub issue: not created
- Initial/current planning size: XL / XL
- Owner/agent: unassigned
- Adjudicator decision points: stage ordering and ledger contract; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: planning IR / P0 / XL
- Parent: WP-0025 E2; depends on LISS-0082 and LISS-0033
- Blocks: LISS-0085–0094 and portable backends
- Branch: `feature/liss-0083-algorithm-plan-ir`
- Implementation permission: **none**
- LISS-0082 handoff: consume the verified Semantic module's operation-scoped
  exactness, approximation obligations, Physics/source provenance, and
  symbolic structure. Mapping, discretization, tolerance, error ledger, and
  realization policy begin here and must not leak backward into Semantic IR.

## Summary

Represent explicit realization choices—mapping, discretization, evolution,
state preparation, measurement, error and resources—without changing semantic
meaning or prematurely flattening hierarchy.

## Acceptance scenarios

1. Every approximate plan node identifies semantic origin, policy, assumptions,
   bound or estimate, resource effect, and unresolved obligations.
2. Exact and approximate transforms are distinct; missing provenance or error
   disposition is a verifier failure.
3. callable regions, symbolic repetition and exact large resource expressions
   survive until bounded target materialization.
4. `SIM0_EXACT`, `CH0_COMMON_PHYSICAL`, NH5, QP-2 and QS-2 consume one schema;
   profile limits do not enter Quantum Semantic IR.

## Slices

| Slice | Scope |
|---|---|
| A | immutable plan identities, provenance, hierarchy and verifier |
| B | approximation/error ledger and obligation closure |
| C | mapping/discretization and state-preparation decision records |
| D | evolution/measurement plan records and alternatives |
| E | exact/symbolic resources and bounded materialization contract |
| F | Semantic IR lowering and Bell/GHZ + finite-spin witnesses |

## Boundaries and execution

- Candidate writes: new `algorithm_plan_ir.py`; approved
  `tests/test_algorithm_plan_ir_*.py`.
- Read-only: Semantic/Physics IR and existing QPU IR unless a later Slice
  explicitly authorizes a narrow adapter.
- Forbidden: provider types, SDKs, hidden defaults, gate emission, numerical
  solvers, eager expanded-operation allocation.
- Each Red must name DTO fields, verifier codes, fixture profile and expected
  failure under the [bounded packet](../architecture/bounded-feature-execution-packet.md).

## Decisions and verification

Architecture review must resolve the finite-evidence stage-ordering ambiguity
before Slice C. Verify canonical serialization, deterministic diagnostics,
exact large integers/symbols and compact-plan complexity.

## AI planning record

- AIP-0083-001: proposed; XL; strong reasoning for ledger architecture, code
  assistant for one reviewed Slice; estimate N/A until execution packet.
