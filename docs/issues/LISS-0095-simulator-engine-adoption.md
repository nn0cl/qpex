# LISS-0095: Simulator engine adoption

## Metadata

- Local issue ID: LISS-0095
- GitHub issue: not created
- Initial/current planning size: L / L
- Owner/agent: unassigned
- Adjudicator decision points: POC scope, technology selection, adapter phases
- Status/phase: **proposed — technology decision required** /
  `phase-0-design`
- Type/priority/size: dependency adoption / P1 / L
- Depends on: LISS-0094; blocks engine-backed LISS-0096
- Branch: `docs/liss-0095-simulator-selection`; implementation: **none**

## Acceptance scenarios

1. candidates are compared against the accepted simulator port using the same
   correctness fixtures, precision and rejection cases.
2. license, supported platforms, release/version policy, vulnerability
   posture, diagnostics and performance envelope are recorded.
3. a minimal real-file POC proves adapter feasibility without leaking engine
   types into core.
4. exact state-vector is selected first; stabilizer, tensor and mixed engines
   may remain separate later decisions.

## Decision slices

| Slice | Scope |
|---|---|
| A | evaluation matrix and benchmark/reference corpus |
| B | version-matched candidate research |
| C | isolated POCs through LISS-0094 port |
| D | technology ADR and Adjudicator selection |
| E | selected adapter implementation under new phase approval |

No model may select or install an engine from this Issue alone. Candidate POCs
write only isolated adapter/fixture paths approved for Slice C; lockfiles and
dependencies are forbidden before technology approval. Apply the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0095-001: proposed; L; strong reasoning and deterministic benchmarks for
  selection; code assistant only after the chosen technology is approved.
