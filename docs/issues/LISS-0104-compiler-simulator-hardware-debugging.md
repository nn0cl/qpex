# LISS-0104: Compiler, simulator, and hardware debugging

## Metadata

- Local issue ID: LISS-0104
- GitHub issue: not created
- Initial/current planning size: L / L
- Owner/agent: unassigned
- Adjudicator decision points: checkpoint/diagnostic capabilities; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: diagnostics tooling / P1 / L
- Depends on: LISS-0087, LISS-0094 and LISS-0103
- Branch: `feature/liss-0104-debug-evidence`; implementation: **none**

## Acceptance scenarios

1. IR/pass inspection is source-linked, deterministic and does not mutate the
   inspected artifact.
2. simulator checkpoints are non-collapsing capabilities and never become an
   unrequested measurement in a QPU artifact.
3. resource-cost reports identify stage, assumptions and profile snapshot.
4. hardware diagnostic jobs are explicit Host requests with separate results,
   consent and budget.

## Slices and boundaries

| Slice | Scope |
|---|---|
| A | inspection/query VOs and source links |
| B | pass trace and resource-cost report |
| C | simulator checkpoint port/capability |
| D | hardware diagnostic-job contract |
| E | CLI/presentation adapters |

Candidate writes: diagnostic use cases/ports and
`tests/test_debug_evidence_*.py`; semantic mutation, hidden measurement,
provider SDKs and direct UI-to-provider calls are forbidden. Use the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0104-001: proposed; L; strong capability review, code assistant per
  bounded diagnostic Slice.
