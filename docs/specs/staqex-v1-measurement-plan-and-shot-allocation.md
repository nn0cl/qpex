# Staqex v1 measurement plan and shot allocation

## Status and authority

This is the implementation-facing design contract for LISS-0090. The
LISS-0090 Issue is authoritative for scope, acceptance, and approval state;
WP-0025 is authoritative for roadmap ordering. The internal dimensions below
are review dimensions of one implementation unit, not separate Issues, branches,
Red/Green/Refactor cycles, or approval gates.

## Boundary

The measurement planner consumes declared observables and an explicit
uncertainty target and returns an immutable, provider-neutral plan:

```text
declared observables + policy target -> verified measurement plan
                                      -> raw groups + shot allocation + provenance
```

The plan is a planning artifact. It does not sample, submit a Job, fetch
calibration, choose a provider, perform mitigation, or reinterpret Semantic IR.
Terminal measurement remains explicit and static-Kernel execution remains
measurement-deferred until that boundary.

## Integrated contract

| Review dimension | Required meaning | Evidence |
|---|---|---|
| Observable and result mapping | Every declared observable has a stable identity and reconstructable raw-group mapping | deterministic canonical mapping and missing/duplicate diagnostics |
| Compatibility and grouping | Grouping records the declared commutation/compatibility witness and rejects incompatible terms | incompatible pair rejection and witness provenance |
| Statistical target | Confidence target, estimator family, bounds, covariance assumptions, rounding, and total shot budget are explicit | exact/symbolic allocation record and validation diagnostics |
| Allocation and provenance | Allocation is deterministic, preserves raw versus derived provenance, and does not silently add or merge work | stable ordering, budget conservation, reconstruction fixture |

The planner may use exact symbolic counts when a budget exceeds machine-sized
integers. Unknown covariance or unsupported estimator policy is represented as
unknown or rejected; it is never silently approximated.

## Required verifier laws

The integrated verifier must reject:

1. duplicate or missing observable identities and non-reconstructable result
   mappings;
2. a group without an explicit compatibility witness or with incompatible
   observable terms;
3. confidence targets, bounds, covariance assumptions, or shot budgets that
   are absent, contradictory, negative, or non-finite;
4. allocations that do not conserve the declared total budget or whose
   rounding policy is not deterministic;
5. derived results that cannot point back to raw groups and source observables;
6. provider, calibration, random-sampling, mitigation, or fallback data in
   the domain planning contract; and
7. any plan that changes observable meaning or inserts an implicit measurement.

It must accept a deterministic plan with one observable/group, compatible
multi-term groups, exact budget conservation, and a bounded covariance-aware
allocation whose assumptions remain explicit.

Diagnostic codes and detail keys are part of the review surface. The Red phase
must name the reviewed set before implementation.

## Candidate value objects and ports

Candidate immutable domain records are:

- `ObservableSpec`
- `MeasurementGroup`
- `CompatibilityWitness`
- `ConfidenceTarget`
- `CovarianceAssumption`
- `ShotAllocation`
- `MeasurementPlan`
- `MeasurementPlanDiagnostic`

No runtime port is required for the core planner. A future execution adapter may
consume the plan through an existing Host boundary, but provider, RNG,
calibration, and Job ports are outside LISS-0090.

## Integrated test contract

One Red suite covers all four review dimensions. It must include immutable DTOs,
deterministic canonical ordering, observable-to-raw-group reconstruction,
compatible grouping with an explicit witness, incompatible grouping rejection,
basic and covariance-aware allocation with exact budget conservation, invalid
confidence/bounds/rounding/covariance rejection, raw/derived provenance
continuity, and `SIM0_EXACT` plus `CH1_DIGITAL_RESEARCH` fixtures using the same
contract.

Tests use repository-local literals and deterministic doubles only. No provider
SDK, live execution, calibration fetch, random sampler, or numerical solver is
required.

## Execution and approval

LISS-0090 follows one ordered cycle:

1. Architecture/design intake + integrated Phase 1 Red: review vocabulary,
   statistical assumptions, verifier laws, and the complete test suite; only
   tests, fixtures, and design traces change.
2. Phase 2 Green: implement the minimum immutable planning records, grouping
   verifier, deterministic allocator, and provenance evidence.
3. Phase 3 Refactor: preserve behavior, simplify responsibilities, synchronize
   documentation, and run regression checks.
4. Final review: complete the Issue/work-plan/trace packet, verify CI, and merge
   one PR.

No internal-dimension approval is required. A change to estimator meaning,
provider execution, mitigation, or result ownership invalidates this packet and
requires a new architecture review.

## Downstream relationship

- LISS-0091 may consume the plan's exact/symbolic shot and resource evidence;
  it owns broader resource feasibility, not measurement semantics.
- LISS-0092 consumes target capability and routing information; it must not
  move target constraints into this provider-neutral plan.
- LISS-0093 consumes explicit measurement cost and uncertainty evidence for
  mitigation planning; it must not mutate the raw plan silently.
- LISS-0103 owns published result and uncertainty reporting; LISS-0090 owns
  the reconstructable plan and allocation evidence consumed by that report.

## Open decisions for review

- exact confidence/interval vocabulary and whether confidence is one-sided or
  two-sided for the first implementation;
- the finite compatibility witness vocabulary for Pauli-like and general
  observable terms;
- whether covariance-aware allocation may use a declared symbolic covariance
  matrix or only named assumption classes; and
- the initial diagnostic code set and public detail-key stability policy.
