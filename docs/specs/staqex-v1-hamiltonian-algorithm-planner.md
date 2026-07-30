# Staqex v1 Hamiltonian and Algorithm Planner Contract

## Purpose and authority

This specification defines the provider-neutral planning contract for
LISS-0088. The LISS-0088 Issue is authoritative for scope, acceptance
scenarios, status, and approval state. WP-0025 and WP-0029 are authoritative
for roadmap order and delivery profiles. LISS-0083 remains authoritative for
the Algorithm Plan IR DTOs, exactness obligations, provenance, and consumer
projection boundary.

LISS-0088 is one implementation unit. Candidate evaluation, Suzuki, QDrift,
state preparation, bounded Krylov/QFT, and deferred fault-tolerant methods are
internal review dimensions, not separate Issues, branches, Red/Green/Refactor
cycles, or approval gates.

## Boundary

The planner consumes a verified Semantic/Algorithm Plan context and produces a
provider-neutral planning decision. It does not emit gates, call a simulator,
select a provider, bind credentials, run a numerical solver, or mutate the
source Semantic IR or Algorithm Plan IR.

```text
Semantic IR -> Algorithm Plan IR -> Hamiltonian planner -> verified pass
                                             |          -> simulator/QPU plan
                                             `-> explicit rejection evidence
```

Candidate implementation files are limited to:

- `compiler/staqex/algorithm_planner.py`
- `tests/test_algorithm_planner_integrated_red.py`
- synchronized Issue, this specification, WP-0025/WP-0029 references, and a
  dated trace

No provider SDK, target adapter, numerical library, or network dependency is
permitted in this Issue.

## Integrated contract

The following records are immutable and provider-neutral. Names are provisional
until Phase 1 Red review.

| Record | Required meaning |
|---|---|
| `PlannerRequest` | Hamiltonian/observable identity, semantic provenance, requested evolution or preparation, delivery profile, and declared constraints |
| `AlgorithmCandidate` | method family, order/step parameters or symbolic bounds, preparation mode, and capability prerequisites |
| `CandidateEvaluation` | accepted/rejected/unsupported disposition, alternatives, assumptions, rejection reasons, policy provenance, and resource/approximation obligations |
| `PlannerDecision` | deterministic selected candidate or explicit rejection; never hidden runtime adaptation |
| `PreparationContract` | explicit initial-state source, preparation obligations, and whether an oracle or zero-state assumption is forbidden |
| `PlannerProfile` | profile identifier and non-semantic resource envelope; current profiles and NH5 stress profiles are fixtures, not language limits |

All records preserve the source/Physics/Semantic provenance already required by
LISS-0083. Exact and approximate obligations are represented through the
Algorithm Plan IR contract rather than a second ledger.

## Supported and deferred method boundary

P1 implementation scope:

- Suzuki orders and bounded step policies whose error/resource obligations are
  explicit and closed;
- QDrift with explicit sampling, error, and resource obligations;
- hardware-efficient preparation only when its target prerequisites and
  preparation evidence are explicit;
- deterministic candidate evaluation against `SIM0_EXACT` and
  `CH1_DIGITAL_RESEARCH`, with compact `NH5_NISQ_MODULAR` or `NH5_FT_MEGA`
  stress fixtures where symbolic scale matters.

The following remain explicit `unsupported` or `deferred` dispositions until
their separate mathematical and target prerequisites are accepted:

- bounded Krylov and QFT variants beyond the reviewed P1 witness;
- fault-tolerant qubitization and LCU;
- provider-specific, runtime-adaptive, heuristic “best method” selection;
- hidden zero-state, oracle, calibration, credential, or target SDK assumptions.

An unsupported result is valid evidence when it names the missing prerequisite
and preserves the original request/provenance.

## Verifier laws

The integrated planner/verifier must reject:

1. a candidate with incomplete source/Physics/Semantic provenance;
2. an approximate method without a bound/estimate, disposition, and closed
   obligation;
3. a selection without alternatives, assumptions, rejection reasons, and
   policy provenance;
4. a preparation that silently assumes `|0>` or an oracle;
5. a candidate requiring a profile/provider field not declared by the request;
6. runtime-adaptive or provider-specific policy in semantic planning meaning;
7. resource or repetition expressions that are eagerly expanded or silently
   narrowed to machine values; and
8. a deferred/unsupported method presented as accepted.

It must accept exact plans, explicitly bounded approximate plans, explicit
unsupported decisions, symbolic resource expressions, and consumer-neutral
projections over the unchanged source plan.

Diagnostics are deterministic and stable within the reviewed contract. The Red
phase must name the diagnostic codes and detail keys before Green.

## Delivery profiles

The first witness matrix is:

| Profile | Role in this Issue |
|---|---|
| `SIM0_EXACT` | deterministic exact oracle for small Suzuki and preparation cases |
| `CH1_DIGITAL_RESEARCH` | current-machine digital witness with target-resolved bounded resources |
| `NH5_NISQ_MODULAR` | compact symbolic stress for larger physical carrier counts |
| `NH5_FT_MEGA` | compact symbolic stress for large logical operation budgets; no delivery claim |

`CH1_ANALOG_RESEARCH`, `NH5_FT_GIGA`, and `NH5_NATIVE_LARGE` remain named
future integration profiles, not implementation requirements for this Issue.
Profile numbers never become semantic maxima.

## Integrated test contract

One Red suite must cover all internal dimensions:

- exact Suzuki candidate accepted;
- bounded approximate Suzuki and QDrift candidates accepted only with closed
  obligations;
- explicit hardware-efficient preparation accepted only with preparation
  evidence;
- missing provenance, missing alternatives, missing approximation evidence,
  hidden zero-state/oracle, runtime adaptation, provider leakage, and deferred
  method selection rejected;
- symbolic resource expressions and repetitions remain compact;
- deterministic alternatives, diagnostics, and serialization are stable; and
- `SIM0_EXACT`, `CH1_DIGITAL_RESEARCH`, and one NH5 compact fixture consume the
  same provider-neutral decision contract.

Fixtures use repository-local literals and deterministic doubles. No live QPU,
provider SDK, network, random source, or numerical solver is part of Red or
Green.

## Execution and approval

The Issue follows one ordered cycle:

1. Architecture + Phase 1 Red: review this contract and add only the
   integrated failing tests and design trace.
2. Phase 2 Green: implement the minimum planner DTOs, evaluator, verifier
   integration, and fixtures needed by the reviewed tests.
3. Phase 3 Refactor: preserve behavior, simplify boundaries, synchronize
   documentation, and run regression checks.
4. Final review: commit, push, open PR, verify CI, and merge after approval.

No method-specific slice approval is required. Adding a numerical dependency,
provider adapter, target SDK, runtime adaptation, or semantic mutation
invalidates this contract and requires a new Architecture Path decision.
