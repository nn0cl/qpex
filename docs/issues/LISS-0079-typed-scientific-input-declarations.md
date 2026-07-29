# LISS-0079: Typed scientific input declarations

## Metadata

- Local issue ID: LISS-0079
- GitHub issue: not created
- Initial/current planning size: L / L
- Owner/agent: unassigned
- Adjudicator decision points: source surface; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: language + input contract / P1 / L
- Depends on: LISS-0076 and LISS-0045; blocks LISS-0101
- Branch: `feature/liss-0079-scientific-input-declarations`; implementation:
  **none**

## Acceptance scenarios

1. Source declarations describe Host-bound scalar, array, table and instrument
   inputs with type, shape/schema, unit and provenance requirements.
2. Shape, unit, schema or phase mismatch fails before execution.
3. Declarations contain no path, network, credential or parser API.
4. Core tests bind immutable fake values; adapters remain optional.

## Slices and boundaries

| Slice | Scope |
|---|---|
| A | scalar/array declaration syntax and HIR |
| B | table/schema and unit contracts |
| C | instrument/provenance requirement declarations |
| D | binding diagnostics and module-link behavior |

Candidate writes: parser/AST/HIR/typecheck and
`tests/test_scientific_input_declaration_*.py` as separately approved.
`scientific_input.py` adapters are read-only; files/network/secrets are
forbidden. Use the [bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0079-001: proposed; L; strong syntax/boundary review then code assistant
  per Slice; estimate N/A until packet.
