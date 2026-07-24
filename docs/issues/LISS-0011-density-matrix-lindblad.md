# LISS-0011: Density matrix and Lindblad CPTP semantics

## Metadata

- Local issue ID: LISS-0011
- GitHub issue: none
- Status: **Phase 3 reviewed; numeric and one-qubit symbolic slices complete**
- Phase: Feature Path — Phase 3 Refactor complete
- Type: architecture + language semantics
- Priority: P1
- Initial planning size: XL
- Current planning size: TBD
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

## Summary

Specify the mixed-state extension covered by ADR 0057: density matrices,
partial trace, and completely positive trace-preserving Lindblad evolution.
This issue is design-only until the representation and `State<T>` boundary are
accepted.

## Acceptance Notes

- [x] ADR 0057 is updated with an accepted representation.
- [x] Pure-state compatibility and `measure` collapse semantics are specified.
- [x] CPTP/Lindblad time evolution and trace preservation have numeric observable cases.
- [x] Partial trace and subsystem composition have typed contract boundaries.
- [x] Kernel/SV scope and non-goals are recorded before implementation.

## Dependencies

- Parent: none
- Depends on: ADR 0018, ADR 0016, LISS-0019 if concrete QPU IR is needed
- Blocks: mixed-state Kernel implementation
- Related: ADR 0057, `docs/architecture/qpex-stdlib-combinators.md`
- Architecture proposal: [ADR 0057](../architecture/adr/0057-density-cptp-lindblad.md)
- Acceptance specification: [`qpex-density-cptp-lindblad.md`](../specs/qpex-density-cptp-lindblad.md)

## Adjudicator Decision Points

- [x] Choose density matrix representation and ownership of trace/positivity checks.
- [x] Decide whether Lindblad is Kernel CPU-only MVP or a later port.
- [x] Define terminal measurement and host-sink behavior for mixed states.

## Context

- Included: density matrices, CPTP maps, Lindblad evolution, partial trace.
- Omitted: vendor QPU APIs, quantum chemistry, and pulse-level simulation.
- Assumptions: Never Leave the State remains the language law.

## AI Planning Records

### AIP-0011-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: XL
- Intended execution route: Architecture Path; no implementation.
- Intended scope: accepted representation and observable semantics only.
- Estimation basis: new state model and multiple architecture boundaries.
- Assumptions: no third-party dependency is selected.
- Confidence: medium

## Verification

- Architecture review checklist completed for the accepted contract boundary.
- Numeric density/CPTP/Lindblad verification is covered by the completed
  numeric and runtime slices below.

## Phase 1 design record

The proposal preserves pure `State<T>` and introduces a distinct finite
`DensityState<T>` plus typed CPTP `Channel<A, B>` contracts. Lindblad is
proposed for an explicit CPU/simulator lane first. Terminal `measure` remains
the only observation boundary, and LISS-0037 remains dependent on this
representation decision. The architecture review accepted these choices,
including the MVP channel constructors and mixed-state measurement metadata.

The architecture review approved the representation and numerical boundary.
Phase 1 Red acceptance tests were then reviewed and executed before the
contract-only implementation slice.

## Phase 1 Red record

- Acceptance tests: [`test_density_cptp_lindblad_red.py`](../../tests/test_density_cptp_lindblad_red.py)
- Proposed surface: `DensityState<T>`, typed `Channel<A, B>`, explicit
  `pure_to_density`, `partial_trace`, `lindblad`, and terminal `measure`.
- The tests were initially Red until the mixed-state contract was exposed and
  pure-state/channel mixing was rejected; they now serve as the contract
  acceptance tests for the Green slice.

## Phase 2 Green record

- Implementation: [`mixed_state.py`](../../compiler/qpex/mixed_state.py),
  [`pipeline.py`](../../compiler/qpex/pipeline.py), and the public export in
  [`__init__.py`](../../compiler/qpex/__init__.py).
- `CompileResult.mixed_state_contracts` exposes immutable contract metadata for
  `DensityState<T>` and typed `Channel<A, B>` bindings.
- Explicit operations are recognized for `pure_to_density`, `apply`,
  `partial_trace`, and `lindblad`; applying a channel to `State<T>` produces the
  hard diagnostic `MIXED_STATE_TYPE_ERROR`.
- Verification: the LISS acceptance tests pass, the standalone suite passes,
  and Spec Verification remains 165/165 (100%).
- Scope limit: no numeric density matrix storage or Lindblad integrator is
  shipped in this slice. Constructor positivity/trace arithmetic and explicit
  numeric Kraus completeness validation are included below.

## Completed slice boundary

The finite numeric constructors, dependency-free fixed-step RK4 runtime,
source-level integration, explicit numeric jumps, and one-qubit symbolic jump
lowering are complete. LISS-0037 may use this accepted mixed-state boundary.
General operator algebra, adaptive integration, positivity projection, and
provider/QPU execution remain deferred follow-ups.

## Phase 0 design intake for the numeric slice

The next Red tests must make the following observable cases explicit:

- a finite density value is accepted only when trace and positivity evidence
  are valid;
- malformed density values are rejected without silent normalization;
- a Kraus channel is accepted only when completeness is established;
- Lindblad evolution is explicitly classified as CPU/simulator-only and
  preserves the declared numerical trace tolerance.

ADR 0057 now accepts the uniform `DensityState(...)` constructor with
`Ensemble` and `RawMatrix` inputs. Numeric storage format, precision
implementation, and dependency policy remain open technology decisions and
must not be guessed by Phase 1 tests.

## Numeric slice Phase 1 Red record

- Acceptance tests: [`test_density_cptp_lindblad_numeric_red.py`](../../tests/test_density_cptp_lindblad_numeric_red.py)
- Covered cases: invalid trace, non-positive matrix, valid `Ensemble`, valid
  `RawMatrix`, incomplete Kraus completeness, and explicit Lindblad
  construction.
- Expected Red evidence: the first malformed-density case fails because
  `MALFORMED_DENSITY_STATE` is not implemented yet.
- No production implementation or numeric dependency was added in this phase.
- Gate result: Adjudicator reviewed and approved these tests for Phase 2 Green.

## Numeric slice Phase 2 Green record

- `ListExpr` supports the explicit list inputs required by `Ensemble`,
  `RawMatrix`, and `KrausChannel`.
- `RawMatrix` validates square finite real matrices, trace one, Hermiticity,
  and the 2×2 positive-semidefinite bound with the declared `1e-12`
  tolerances.
- `Ensemble` validates finite non-negative weights and trace-one weight sums.
- `KrausChannel` validates explicit real matrix completeness and rejects
  symbolic or incomplete evidence with `INCOMPLETE_KRAUS_CHANNEL`.
- No numeric dependency, runtime density storage, or Lindblad integrator was
  added. The Lindblad test remains a contract-construction boundary only.
- Verification: numeric acceptance tests, existing mixed-state tests, the
  standalone suite, and Spec Verification 165/165 pass.

## Runtime Lindblad Phase 1 Red record

- Acceptance tests: [`test_density_cptp_lindblad_runtime_red.py`](../../tests/test_density_cptp_lindblad_runtime_red.py)
- Proposed runtime boundary: dependency-free `runtime.lindblad` using the
  existing complex matrix type, finite Liouvillian action, and fixed-step RK4.
- Covered cases: amplitude-damping trace preservation and reference value,
  deterministic fixed-step execution, and hard `NumericalTraceDefect` failure.
- Expected Red evidence: the test currently fails because the Lindblad runtime
  module does not exist.
- Phase 2 Green implementation: [`runtime/lindblad.py`](../../compiler/qpex/runtime/lindblad.py)
  uses the existing dependency-free `Matrix` type and fixed-step RK4.

## Runtime Lindblad Phase 2 Green record

- `lindblad_rhs` implements the finite Lindblad master-equation right-hand
  side using Hamiltonian and jump matrices.
- `evolve_lindblad` performs deterministic fixed-step RK4 and requires
  `total_time` to be an integer multiple of `dt`.
- Trace is checked before evolution and after every step. Violations raise
  `NumericalTraceDefect`; no normalization or repair is performed.
- Verification: runtime Red tests now pass, along with the constructor and
  numeric validation suites, standalone tests, and Spec Verification 165/165.
- Scope limit: no adaptive stepping, positivity projection, or provider/QPU
  execution is included.

## Source-level integration Phase 1 Red record

- Acceptance tests: [`test_density_cptp_lindblad_source_red.py`](../../tests/test_density_cptp_lindblad_source_red.py)
- Covered cases: opaque mixed `JobResult` measurement metadata, CPU-lane
  source-level Lindblad execution, and preservation of the pure/channel hard
  boundary.
- Initial Red evidence: `run_source()` returned a runtime error for the
  unimplemented `DensityState` evaluator call.

## Source-level integration Phase 2 Green record

- `DensityStateValue` is maintained in a dedicated evaluator lane and is not
  inserted into the pure-state `Joint`.
- `DensityState(...)`, source-level `lindblad(...)`, and terminal `measure`
  are bridged to the existing Host `JobResult` boundary.
- Mixed results expose `state_type = DensityState` and the CPU lane in Host
  metadata; raw matrix storage is not exposed.
- Scope limit: source-level symbolic Hamiltonian/jump lowering records the CPU
  lane and preserves the finite state. Explicit numerical evolution remains
  available through `runtime.lindblad`; numeric `JumpSet([RawMatrix(...)])`
  lowering is covered by LISS-0039, while one-qubit symbolic jump lowering is
  covered by LISS-0040.
- Verification: all mixed-state suites, standalone tests, and Spec
  Verification 165/165 pass.

## Symbolic Lindblad lowering Phase 1 Red record

- Acceptance test: [`test_density_cptp_lindblad_symbolic_red.py`](../../tests/test_density_cptp_lindblad_symbolic_red.py)
- Covered case: source `Operator H = X`, finite `RawMatrix` input, empty jump
  list, and explicit time `0.1` must lower to numerical unitary evolution
  before terminal measurement.
- Expected Red evidence: the current source bridge preserves the input state,
  so the expected non-zero `|1>` probability is absent.
- Next Green scope: resolve source Hamiltonian matrices and time literals,
  invoke the existing numeric Lindblad runtime, and preserve the opaque Host
  boundary. One-qubit symbolic jump lowering is separately tracked by
  LISS-0040; broader operator lowering remains deferred.

## Symbolic Lindblad lowering Phase 2 Green record

- Explicit source inputs resolve a one-qubit `Operator` and numeric time
  literal, then invoke the dependency-free fixed-step RK4 runtime.
- Empty jump lists, explicit numeric `JumpSet([RawMatrix(...)])` inputs, and
  bound one-qubit symbolic `Operator` jumps are supported by the completed
  MVP. General operator lowering remains deferred.
- Unresolved `H`, `jumps`, or `t` values remain an opaque contract path; they
  are not silently converted to numerical defaults.
- Verification: symbolic, source integration, numeric, runtime, standalone,
  and Spec Verification 165/165 pass.

## Phase 3 review record

- Numeric, runtime, source, explicit-jump, and one-qubit symbolic-jump slices
  were reviewed together against ADR 0057 and their companion LISS issues.
- Reviewer empathy: pure `State<T>`, finite `DensityState<T>`, CPU numerical
  execution, and opaque Host results remain separate boundaries.
- Verification: all mixed-state suites, standalone tests, and Spec
  Verification 165/165 pass.
