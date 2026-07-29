# WP-0025: QPex v1 north-star language and compiler

## Status

Proposed Architecture Path work plan. No listed Issue has implementation
approval merely because it appears here.

## Goal

Evolve the shipping QPex Kernel into the language described by ADR 0106:

- a physicist writes theory and experiment intent directly;
- the compiler preserves mathematical meaning through typed IR;
- simulation, OpenQASM 3.1, QIR, and QPU submission share contracts;
- every approximation and target decision is explicit and reproducible;
- static and dynamic quantum control remain semantically separated.

## Planning classification

- Initial size: XL
- Current size: XL
- Route: Architecture Path for the roadmap; Feature Path per implementation
  Issue
- Canonical planning record: AIP-WP-0025-001 below
- First executable unit: LISS-0068

## AIP-WP-0025-001

- Status: proposed
- Created by:
  - Agent/environment: Codex desktop
  - Model as displayed: GPT-5
  - Reasoning setting as displayed: not exposed
- Created at: 2026-07-27
- Planning size: XL
- Intended execution route: Architecture review, then one Feature Path branch
  per approved LISS
- Intended scope: normative rebaseline, source/frontend, IR, optimization,
  simulator/QPU backends, Host workflow, and product validation
- Estimated token range: N/A
- Estimated token midpoint: N/A
- Token metric: unavailable in the environment
- Estimation basis: N/A
- Assumptions: Python remains the executable reference; Rust remains the
  long-term target; provider and dependency choices require separate approval
- Confidence: medium-high for boundaries, medium for technology sequencing
- Revises: none
- Revision reason: none
- Superseded by: none

## Principles governing every Issue

1. Ideal final form under ADR 0095; no compatibility alias merely to avoid a
   migration.
2. One language semantics; Python and future Rust implementations use one
   conformance corpus.
3. No implementation without accepted scenarios and phase approval.
4. No hidden normalization, truncation, mapping, approximation, mitigation,
   fallback, measurement, or Host emulation.
5. Formula-to-source and source-to-observable evidence is required for every
   language capability.
6. Provider SDKs, credentials, files, and network remain adapters behind ports.
7. Each approximation and target transform preserves provenance.

## Epic and phase overview

| Delivery phase | Epic | Outcome |
|---|---|---|
| Phase A | E0 — specification and conformance | one versioned v1 contract |
| Phase B | E1 — source and frontend | paper-shaped, statically safe source |
| Phase C | E2 — semantic IR | meaning-preserving multi-level pipeline |
| Phase D | E3 — planning and optimization | explicit algorithms and target planning |
| Phase E | E4 — simulators and portable backends | validated simulator/OpenQASM/QIR artifacts |
| Phase F | E5 — Host workflow and tooling | real data to reproducible results |
| Phase G | E6 — validation and release | capstones, benchmarks, migration, release gate |

Phases describe roadmap order, not AT-TDD permission. Every LISS still moves
through Phase 0, Phase 1 Red, Phase 2 Green, and Phase 3 Refactor independently.

## E0 — Specification and conformance

### LISS-0068 — Rebaseline the normative v1 specification

- Priority/size: P0 / XL
- Depends on: Adjudicator review of ADR 0106
- Action:
  - inventory every accepted ADR through ADR 0105;
  - reconcile the v0.1 normative specification, EBNF, diagnostic list, and
    examples;
  - classify each v1 proposal as preserved, additive, or breaking;
  - publish EARS/Gherkin acceptance envelopes and a versioning policy.
- Acceptance:
  - no accepted behavior is accidentally lost;
  - every contradiction has one authoritative resolution;
  - every breaking change has a migration and removal plan;
  - no implementation is changed in this Issue's design slice.

### LISS-0069 — Canonical mathematical source and migration

- Priority/size: P0 / XL
- Depends on: LISS-0068
- Action:
  - specify Unicode normalization, identifier profile, confusable diagnostics,
    Dirac tokens, `†`, and `⊗`;
  - specify removal of permanent ASCII aliases;
  - build a source migrator contract and formatter golden corpus.
- Acceptance:
  - one canonical emitted spelling;
  - no collision with `|>`;
  - round-trip comments/spans preserved;
  - every v0.1 example has deterministic migrated output.

### LISS-0070 — [延期 / 次期バージョン] Rust compiler infrastructure

- Priority/size: deferred / L (was P0 for current shipping track)
- Status: **deferred to next version** (Adjudicator 2026-07-28)
- Depends on: LISS-0068
- Shipping note: current Shipping Kernel remains Python (`compiler/qpex/`).
  Rust VM/simulator is a later-generation implementation behind the same
  language semantics — not a current gate for language-spec work.
- Decision (when resumed):
  - custom Rust IR only;
  - custom high-level IR plus selective MLIR;
  - broader MLIR dialect adoption.
- Required evidence:
  - minimal Physics IR and provenance POC;
  - build/distribution complexity;
  - dependency and vulnerability review;
  - diagnostic/source-span quality;
  - QIR/LLVM interoperability;
  - contributor cognitive cost.
- Recommended default: custom Rust HIR/Physics/Quantum IR, optional MLIR below
  Algorithm Plan IR.

### LISS-0071 — Versioned conformance and differential oracle

- Priority/size: P0 / XL
- Depends on: LISS-0068
- Action:
  - define valid, invalid, semantic, numerical, provenance, and backend
    conformance suites;
  - establish a **Python-reference** oracle first; Rust differential execution
    is postponed with LISS-0070;
  - define tolerance and nondeterminism policy;
  - eliminate generated-report drift from ordinary test runs.
- Acceptance:
  - each language claim maps to a stable scenario;
  - no implementation-private dictionary is a public oracle;
  - numerical comparisons state precision and confidence policy.

## E1 — Source and frontend

### LISS-0072 — Lossless CST, formatter, and source versioning

- Priority/size: P0 / L
- Status: **complete — Slice A–D** (2026-07-28)
- Depends on: LISS-0069
- Note: Python Kernel CST/formatter may proceed without LISS-0070 (Rust deferred).
- Action: implement lossless token/CST structure, comments, formatting,
  source-version markers, and migration fix-its.
- Acceptance: parse-format-parse preserves AST and comments; malformed Unicode
  has precise diagnostics.

### LISS-0073 — Named Dirac notation and algebra AST

- Priority/size: P0 / XL
- Status: **complete — Slice A–G** (2026-07-29)
- Depends on: LISS-0069, LISS-0072
- Plan: [`qpex-v1-dirac-algebra-ast-plan.md`](../specs/qpex-v1-dirac-algebra-ast-plan.md)
- Action: parse Kets, Bras, matrix elements, projectors, adjoints, tensor
  products, commutators, and anticommutators into one typed algebra model.
- Acceptance: formula-to-AST mappings are unambiguous; domain mismatches and
  pipeline collisions are hard errors; no macro/string semantics.

### LISS-0074 — Qutrit, qudit, and finite local-dimension types

- Priority/size: P0 / L
- Status: **complete** (2026-07-29); D=3 SV → [LISS-0112](../issues/LISS-0112-qutrit-qudit-d3-statevector-mvp.md) **complete**
- Depends on: LISS-0068, LISS-0071
- Plan: [`qpex-v1-qudit-local-dimension-plan.md`](../specs/qpex-v1-qudit-local-dimension-plan.md)
- Issue: [`LISS-0074`](../issues/LISS-0074-qutrit-qudit-finite-local-dimension-types.md)
- Action: add `QutritRegister<N>` and `QuditRegister<D,N>`, basis-label
  checking, acting-space algebra, and target capability requirements.
- Acceptance: invalid Ket labels and incompatible local dimensions fail before
  lowering; no integer-array equivalence is exposed.

### LISS-0112 — Qutrit / qudit D=3 state-vector MVP

- Priority/size: P0 / L
- Status: **complete** (2026-07-29)
- Depends on: LISS-0074 **complete**
- Plan: [`qpex-v1-qudit-d3-sv-plan.md`](../specs/qpex-v1-qudit-d3-sv-plan.md)
- Issue: [`LISS-0112`](../issues/LISS-0112-qutrit-qudit-d3-statevector-mvp.md)
- Action: real dim-3 Kernel SV for `State<Qutrit>` / `State<Qudit<3>>`; lift
  `UNSUPPORTED_LOCAL_DIMENSION` on measure + Identity evolve/apply(I) only.
- Acceptance: dim-3 measure and Identity paths; QASM / D≠3 remain fail-closed;
  no multi-site register SV or OpenQASM qudit opcodes in this Issue.

### LISS-0075 — Linear quantum usage and safe uncomputation

- Priority/size: P0 / XL
- Depends on: LISS-0071 **complete**, [LISS-0080](../issues/LISS-0080-phase-resolved-typed-hir.md)
  (HIR; plan intake 2026-07-29)
- Action: define ownership/borrowing or linear-use model, no-cloning,
  no-implicit-discard, ancilla lifetime, and proof-driven uncomputation.
- Acceptance: cloning/discard counterexamples fail; accepted uncomputation is
  simulator-equivalent and provenance-recorded.
- Blocked until: LISS-0080 MVP slices sufficient for linear analysis hooks.

### LISS-0076 — Body-level scientific phase typing

- Priority/size: P0 / XL
- Depends on: LISS-0068, existing LISS-0034
- Action: enforce Theory/Experiment/Workflow/Execution/Report visibility inside
  expression bodies, imports, generic calls, and methods.
- Acceptance: phase leaks produce phase diagnostics rather than unresolved-name
  or generic type errors.

### LISS-0077 — Dynamic QPU controller and feed-forward

- Priority/size: P0 / XL
- Depends on: LISS-0075, LISS-0076, LISS-0082
- Action: specify/implement `dynamic qpu fn`, `Controller<T>`, finite `match`,
  reset/reuse, timing/capability requirements, and dynamic result metadata.
- Acceptance:
  - Static Kernel terminal-measure tests remain unchanged;
  - controller values cannot escape or control shape;
  - supported simulator execution is deterministic under supplied outcomes;
  - unsupported targets fail explicitly.

### LISS-0078 — Function, interface, pipeline, and effect consolidation

- Priority/size: P1 / L
- Depends on: LISS-0068, LISS-0076
- Action: make function types, partial application, interface dispatch, effect
  propagation, and `return` one coherent typed model.
- Acceptance: wrappers and pipelines cannot hide effects; coherence and
  visibility diagnostics survive module linking.

### LISS-0079 — Typed scientific input declarations

- Priority/size: P1 / L
- Depends on: LISS-0076, existing LISS-0045
- Action: define source declarations for Host-bound scalar, array, table, and
  instrument datasets without embedding a file/network API.
- Acceptance: unit/schema/provenance mismatch fails before execution; adapters
  remain optional for core tests.

## E2 — Semantic IR

### LISS-0080 — Phase-resolved typed HIR

- Priority/size: P0 / XL
- Status: **Slice A Phase 1 Red** (2026-07-29)
- Depends on: LISS-0071 **complete**, LISS-0072 **complete**
  (**not** LISS-0070 — Rust deferred; Python Shipping Kernel first)
- Plan: [`qpex-v1-phase-resolved-hir-plan.md`](../specs/qpex-v1-phase-resolved-hir-plan.md)
- Issue: [`LISS-0080`](../issues/LISS-0080-phase-resolved-typed-hir.md)
- Action: implement resolved symbols, types, phases, effects, generics,
  interfaces, and source/desugaring provenance in immutable HIR via
  additive extraction from the shipping typechecker (no big-bang rewrite).
- Acceptance: all frontend diagnostics arise before Physics IR; HIR verifier
  detects invalid construction; Rust mirror remains LISS-0070 later.
- Unlocks: LISS-0075; LISS-0081 / LISS-0082

### LISS-0081 — Physics IR for equations and operator algebra

- Priority/size: P0 / XL
- Depends on: LISS-0073, LISS-0074, LISS-0080
- Action: represent Hilbert spaces, operators, equations, binders, units,
  statistics, symmetries, channels, and observables without gate expansion.
- Acceptance: Ising, Heisenberg, Hubbard, molecular electronic, oscillator, and
  Lindblad formulas preserve recognizable structure and source provenance.

### LISS-0082 — Quantum Semantic IR

- Priority/size: P0 / XL
- Depends on: LISS-0075, LISS-0081
- Action: represent finite pure/mixed transformations, unitary/channel regions,
  static/dynamic control, parameters, measurements, and ancilla lifetimes.
- Acceptance: simulator and QPU planning consume the same semantic contract;
  no target/provider types appear.

### LISS-0083 — Algorithm Plan IR and approximation ledger

- Priority/size: P0 / XL
- Depends on: LISS-0082, existing LISS-0033
- Action: type mappings, discretizations, evolution strategies, state
  preparation, measurement plans, error categories, and resource estimates.
- Acceptance: every approximate node identifies source, policy, bound/estimate,
  and resource impact; missing provenance is a hard verifier failure.

### LISS-0084 — General mixed states, channels, and POVMs

- Priority/size: P1 / XL
- Depends on: LISS-0081, LISS-0082, existing LISS-0011/LISS-0037
- Action: general acting-space density states, Kraus/Choi/superoperator
  boundaries, general effects, mixed-system partial trace, and channel
  composition.
- Acceptance: positivity/trace/completeness rules never silently repair input;
  pure/mixed measurement contracts agree.

### LISS-0085 — Continuous equations and numerical lowering

- Priority/size: P1 / XL
- Depends on: LISS-0081, LISS-0083, existing LISS-0036
- Action: equation declarations, domains, bases, boundary conditions,
  differentiation/integration IR, discretization, and explicit numerical
  solver plans.
- Acceptance: no continuous expression becomes finite without a contract;
  convergence/error provenance is reportable.

### LISS-0086 — General second-quantized mappings

- Priority/size: P1 / XL
- Depends on: LISS-0081, LISS-0083, existing LISS-0032
- Action: Bravyi-Kitaev/parity mappings, boson/spin mappings, normal ordering,
  exchange-law simplification, symmetry tapering, and external chemistry
  adapter boundary.
- Acceptance: mappings are explicit and numerically checked against small exact
  models; statistics/order provenance is preserved.

## E3 — Planning and optimization

### LISS-0087 — Verified pass manager

- Priority/size: P0 / L
- Depends on: LISS-0080–LISS-0083
- Action: immutable pass API, pre/post invariant verifiers, exact/approximate
  classification, deterministic configuration, and pass provenance.
- Acceptance: invalid pass output cannot reach a backend.

### LISS-0088 — Hamiltonian and algorithm planner

- Priority/size: P1 / XL
- Depends on: LISS-0083, LISS-0087
- Action: common planner contract for Suzuki orders, QDrift, Krylov,
  qubitization/LCU candidates, QFT variants, and state preparation.
- Acceptance: selection is policy-driven, alternatives/costs are recorded, and
  no runtime-adaptive choice appears without explicit semantics.

### LISS-0089 — Exact circuit synthesis and optimization

- Priority/size: P1 / XL
- Depends on: LISS-0082, LISS-0087
- Action: cancellation, rotation merge, commutation proofs, controlled/adjoint
  specialization, ancilla reuse, and unitary synthesis.
- Acceptance: differential simulation proves equivalence; source term order is
  changed only when legal under declared policy.

### LISS-0090 — Measurement grouping and shot allocation

- Priority/size: P1 / L
- Depends on: LISS-0083, LISS-0087
- Action: commuting-group planning, covariance-aware allocation, confidence
  targets, and raw/derived measurement provenance.
- Acceptance: user-declared observables and uncertainty targets remain
  reconstructable from results.

### LISS-0091 — Resource estimation and feasibility

- Priority/size: P1 / L
- Depends on: LISS-0083, LISS-0087
- Action: logical qubits/qudits, ancillas, depth, gates, measurements,
  classical-control latency, simulator memory, execution time, and cost
  estimates.
- Acceptance: estimates state assumptions and uncertainty; pre/post-routing
  estimates remain distinct.

### LISS-0092 — Layout, routing, native translation, and scheduling

- Priority/size: P1 / XL
- Depends on: LISS-0089, LISS-0091, LISS-0099
- Action: target pipeline stages, logical/physical mapping, SWAP insertion,
  native gates, timing, barriers, and post-routing validation.
- Acceptance: logical register provenance survives; no target constraint leaks
  back into Theory.

### LISS-0093 — Explicit error mitigation transforms

- Priority/size: P2 / XL
- Depends on: LISS-0090, LISS-0092, LISS-0103
- Action: readout mitigation, ZNE, PEC, symmetry verification, calibration
  dependencies, uncertainty, and sampling overhead.
- Acceptance: raw and mitigated results both remain available; method is not
  labelled semantics-preserving.

## E4 — Simulators and portable backends

### LISS-0094 — Simulator port and capability profiles

- Priority/size: P0 / L
- Depends on: LISS-0082, LISS-0083
- Action: define simulator plan/result ports, capability negotiation,
  observation plans, deterministic RNG, budgets, and rejection behavior.
- Acceptance: core tests use fake ports; engine limitations do not change
  source semantics.

### LISS-0095 — [要決定] Simulator engine adoption

- Priority/size: P1 / L
- Depends on: LISS-0094
- Decision: select initial exact state-vector, stabilizer, tensor-network,
  density/open-system engines and dependency boundaries.
- Required evidence: correctness POC, precision, platform support, license,
  vulnerability posture, performance envelope, diagnostics, and minimal
  real-file tests.

### LISS-0096 — Dynamic and mixed-state simulator execution

- Priority/size: P1 / XL
- Depends on: LISS-0077, LISS-0084, LISS-0094/0095
- Action: dynamic measurement/feed-forward, density/channel execution,
  trajectories, Lindblad plans, and conformance across equivalent cases.
- Acceptance: supplied seeds/outcomes are reproducible; unsupported
  combinations fail without fallback.

### LISS-0097 — OpenQASM 3.1 backend completion

- Priority/size: P0 / XL
- Depends on: LISS-0082, LISS-0083, LISS-0087
- Action: parameters, subroutines/inlining policy, dynamic regions, timing,
  measurement/results, annotations, capability manifest, and independent
  parser validation.
- Acceptance: no empty-program fallback; emitted version/subset is explicit;
  diagnostics map to source.

### LISS-0098 — [要決定] QIR profile and toolchain

- Priority/size: P1 / L
- Depends on: LISS-0082, LISS-0070
- Decision: QIR profile(s), LLVM version, runtime ABI, validator, packaging,
  and ownership boundary.
- Acceptance evidence: static and dynamic Bell/teleportation POCs, output
  metadata round-trip, platform/toolchain matrix, dependency review.

### LISS-0099 — Target capability profile and physical target port

- Priority/size: P0 / L
- Depends on: LISS-0082, existing LISS-0067
- Action: versioned native gates, connectivity, measurement/reset, dynamic
  latency, qudit support, timing, limits, calibration snapshot, and resource
  policy.
- Acceptance: stale/unknown capabilities are explicit; provider data is
  adapter-owned.

### LISS-0100 — [要決定] First live QPU provider adapter

- Priority/size: P2 / XL
- Depends on: LISS-0097 or LISS-0098, LISS-0099, LISS-0102
- Decision: provider, SDK/version, authentication, retry/session behavior,
  quotas/cost controls, and integration-test environment.
- Recommended selection criterion: best contract coverage and testability, not
  brand preference.

## E5 — Host workflow and tools

### LISS-0101 — Scientific input bundle and provenance schema

- Priority/size: P1 / L
- Depends on: LISS-0079
- Action: versioned immutable scalar/array/table input bundle, units, schema,
  hashes, capture time, validation, and adapters for initial text formats.
- Acceptance: same validated contract feeds simulator and QPU execution;
  credentials and paths are not persisted as scientific values.

### LISS-0102 — Job, Session, Batch, cancellation, and retry orchestration

- Priority/size: P1 / XL
- Depends on: existing LISS-0065/0066, LISS-0099
- Action: provider-neutral lifecycle, idempotency, attempts, cancellation,
  complete/partial result policy, session/batch semantics, and cost budgets.
- Acceptance: lifecycle state machine is deterministic; adapter failures map to
  stable Host results; Kernel code is unchanged.

### LISS-0103 — Result, uncertainty, and report model

- Priority/size: P1 / XL
- Depends on: LISS-0090, LISS-0101, LISS-0102
- Action: typed measurements/expectations, uncertainty, raw versus transformed
  results, input/lowering/target provenance, and export adapters.
- Acceptance: a published result can identify source, data, compiler, target,
  shots, mapping, mitigation, and attempts.

### LISS-0104 — Compiler, simulator, and hardware debugging

- Priority/size: P1 / L
- Depends on: LISS-0087, LISS-0094, LISS-0103
- Action: IR/pass inspection, non-collapsing simulator checkpoints, resource
  cost reports, hardware diagnostic-job contracts, and source-linked errors.
- Acceptance: no QPU artifact gains an unrequested measurement; checkpoint
  capability is explicit.

### LISS-0105 — LSP, formatter, notebook, and physicist authoring tools

- Priority/size: P2 / XL
- Depends on: LISS-0072, LISS-0080, LISS-0104
- Action: syntax/semantic highlighting, formula input, hover types/units,
  diagnostics, IR preview, migration, notebook kernel, and experiment result
  links.
- Acceptance: source semantics are compiler-owned; tools use stable APIs and
  do not implement an alternate parser.

## E6 — Validation and release

The following are release work packages rather than reserved LISS numbers; they
should receive IDs when their dependencies are close to completion.

### Capstone model suite

Models:

- Bell/GHZ/teleportation and dynamic correction;
- QFT/phase estimation;
- Ising, Heisenberg, and long-range spin systems;
- Hubbard and molecular electronic structure;
- harmonic oscillator and wavepacket discretization;
- Jaynes-Cummings and Lindblad dissipation;
- VQE/QAOA parameter workflow;
- error-correction syndrome round;
- qutrit/qudit protocol;
- real dataset to report.

Each capstone must label supported profiles:

```text
parse | typecheck | physics-ir | simulator | openqasm | qir | live-qpu
```

### Differential and numerical validation

- hand-derived small matrices;
- independent simulator comparison;
- property-based algebra and type tests;
- pass equivalence tests;
- cross-backend probability/expectation confidence tests;
- generated artifact validators;
- Python/Rust differential behavior.

### Performance and resource benchmark suite

- compile time and IR size by model;
- binder/operator scaling;
- state-vector/density/tensor engine envelopes;
- routing quality and pass reproducibility;
- QPU artifact depth/gate count;
- Host throughput and Job lifecycle behavior.

### v1 release gate

- normative spec, grammar, diagnostics, examples, and tools synchronized;
- migration tool tested against all v0.1 examples;
- no known silent fallback;
- stable package/version policy;
- at least one exact simulator profile;
- OpenQASM 3.1 and one QIR profile validated;
- one provider adapter exercised through ports;
- reproducible end-to-end scientific report.

## Dependency-critical path

```text
ADR 0106 review
  -> LISS-0068 normative rebaseline
  -> LISS-0071 conformance
  -> LISS-0072/0080 frontend and HIR (Python Shipping Kernel)
  -> LISS-0081/0082/0083 semantic IR stack
  -> LISS-0087 verified pass manager
  -> LISS-0094 simulator port + LISS-0097 OpenQASM
  -> LISS-0099 target profile
  -> LISS-0102 Host lifecycle
  -> first live adapter and release capstones

Deferred (next version):
  LISS-0070 Rust compiler infrastructure
```

Parallel tracks after LISS-0068:

- mathematical source: 0069 -> 0072 -> 0073;
- quantum safety: 0075 -> 0077;
- scientific domains: 0074 → 0112 (D=3 SV), 0084, 0085, 0086;
- real-world data: 0079 -> 0101 -> 0103.

## Current next issue

- Issue: **LISS-0080** (phase-resolved typed HIR)
- Path/phase: Feature Path — Slice A **Phase 1 Red**
- Depends on: LISS-0071 **complete**, LISS-0072 **complete** (not LISS-0070)
- Branch: `feature/liss-0080-slice-a-red`
- Reason: Plan merged PR #113; HIR DTO/API Red suite written; awaiting
  Red→Green.
- Required approval: Phase 1 Red assertions → Phase 2 Green.

## Verification for this plan

- all existing LISS/ADR references resolve;
- proposed IDs do not reuse an existing LISS;
- source/backend/provider boundaries agree with accepted ADRs unless the
  migration table explicitly marks a proposed supersession;
- Markdown and links are checked deterministically;
- no compiler source or test file changes in this Architecture Path task.
