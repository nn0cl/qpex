# LISS-0101: Scientific input bundle and provenance schema

## Metadata

- Local issue ID: LISS-0101
- GitHub issue: not created
- Initial/current planning size: L / L
- Owner/agent: unassigned
- Adjudicator decision points: schema/format; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: application input contract / P1 / L
- Depends on: LISS-0079; blocks LISS-0103
- Branch: `feature/liss-0101-scientific-input-bundle`; implementation: **none**

## Acceptance scenarios

1. immutable versioned scalar/array/table values carry validated type,
   shape/schema, unit, hash, capture time and provenance.
2. the same bundle feeds simulator and QPU use cases.
3. paths, handles, credentials and adapter-specific parser objects are not
   persisted as scientific values.
4. invalid or unsupported versions fail before execution without coercion.

## Slices and boundaries

| Slice | Scope |
|---|---|
| A | scalar/array immutable VOs and canonical hash |
| B | table/schema/unit validation |
| C | provenance/capture/version contract |
| D | SourcePort and fake adapter |
| E | initial text-format adapter after format approval |

Candidate writes: new input bundle/domain/port modules and
`tests/test_scientific_input_bundle_*.py`. File parsing and paths stay in
adapters; network and secrets are forbidden. Use the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0101-001: proposed; L; strong schema review, code assistant per Slice.
