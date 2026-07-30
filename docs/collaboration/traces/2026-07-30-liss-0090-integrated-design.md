# LISS-0090 integrated design intake — 2026-07-30

[DESIGN CHECK]

- Scope and expected behavior: consolidate LISS-0090's former A–D slices into
  one provider-neutral measurement-plan contract covering observable mapping,
  compatibility/grouping, statistical targets, allocation, and provenance.
  No physical sampling, provider execution, mitigation, or published result
  reporting is included.
- Specifications and files inspected: LISS-0090 Issue, WP-0025, bounded
  feature execution packet, AT-TDD process, implementation-readiness, AI-human
  scheme, verified pass manager contract, observation checkpoint contract, and
  downstream LISS-0091/0092/0093/0103 relationships.
- Component boundaries, ports/adapters, and VO/DTO candidates: immutable
  domain DTOs (`ObservableSpec`, `MeasurementGroup`, `CompatibilityWitness`,
  `ConfidenceTarget`, `CovarianceAssumption`, `ShotAllocation`,
  `MeasurementPlan`, `MeasurementPlanDiagnostic`). No runtime port is needed
  by the core planner; provider/RNG/calibration/Job boundaries remain outside.
- Applicable constraints: Never Leave the State; terminal measurement remains
  explicit; no target/provider data in the plan; exact or symbolic quantities;
  no silent grouping, rounding, fallback, or reinterpretation.
- Decisions, assumptions, and unresolved ambiguities: the four former slices
  are review dimensions, not approval gates. Confidence interval direction,
  compatibility witness vocabulary, covariance representation, and diagnostic
  codes/detail keys remain open for Architecture/design review.
- Included and omitted AI context: included the Issue, roadmap row, relevant
  contracts, and direct downstream boundaries. Omitted provider SDKs, runtime
  adapters, unrelated compiler modules, private data, and live calibration.
- Task routing: strong reasoning review for the statistical contract and
  deterministic code assistant for the later integrated Red/Green/Refactor;
  deterministic test runner and `py_compile` for verification.
- Input/output evidence contract when AI output is involved: repository-local
  literals only; design decisions must cite the Issue/spec/ADR boundary; no AI
  output is runtime input; tests must expose diagnostic and provenance evidence.
- Verification plan: document topology audit, `git diff --check`, and later one
  integrated Red suite using `SIM0_EXACT` and `CH1_DIGITAL_RESEARCH` fixtures.

## Consolidation finding

The DTO, grouping, and allocation dimensions form one dataflow: allocation is
not meaningful without reconstructable groups, and groups are not reviewable
without compatibility evidence and an uncertainty target. Splitting them into
four phase gates would allow an incomplete statistical contract to appear green
in isolation. LISS-0083, LISS-0087, and LISS-0089 already establish the desired
Issue-level integrated cycle, so LISS-0090 adopts the same topology.

## Downstream map

```text
LISS-0083 plan + LISS-0087 verified boundary
                    |
                    v
          LISS-0090 measurement plan
             /          |          \\
            v           v           v
       LISS-0091    LISS-0092    LISS-0093
       resources    target use   mitigation
            \\           |           /
             \\          v          /
              ---> LISS-0103 result/uncertainty report
```

## Phase 1 Red and Phase 2 Green result

The integrated Red suite was added and executed. It contains 11 tests and
reported 0 passed / 11 failed because `compiler.staqex.measurement_plan` is
not implemented. This is the expected API-absence Red state. `py_compile` and
`git diff --check` passed; `compiler/` was not changed.

The current stop condition is Red review and explicit Phase 2 Green approval.
That approval was received. `compiler/staqex/measurement_plan.py` now contains
the minimum immutable DTOs, deterministic verifier, allocation, and provenance
implementation. The integrated Red suite is 11 passed / 0 failed. Related
POVM, local observation, Algorithm Plan IR, and Verified Pass suites also pass;
`py_compile` and `git diff --check` pass. Reviewed Red assertions are
unchanged. Provider integration, sampling, mitigation, and result publication
remain outside the implementation.

The current stop condition is explicit Phase 3 Refactor approval.

## Phase 3 Refactor result

Refactor extracted identity, group, statistical-policy, allocation, and
provenance verification helpers. Behavior, DTO signatures, diagnostic order,
and reviewed assertions were preserved. The integrated suite remains 11
passed / 0 failed; POVM, local observation, Algorithm Plan IR, Verified Pass,
`py_compile`, and `git diff --check` remain green.

The equal-weight allocation is intentionally the first explicit policy. A
future covariance estimator requires a reviewed extension of the statistical
contract; it is not hidden in this refactor.

## Final-review-ready packet

The Issue and WP-0025 are now marked `final-review-ready`. The exact local
verification is: integrated measurement plan 11 passed; POVM 3 passed; local
observation execution 4 passed; Algorithm Plan IR 10 passed; Verified Pass 10
passed; `py_compile` passed; and `git diff --check` passed. Reviewed Red
assertions are unchanged and the worktree is clean before the completion PR.

Remaining risks are limited to the explicitly bounded first-contract policy:
equal-weight allocation is deterministic, while richer covariance estimators,
provider execution, sampling, mitigation, and published result ownership stay
outside LISS-0090.

Current stop condition: open the completion PR while this packet is
`final-review-ready`; after its number is known, update all three completion
artifacts to `complete`, run `scripts/check-completion-packet.py`, and wait for
CI before merge.
