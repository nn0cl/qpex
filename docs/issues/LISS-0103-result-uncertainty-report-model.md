# LISS-0103: Result, uncertainty, and report model

## Metadata

- Local issue ID: LISS-0103
- GitHub issue: not created
- Initial/current planning size: XL / XL
- Owner/agent: unassigned
- Adjudicator decision points: result/uncertainty schema; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: result domain + presentation / P1 / XL
- Depends on: LISS-0090, LISS-0101 and LISS-0102
- Blocks: LISS-0093 and LISS-0104
- Branch: `feature/liss-0103-result-report`; implementation: **none**

## Acceptance scenarios

1. typed counts, measurements and expectations distinguish raw, derived and
   mitigated values with uncertainty and method.
2. a report identifies source, input, compiler, plan, target snapshot,
   calibration, shots, mapping, attempts and transformations.
3. simulator, emulator and physical evidence are distinct.
4. export adapters cannot change values, hide raw data or invent exactness.

## Slices and boundaries

| Slice | Scope |
|---|---|
| A | typed raw result and execution-kind VOs |
| B | uncertainty/confidence and derived results |
| C | provenance/evidence dossier |
| D | immutable report/application query |
| E | text/JSON export adapters |

Candidate writes: result/domain/use-case modules and
`tests/test_result_report_*.py`; formatting stays in adapters. Hidden
mitigation, theorem/advantage claims and provider objects are forbidden. Use
the [bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0103-001: proposed; XL; strong statistical/provenance review, code
  assistant per DTO/use-case Slice.
