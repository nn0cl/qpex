# LISS-0085: Continuous equations and numerical lowering

## Metadata

- Local issue ID: LISS-0085
- GitHub issue: not created
- Initial/current planning size: XL / XL
- Owner/agent: unassigned
- Adjudicator decision points: discretization/solver boundaries; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: numerical planning / P1 / XL
- Depends on: LISS-0081, LISS-0083 and LISS-0036
- Branch: `feature/liss-0085-continuous-lowering`; implementation: **none**

## Acceptance scenarios

1. Domain, basis, boundary conditions, differentiation and integration remain
   recognizable from Physics IR into a reviewed numerical plan.
2. No continuous expression becomes finite without an explicit discretization
   decision, assumptions, error obligation and provenance.
3. solver plans report convergence evidence or named failure; they do not
   rewrite source meaning.
4. a small grid fits `SIM0_EXACT`/`CH1_DIGITAL_RESEARCH`; larger profiles reject
   or retain compact symbolic plans.

## Slices and boundaries

| Slice | Scope |
|---|---|
| A | domain/basis/boundary DTOs |
| B | differentiation/integration plan contracts |
| C | discretization decision and error ledger |
| D | solver port and fake solver |
| E | oscillator/grid witness and convergence report |

Candidate writes are new planning/port modules and
`tests/test_continuous_plan_*.py`; solver library selection, dependency
adoption and target mapping require separate approval. Apply the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0085-001: proposed; XL; strong numerical architecture review, bounded
  code-assistant slices afterward.
