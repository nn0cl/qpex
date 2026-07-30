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

## Stop condition

This is a design-only update. Architecture/design review and integrated Phase
1 Red approval are required before tests or implementation are written.
