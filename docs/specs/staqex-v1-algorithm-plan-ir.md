# Staqex v1 Algorithm Plan IR and approximation ledger

## Purpose and authority

This document is the implementation-facing contract for LISS-0083. The
LISS-0083 Issue is authoritative for scope, acceptance scenarios, status, and
approval state. WP-0025 is authoritative for roadmap ordering and cross-Issue
dependencies. This specification is authoritative for provider-neutral plan
DTOs, verifier laws, diagnostics, and the projection boundary.

LISS-0083 is one implementation unit. Foundation, ledger, realization,
operations, scale, and handoff are internal review dimensions, not separate
Issues, branches, Red/Green/Refactor cycles, or approval gates.

## Boundary

The plan IR sits after Quantum Semantic IR and before pass orchestration,
algorithm-specific planning, and target backends:

```text
Semantic IR -> Algorithm Plan IR -> pass manager / algorithm planners
                              -> simulator or QPU planning projections
```

The plan may preserve semantic references, source and Physics provenance,
exactness obligations, symbolic repetition, and resource expressions. It must
not mutate Semantic IR, emit gates, select a provider, call a numerical solver,
or hide runtime-adaptive policy choices.

Candidate implementation files are limited to:

- `compiler/staqex/algorithm_plan_ir.py`
- `tests/test_algorithm_plan_ir_*.py`
- synchronized Issue, work-plan, specification, and trace documents

LISS-0087 owns pass orchestration. LISS-0088 owns concrete Hamiltonian
algorithm policy and method-specific planners. LISS-0094 and later Issues own
target capability and backend projections. Their contracts may consume this
boundary but are not implemented here.

## Integrated contract

The following records are immutable value objects or immutable module
collections. Names are provisional until the integrated Red review; changing
them requires updating this specification and the Red evidence together.

| Record family | Required meaning | Required evidence |
|---|---|---|
| Plan identity and provenance | Every plan/node preserves semantic operation identity, whole-Joint-state lineage, source/Physics evidence, and hierarchy | canonical identity and provenance diagnostics |
| Exactness obligation | Exact, approximate, and unresolved obligations are distinct | disposition, bound/estimate, and closure verification |
| Realization decision | Mapping, discretization, encoding boundary, state preparation, evolution, and measurement are explicit | alternatives, assumptions, rejection reasons, and policy provenance |
| Resource expression | Dimensions, ancillas, depth, operations, measurements, latency, memory, and target materialization remain exact or symbolic | no eager expansion; deterministic serialization |
| Consumer projection | A verified plan can be viewed by simulator/QPU planning test doubles without provider types or semantic mutation | consumer-neutral projection fixture |
| Witness fixture | Current hardware and compact NH5/QP-2/QS-2 cases exercise the same laws | finite witness plus compact stress cases |

### Required verifier laws

The integrated verifier must reject:

1. missing or conflicting identity and provenance;
2. an approximate step without a bound or estimate and explicit disposition;
3. an unresolved obligation presented as closed;
4. a realization choice whose alternatives, assumptions, rejection reasons, or
   policy provenance are absent;
5. hidden runtime-adaptive selection or target/provider data in semantic
   meaning;
6. lossy conversion of exact or symbolic resource expressions into bounded
   machine values; and
7. eager expansion of symbolic repetition or large resource multiplicity.

It must accept exact plans, explicitly bounded approximate plans, unresolved
plans that remain marked unresolved, symbolic resource expressions, and
consumer-neutral projections.

Diagnostic codes and detail keys are part of the review surface. The Red
phase must name them before implementation; Green may only implement the
reviewed set.

## Integrated test contract

One Red suite covers all six internal dimensions. It must include:

- a minimal exact plan;
- a bounded approximate plan with closed obligation;
- failures for missing provenance, missing disposition, and incomplete
  obligation closure;
- explicit realization alternatives and rejection evidence;
- exact and symbolic resources larger than machine-word ranges without
  expansion;
- canonical serialization and deterministic diagnostic order;
- simulator/QPU planning test doubles that consume projections without SDK
  types or source Semantic mutation; and
- a finite current-hardware witness plus compact NH5/QP-2/QS-2 stress fixtures.

The fixture contract measures structural compactness, not expanded operation
count. Tests use repository-local literals and deterministic doubles only.

## Execution and approval

The LISS follows one ordered cycle:

1. Architecture + Phase 1 Red: review this contract, resolve ambiguities,
   and add only the integrated tests and design traces.
2. Phase 2 Green: implement the minimum provider-neutral DTOs, verifier,
   lowering/projection boundary, and fixtures needed by the reviewed tests.
3. Phase 3 Refactor: preserve behavior, simplify boundaries, synchronize all
   documentation, and run the regression sweep.
4. Final review: commit, push, open PR, verify CI, and merge after approval.

No slice-level approval is required. A material architecture change, provider
selection, source Semantic mutation, or scope expansion into LISS-0087,
LISS-0088, or backend Issues invalidates the batch and requires a new review.

## Document topology

Do not create `LISS-0083-slice-*.md` files. Add durable information to the
proper artifact:

- acceptance or status change -> the LISS-0083 Issue;
- DTO/verifier or boundary change -> this specification;
- dependency or roadmap change -> WP-0025;
- execution evidence or adjudicator decision -> a dated trace.

This topology keeps the design precise without multiplying approval surfaces.
