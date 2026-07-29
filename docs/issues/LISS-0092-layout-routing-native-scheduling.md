# LISS-0092: Layout, routing, native translation, and scheduling

## Metadata

- Local issue ID: LISS-0092
- GitHub issue: not created
- Initial/current planning size: XL / XL
- Owner/agent: unassigned
- Adjudicator decision points: target-stage contract; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: target planning / P1 / XL
- Depends on: LISS-0089, LISS-0091 and LISS-0099
- Branch: `feature/liss-0092-target-routing`; implementation: **none**

## Acceptance scenarios

1. logical-to-physical mapping, inserted operations, native translation and
   schedule are separate, ordered stages with provenance.
2. connectivity, timing, measurement/reset and concurrency constraints come
   only from a versioned target snapshot.
3. logical resource identity survives routing and post-routing validation.
4. infeasible plans fail explicitly; target constraints never flow back into
   Theory, Physics IR or Semantic IR.

## Slices and boundaries

| Slice | Scope |
|---|---|
| A | target pipeline stage/result DTOs |
| B | layout and topology validation |
| C | deterministic routing/SWAP insertion |
| D | native translation and post-route verifier |
| E | timing/barrier scheduling and CH1/NH5 fixtures |

Candidate writes: new target-planning modules and
`tests/test_target_routing_*.py`; provider SDKs, calibration fetches and
semantic rewrites are forbidden. Use the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0092-001: proposed; XL; strong pipeline review, code assistant per
  deterministic stage.
