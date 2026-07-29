# LISS-0078: Function, interface, pipeline, and effect consolidation

## Metadata

- Local issue ID: LISS-0078
- GitHub issue: not created
- Initial/current planning size: L / L
- Owner/agent: unassigned
- Adjudicator decision points: canonical coherence contract; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: type-system consolidation / P1 / L
- Depends on: LISS-0068 and LISS-0076; branch:
  `feature/liss-0078-function-effect-model`; implementation: **none**

## Acceptance scenarios

1. Function values, calls, partial application, pipelines, interface dispatch
   and explicit `return` use one resolved signature/effect model.
2. Wrappers, methods and module links cannot erase Execution or QPU effects.
3. Visibility and phase diagnostics retain source provenance after dispatch.
4. Existing pure Host/Theory functions retain behavior.

## Slices and boundaries

| Slice | Scope |
|---|---|
| A | canonical function/effect signature VO |
| B | calls, partial application and pipeline propagation |
| C | interface/method dispatch and visibility |
| D | return/coherence/module-link diagnostics |

Candidate writes are `hir.py`, `typecheck.py` and approved
`tests/test_function_effect_*.py`; parser/runtime changes require a separate
Slice. No new syntax, implicit effect, provider behavior or adapter logic.

Apply the [bounded packet](../architecture/bounded-feature-execution-packet.md).
Red must name one construct matrix and exact diagnostic; run type, phase,
module-link and existing pipeline suites.

## Planning

- AIP-0078-001: proposed; L; strong review for coherence, code assistant per
  approved Slice; estimate N/A until execution packet.
