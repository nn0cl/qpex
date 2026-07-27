# LISS-0062: Resource profile manifest and simulator budget

## Metadata

- Local issue ID: LISS-0062
- GitHub issue: none
- Status: Phase 3 complete
- Phase: Feature Path — Phase 1 Red → Phase 2 Green → Phase 3 Refactor complete
- Type: Host configuration + simulator planning
- Priority: P2
- Initial planning size: M
- Current planning size: TBD
- Owner/agent: Codex
- Related ADR: [ADR 0100](../architecture/adr/0100-resource-budget-policy.md)

## Summary

Load a user-editable `qpex.toml` resource profile, apply versioned defaults,
validate it before compilation, and provide a representation-aware simulator
resource estimate without putting file-system policy in the Kernel.

## Proposed manifest

```toml
schema_version = 1

[resources.binder]
term_limit = 100_000
policy = "Abort"

[resources.simulator]
policy = "Abort"
memory_limit_bytes = 8_589_934_592
```

## Acceptance scenarios

```gherkin
Given no manifest is present
When a source is compiled
Then the versioned default ResourceProfile is used
```

```gherkin
Given qpex.toml with schema_version = 1
When the Host configuration adapter loads it
Then it returns an immutable ResourceProfile DTO
And the Kernel receives the DTO rather than reading the file
```

```gherkin
Given a StateVector, DensityState, or Lindblad RK4 simulation
When a resource estimate is requested
Then the representation-aware formula and formula_version are recorded
```

```gherkin
Given a simulator estimate above memory_limit_bytes
When policy is Warn
Then local simulation emits SIMULATOR_RESOURCE_WARNING
But QASM and QPU lanes reject with SIMULATOR_RESOURCE_ERROR
```

## Proposed formulas

```text
complex_f64_bytes = 16
StateVector:  2^n × 16 × 3
DensityState: 4^n × 16 × 3
Lindblad RK4: 4^n × 16 × 6
```

The factors are provisional and require benchmark evidence before Green.

## Diagnostics

- `RESOURCE_MANIFEST_NOT_FOUND`
- `RESOURCE_MANIFEST_PARSE_ERROR`
- `RESOURCE_MANIFEST_SCHEMA_ERROR`
- `RESOURCE_SETTING_INVALID`
- `SIMULATOR_RESOURCE_WARNING`
- `SIMULATOR_RESOURCE_ERROR`

## Phase 1 boundary candidates

The Red tests use a small dependency-free boundary which the Green
implementation may realize without exposing TOML or file-system objects to
the Kernel:

```text
load_resource_profile(manifest_path, project_root) -> ResourceProfile
estimate_simulator_resources(representation, logical_qubits)
    -> SimulationResourceEstimate
```

The returned values are immutable and diagnostics remain structured records.
The names are part of the reviewed test boundary for this slice; internal
parsing helpers remain free to change.

## Non-goals

- TOML parsing inside the Kernel.
- Provider credentials or QPU target capability discovery.
- CPU-time prediction in the first slice.
- Truncation, normalization, or silent state reduction.

## Adjudicator decision points

- [x] Approve the manifest loader boundary and lookup order.
- [x] Approve the default `memory_limit_bytes` for the initial profile.
- [x] Approve the estimator workspace factors for the dependency-free MVP.
- [x] Approve Phase 1 Red tests.

The approved slice is intentionally limited to the Host configuration DTO and
the deterministic estimator. Runtime enforcement and benchmark calibration are
follow-up work, not implicit parts of this Issue.

## Phase 2 Green record

- Added the dependency-free `compiler/qpex/resource_profile.py` boundary.
- `qpex.toml` loading uses `schema_version = 1`, explicit path precedence,
  project-root lookup, and versioned defaults.
- Invalid schema, malformed TOML, missing explicit files, and invalid settings
  produce structured diagnostics without silent repair.
- StateVector, DensityState, and Lindblad RK4 estimates use the reviewed
  representation-aware formulas and record `formula_version`.
- Phase 1 Red tests now pass: 4/4.
- CLI integration, QASM/QPU lane enforcement, benchmark validation, and CPU
  work estimation remain outside this Green slice.

## Phase 3 review record

- Kept manifest lookup, validation diagnostics, immutable DTOs, and estimator
  formulas unchanged from the accepted Green slice.
- Kept the Kernel independent from TOML and file-system policy.
- Recorded the provisional formula factors and default memory limit as explicit
  follow-up calibration items rather than presenting them as hardware facts.
- Verification: focused resource-profile tests, Python compilation, and
  `git diff --check` passed.

Phase 3 is complete for the dependency-free Host configuration and estimator
boundary. CLI enforcement, QASM/QPU lane policy application, benchmark-backed
factor calibration, and CPU work estimation remain separate follow-ups.

Runtime enforcement is now tracked separately as
[LISS-0063](LISS-0063-simulator-resource-enforcement.md). This Issue remains
complete for the manifest and deterministic estimator boundary.
