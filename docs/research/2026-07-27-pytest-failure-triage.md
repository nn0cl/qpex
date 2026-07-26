# Pytest failure triage after LISS-0062

## Scope

This document records the first pytest sweep after the LISS-0062 resource
profile refactor. It classifies failures without changing production code,
tests, language semantics, or Issue numbering.

- Current phase: design intake / triage only
- Base: `main` at the LISS-0057 documentation-sync merge
- LISS-0062 relationship: no failing test is caused by the resource-profile
  refactor
- Verification command: `./.venv/bin/python -m pytest -q`
- Result: 311 passed, 6 failed

## Classification

| Failure | Classification | Proposed follow-up | Dependency / decision |
|---|---|---|---|
| `test_product_deferral_is_explicitly_diagnosed` | stale acceptance expectation | Update or retire the old Red contract after confirming LISS-0055 scope | LISS-0055 completion evidence; no new implementation decision expected |
| `test_bounded_evolve_until_is_a_state_preserving_expression` | specification boundary mismatch | Review whether static QPU IR rejection is normative for `until` | LISS-0012 / ADR 0079; architecture decision required before changing code or test |
| `test_classical_harvest_from_pub_fun` | runtime bug | Add a dedicated bug Issue and reproduce the function-local value lookup failure | Function harvest/evaluator ownership; Phase 1 Red required |
| `test_harvest_collision_diagnostic` | diagnostic bug or obsolete harvest model | Pair with the runtime harvest investigation, then decide whether collision detection remains normative | Same design review as the previous row |
| `test_qft_rejects_unsupported_static_resource_size` | lowering diagnostic bug | Add a regression for hard resource rejection before numeric angle expansion | LISS-0042 / ADR 0086; preserve no-silent-fallback policy |
| `test_observatory_cpu_entry_uses_continuous_and_sparse_models` | stale example contract | Compare the example against the current accepted capstone specification and update the test or example | LISS-0016 / LISS-0036 / capstone work plan; documentation/example review first |

## Dependency graph

```text
LISS-0055 completion evidence
    └─ product Red-contract cleanup

LISS-0012 / ADR 0079
    └─ evolve-until boundary decision

function harvest model review
    ├─ local-value runtime crash
    └─ collision diagnostic

LISS-0042 / ADR 0086
    └─ QFT resource-overflow diagnostic

capstone specification / LISS-0036
    └─ Observatory example contract sync
```

The harvest pair should be handled together because both failures concern the
same cross-module configuration harvest boundary. The remaining four items
should not be merged into that bug work.

## Recommended order

1. Confirm the two stale-contract cases (`product` and Observatory) against
   their accepted Issue/ADR records; update tests or documentation only after
   that comparison.
2. Make the `evolve until` decision explicit in LISS-0012/ADR 0079. Do not
   make the test pass by weakening the QPU capability rejection.
3. Open one M-sized bug Issue for the two harvest failures and begin with
   Phase 1 Red reproduction if the behavior remains normative.
4. Open one S/M-sized bug Issue for the QFT overflow-to-diagnostic path and
   begin with Phase 1 Red.

## Explicit non-goals

- No changes to LISS-0062 implementation or its resource formulas.
- No new LISS numbers are assigned by this research note.
- No pytest failures are silenced, marked expected, or removed.
- No implementation phase is authorized by this triage document.

## Approval points

Adjudicator approval is required before:

- promoting any row into a new or existing LISS;
- changing an accepted ADR or its test contract;
- starting Phase 1 Red for a bug or feature;
- changing the Observatory example as an acceptance artifact.

