# LISS-0097: OpenQASM 3 backend completion

## Metadata

- Local issue ID: LISS-0097
- GitHub issue: not created
- Initial/current planning size: XL / XL
- Owner/agent: unassigned
- Adjudicator decision points: backend/subset/parser; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: portable backend / P0 / XL
- Depends on: LISS-0082, LISS-0083, LISS-0087
- Related: existing QASM backend; LISS-0077 for dynamic slices
- Branch: `feature/liss-0097-openqasm3`
- Implementation permission: **none**
- LISS-0082 handoff: consume a verified provider-neutral Semantic/Algorithm
  Plan projection. OpenQASM version, subset, timing, dynamic support, and
  emission policy remain backend-owned and must not enter Semantic IR.

## Acceptance scenarios

1. Static CH0 plans emit a declared OpenQASM version/subset with parameters,
   measurement/result metadata and source-linked diagnostics.
2. Empty or unsupported plans fail; no empty-program or simulator fallback is
   emitted.
3. An independent parser accepts every success artifact, while capability
   validation remains distinct from syntax validation.
4. Dynamic, timing and subroutine features are emitted only after their
   semantic and target capabilities are approved.

## Slices

| Slice | Scope | Gate |
|---|---|---|
| A | static CH0 subset manifest and failure contract | P0 first |
| B | parameters and deterministic declarations | after A |
| C | measurement/results and source annotations | after B |
| D | subroutine/inlining policy | separate architecture review |
| E | dynamic regions/reset | after LISS-0077 |
| F | timing/barriers and target validation evidence | after LISS-0099 |

## Boundaries and execution

- Candidate writes: `compiler/staqex/backend/qasm/` and narrowly approved QASM
  tests; `codegen/openqasm.py` is read-only until migration scope is explicit.
- Forbidden: language semantics in emitter, provider SDK, silent degradation,
  unreviewed dynamic control, claiming syntax as executability.
- Use one Slice/phase via the
  [bounded packet](../architecture/bounded-feature-execution-packet.md).

## Decisions, verification, planning

Approve authoritative backend path, supported subset and independent parser
before Red. Verify deterministic text, parse round-trip, negative capability
fixtures and unchanged Semantic IR.

- AIP-0097-001: proposed; XL; strong reasoning for backend consolidation,
  code assistant for bounded emitter slices; estimate N/A until packet.
