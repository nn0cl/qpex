# Staqex v1 verified pass manager

## Purpose and authority

This document is the implementation-facing contract for LISS-0087. The
LISS-0087 Issue is authoritative for scope, acceptance, status, and approval
state. WP-0025 is authoritative for roadmap ordering and dependencies. This
specification is authoritative for pass/result/configuration DTOs, invariant
verification, hard-stop orchestration, provenance, and deterministic pipeline
composition.

LISS-0087 is one implementation unit. Pass records, verifier orchestration,
exactness propagation, composition, and CH0/NH5 fixtures are internal review
dimensions, not separate Issues, branches, Red/Green/Refactor cycles, or
approval gates.

## Boundary

The verified pass manager consumes a verified Semantic or Algorithm Plan
module and returns an immutable result with evidence:

```text
verified Semantic/Plan input -> verified pass -> verified result / hard stop
                                                -> later pass or backend
```

Every pass is provider-neutral. A pass may transform a plan only under an
explicit configuration and must preserve or discharge provenance and
exactness obligations. A failed precondition, postcondition, or invariant
stops the pipeline; no later pass or backend may be called.

Candidate implementation files are limited to:

- `compiler/staqex/verified_pass.py`
- `tests/test_verified_pass_*.py`
- synchronized Issue, work-plan, specification, and trace documents

Forbidden in this Issue: pass-specific algorithm policy, mutable global
registries, backend fallback, provider SDKs, target selection, gate emission,
and silently swallowed diagnostics. LISS-0088 owns algorithm selection;
LISS-0089 owns exact circuit transformations; LISS-0090/0091 own measurement
and resource planning; LISS-0094 and later Issues own target adapters.

## Integrated contract

| Record family | Required meaning | Required evidence |
|---|---|---|
| Pass identity/configuration | Pass identity, version, configuration identity, and input/output schema are explicit and immutable | canonical serialization and identity diagnostics |
| Pass result | Output, exactness class, provenance, diagnostics, and success/failure state travel together | deterministic result contract |
| Invariant boundary | Precondition and postcondition verification run around every pass | invalid output is rejected before downstream invocation |
| Obligation propagation | Exactness and approximation obligations are preserved, discharged, or reopened explicitly | no silent loss or closure |
| Pipeline composition | Ordering, inputs, outputs, and hard-stop behavior are deterministic | later passes are absent after failure |
| Delivery evidence | CH0 and compact NH5 plans use the same pass contract | finite and compact structural fixtures |

### Required verifier laws

The integrated verifier must reject:

1. mutable input or output objects, missing pass/configuration identity, or
   provenance gaps;
2. a pass invoked without verified input or with a failed precondition;
3. output that fails its postcondition or changes exactness/obligations without
   an explicit disposition;
4. nondeterministic configuration, diagnostic order, or pipeline ordering;
5. downstream invocation after any failed check; and
6. backend fallback or provider-specific data entering the pass-domain
   contract.

It must accept a verified no-op/pass-through result, a verified exact pass,
and an explicitly bounded approximate pass whose obligation evidence remains
closed or intentionally unresolved.

Diagnostic codes and detail keys are part of the review surface. The Red
phase must name them before implementation; Green may implement only the
reviewed set.

## Integrated test contract

One Red suite covers all five internal dimensions. It must include:

- immutable pass/configuration/result records;
- deterministic precondition and postcondition failures;
- hard stop proving that a later pass and backend spy are not called;
- exactness and approximation-obligation propagation;
- deterministic composition and diagnostic ordering;
- provenance continuity across a multi-pass chain; and
- one CH0 current-hardware fixture plus one compact NH5 fixture using the
  same evidence contract.

Tests use repository-local literals and deterministic test doubles only. No
provider SDK, live backend, random source, or numerical solver is required.

## Execution and approval

The LISS follows one ordered cycle:

1. Architecture + Phase 1 Red: review the vocabulary, DTOs, verifier laws,
   hard-stop semantics, and integrated tests; only tests and traces change.
2. Phase 2 Green: implement the minimum immutable pass/result/configuration
   domain, verifier orchestration, and deterministic fixtures.
3. Phase 3 Refactor: preserve behavior, simplify responsibilities, synchronize
   documentation, and run regression checks.
4. Final review: complete the status packet, commit, push, open PR, verify CI,
   and merge.

No slice-level approval is required. A change to pass policy, backend
fallback, provider selection, or Semantic/Plan ownership invalidates the
approved packet and requires a new architecture review.

## Document topology

Do not create `LISS-0087-slice-*.md` files. Add durable information to the
proper artifact:

- acceptance or status change -> the LISS-0087 Issue;
- DTO/verifier or boundary change -> this specification;
- dependency or roadmap change -> WP-0025;
- execution evidence or adjudicator decision -> a dated trace.

This topology preserves review precision without multiplying approval points.
