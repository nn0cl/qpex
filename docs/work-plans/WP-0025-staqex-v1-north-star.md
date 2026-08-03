# WP-0025: Staqex v1 north-star language and compiler

## Status

Proposed Architecture Path work plan. No listed Issue has implementation
approval merely because it appears here.

## Goal

Evolve the shipping Staqex Kernel into the language described by ADR 0106:

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
- Revises: priority/delivery sequencing through
  [WP-0029](WP-0029-current-hardware-delivery-horizon.md)
- Revision reason: P0/P1 must retain current-machine execution evidence and
  2026–2031 planned-system readiness
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
8. P0/P1 capabilities retain bounded current-hardware witnesses; NH5 and
   QP-1/QP-2/QS-2 profiles remain non-normative stress loads.

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
- Shipping note: current Shipping Kernel remains Python (`compiler/staqex/`).
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
- Plan: [`staqex-v1-dirac-algebra-ast-plan.md`](../specs/staqex-v1-dirac-algebra-ast-plan.md)
- Action: parse Kets, Bras, matrix elements, projectors, adjoints, tensor
  products, commutators, and anticommutators into one typed algebra model.
- Acceptance: formula-to-AST mappings are unambiguous; domain mismatches and
  pipeline collisions are hard errors; no macro/string semantics.

### LISS-0074 — Qutrit, qudit, and finite local-dimension types

- Priority/size: P0 / L
- Status: **complete** (2026-07-29); D=3 SV → [LISS-0112](../architecture/documentation-compression-map.md) **complete**
- Depends on: LISS-0068, LISS-0071
- Plan: [`staqex-v1-qudit-local-dimension-plan.md`](../specs/staqex-v1-qudit-local-dimension-plan.md)
- Issue: [`LISS-0074`](../architecture/documentation-compression-map.md)
- Action: add `QutritRegister<N>` and `QuditRegister<D,N>`, basis-label
  checking, acting-space algebra, and target capability requirements.
- Acceptance: invalid Ket labels and incompatible local dimensions fail before
  lowering; no integer-array equivalence is exposed.

### LISS-0112 — Qutrit / qudit D=3 state-vector MVP

- Priority/size: P0 / L
- Status: **complete** (2026-07-29)
- Depends on: LISS-0074 **complete**
- Plan: [`staqex-v1-qudit-d3-sv-plan.md`](../specs/staqex-v1-qudit-d3-sv-plan.md)
- Issue: [`LISS-0112`](../architecture/documentation-compression-map.md)
- Action: real dim-3 Kernel SV for `State<Qutrit>` / `State<Qudit<3>>`; lift
  `UNSUPPORTED_LOCAL_DIMENSION` on measure + Identity evolve/apply(I) only.
- Acceptance: dim-3 measure and Identity paths; QASM / D≠3 remain fail-closed;
  no multi-site register SV or OpenQASM qudit opcodes in this Issue.

### LISS-0075 — Linear quantum usage and safe uncomputation

- Priority/size: P0 / XL
- Status: **complete** (2026-07-29) — Slices A–D on
  `feature/liss-0075-linear-quantum-usage`
- Depends on: LISS-0071 **complete**, [LISS-0080](../architecture/documentation-compression-map.md)
  **complete**
- Action: define ownership/borrowing or linear-use model, no-cloning,
  no-implicit-discard, ancilla lifetime, and proof-driven uncomputation.
- Acceptance (shipped MVP): `LINEAR_DUPLICATE_USE`, `LINEAR_IMPLICIT_DISCARD`,
  static `|0>`/`vacuum` Uncompute witness + `HirDecl.effects`; diagnostics on
  `HirModule.linear_diagnostics` via `build_hir`.
- Residuals: triaged to [LISS-0114](../architecture/documentation-compression-map.md)
  (pipeline hard-fail, control-flow, runtime witness). **Not** LISS-0077.

### LISS-0114 — Linear verifier hardening and residual risks

- Priority/size: P0 / L (sliced A–F)
- Status: **complete** — Slices A–F (2026-07-29); ADR 0107 **Accepted**
- Depends on: [LISS-0075](../architecture/documentation-compression-map.md) **complete**
- Action: dispose 0075 R1–R9 (R10 closed-accepted); pipeline hard-fail (R5);
  Gherkin rebaseline (R8); consume-set / alias / DensityState / control-flow /
  runtime uncompute slices.
- Acceptance (A–F shipped): hard-fail; consume-set; strict alias; DensityState
  carriers; nested `forEach` + `when`/`inspect`; runtime ≈|0⟩ witness +
  `LINEAR_UNCOMPUTE_AMPLITUDE_TOL`.
- Does **not** replace LISS-0077 (Dynamic QPU).
- Branch: `feature/liss-0114-slice-a` (merged PR #120)
- ADR: [0107](../architecture/adr/0107-linear-uncompute-amplitude-tolerance.md) **Accepted**

### LISS-0076 — Body-level scientific phase typing

- Priority/size: P0 / XL
- Status: **complete** — Slices A–E on `feature/liss-0076-slice-a` (2026-07-29)
- Depends on: LISS-0068 **complete**, [LISS-0034](../issues/LISS-0034-phase-separated-scientific-scopes.md)
  Phase 3 (body-level deferred here), LISS-0080 **complete**
- Issue: [LISS-0076](../architecture/documentation-compression-map.md)
- Action: enforce Theory/Experiment/Workflow/Execution/Report visibility inside
  expression bodies, imports, generic calls, and methods.
- Acceptance: phase leaks produce phase diagnostics rather than unresolved-name
  or generic type errors.
- Shipped: CU + Exp/Wf + import + call/method → `PHASE_TYPE_VISIBILITY_ERROR`;
  catalog + Gherkin closeout.

### [LISS-0077](../architecture/documentation-compression-map.md) — Dynamic QPU controller and feed-forward

- Priority/size: P0 / XL (P0 package L; E deferred)
- Status: **complete** (P0 package) — PR #168 (`84742bb`); `dynamic_qpu.py`;
  E deferred
- Depends on: LISS-0075/0076 **complete**; LISS-0082 **complete**; LISS-0094
  **complete**
- Plan: [dynamic-qpu plan](../specs/staqex-v1-dynamic-qpu-plan.md)
- Action: P0 integrated controller/feed-forward contract (lane/escape, match/
  merge, reset/reuse obligations, Fake supplied-outcome execution); defer
  portable dynamic artifact (E).
- Acceptance:
  - Static Kernel terminal-measure tests remain unchanged;
  - controller values cannot escape or control shape;
  - supported Fake SIM0 execution is deterministic under supplied outcomes;
  - unsupported capabilities fail explicitly.

### [LISS-0078](../issues/LISS-0078-function-interface-pipeline-effect-consolidation.md) — Function, interface, pipeline, and effect consolidation

- Priority/size: P1 / L
- Depends on: LISS-0068, LISS-0076
- Action: make function types, partial application, interface dispatch, effect
  propagation, and `return` one coherent typed model.
- Acceptance: wrappers and pipelines cannot hide effects; coherence and
  visibility diagnostics survive module linking.

### [LISS-0079](../issues/LISS-0079-typed-scientific-input-declarations.md) — Typed scientific input declarations

- Priority/size: P1 / L
- Depends on: LISS-0076, existing LISS-0045
- Action: define source declarations for Host-bound scalar, array, table, and
  instrument datasets without embedding a file/network API.
- Acceptance: unit/schema/provenance mismatch fails before execution; adapters
  remain optional for core tests.

## E2 — Semantic IR

### LISS-0080 — Phase-resolved typed HIR

- Priority/size: P0 / XL
- Status: **complete** (2026-07-29)
- Depends on: LISS-0071 **complete**, LISS-0072 **complete**
  (**not** LISS-0070 — Rust deferred; Python Shipping Kernel first)
- Plan: [`staqex-v1-phase-resolved-hir-plan.md`](../specs/staqex-v1-phase-resolved-hir-plan.md)
- Issue: [`LISS-0080`](../architecture/documentation-compression-map.md)
- Action: implement resolved symbols, types, phases, effects, generics,
  interfaces, and source/desugaring provenance in immutable HIR via
  additive extraction from the shipping typechecker (no big-bang rewrite).
- Acceptance: all frontend diagnostics arise before Physics IR; HIR verifier
  detects invalid construction; Rust mirror remains LISS-0070 later.
- Unlocks: LISS-0075; LISS-0081 / LISS-0082

### LISS-0081 — Physics IR for equations and operator algebra

- Priority/size: P0 / XL
- Status: **complete** — Adjudicator global closeout 2026-07-29
  (Slices A–D + E; follow-ups LISS-0115–0117 under WP-0028 **closed**).
- Depends on: LISS-0073, LISS-0074, LISS-0080
- Action: represent Hilbert spaces, operators, equations, binders, units,
  statistics, symmetries, channels, and observables without gate expansion.
- Acceptance: Ising, Heisenberg, Hubbard, molecular electronic, oscillator, and
  Lindblad formulas preserve recognizable structure and source provenance
  (fixture catalog + oscillator lowered-IR evidence; full public-oracle
  promotion deferred beyond this Issue).
- Follow-up IDs (**complete** under WP-0028): [LISS-0115](../architecture/documentation-compression-map.md)
  (HIR lowering + soft compile wire), [LISS-0116](../architecture/documentation-compression-map.md)
  (Equation/Unit DTO), [LISS-0117](../architecture/documentation-compression-map.md)
  (source-backed goldens / oscillator evidence). Do not reassign these IDs.
  Parallelism record: [WP-0028](../architecture/documentation-compression-map.md) **closed**.

### [LISS-0082](../architecture/documentation-compression-map.md) — Quantum Semantic IR

- Priority/size: P0 / XL
- Status: **complete** A–F; soft `CompileResult.quantum_semantic_ir` shipped
  (Slice F Red/Green/Refactor); ADR 0108–0111 **Accepted**
- Depends on: LISS-0075 **complete**, LISS-0081 **complete**
- Issue: [`LISS-0082`](../architecture/documentation-compression-map.md)
- Plan: [`staqex-v1-quantum-semantic-ir-plan.md`](../specs/staqex-v1-quantum-semantic-ir-plan.md)
- Detailed contract:
  [`quantum-semantic-ir-contract.md`](../architecture/quantum-semantic-ir-contract.md);
  [ADR 0108](../architecture/adr/0108-quantum-semantic-ir-value-region-contract.md)
  is **Accepted**.
- Scale/model envelope:
  [`quantum-machine-scale-and-model-envelope.md`](../architecture/quantum-machine-scale-and-model-envelope.md);
  [ADR 0109](../architecture/adr/0109-quantum-machine-scale-and-model-envelope.md)
  is **Accepted**.
- Optimistic capacity stress envelope:
  [`quantum-capacity-horizon-scenarios.md`](../architecture/quantum-capacity-horizon-scenarios.md);
  [ADR 0110](../architecture/adr/0110-optimistic-quantum-capacity-horizon.md)
  is **Accepted**.
- Current/NH5 delivery envelope:
  [`current-hardware-delivery-envelope.md`](../architecture/current-hardware-delivery-envelope.md);
  [ADR 0111](../architecture/adr/0111-current-hardware-first-delivery-horizon.md)
  and [WP-0029](WP-0029-current-hardware-delivery-horizon.md) are
  **Accepted** (profiles remain non-normative fixtures).
- Action: represent immutable whole-Joint-state generations over finite acting
  spaces; explicit unitary/isometry/channel/measurement signatures; coherent
  versus dynamic control lanes; parameters; linear/ancilla and approximation
  obligations on an additive Kernel module.
- Acceptance: simulator and QPU planning consume the same semantic contract;
  Static Kernel measurement remains terminal; no target/provider/realization
  types appear; structured regions do not require eager flattening; local and
  utility-scale deployment do not fork meaning; CH0/NH5/QP-2/QS-2 profiles
  remain downstream consumers of one module.
- Completion evidence: PR #145 (`docs: finalize LISS-0082 Slice E contract
  status`) merged into `main` as `322c59a`; integrated Slice E and
  cross-cutting Semantic IR tests passed.
- Out of scope (fixed at intake): numerical solving, gate expansion, JW
  execution, Algorithm Plan IR, Dynamic QPU behavior, general channel
  execution, existing QPU IR migration, soft compile wire (optional Slice F),
  Equation DTO extensions.

### [LISS-0083](../architecture/documentation-compression-map.md) — Algorithm Plan IR and approximation ledger

- Priority/size: P0 / XL
- Status: **complete** — integrated A–F scope merged through PR #146; CI passed
  2026-07-30
- Depends on: LISS-0082, existing LISS-0033
- Action: type mappings, discretizations, evolution strategies, state
  preparation, measurement plans, error categories, hierarchical callable
  plans, symbolic repetition/resource expressions, and resource estimates.
- Acceptance: every approximate node identifies source, policy, bound/estimate,
  and resource impact; missing provenance is a hard verifier failure; large
  plans remain structured until bounded target materialization; resource
  multiplicities are exact/symbolic beyond unsigned 64-bit range; one
  `SIM0_EXACT`/`CH0_COMMON_PHYSICAL` witness and NH5 compact plans exercise the
  same plan schema.
- Approval unit: internal dimensions A–F are not independent gates. Approvals
  are integrated Architecture + Red, Green, Refactor, and final PR/merge.

### LISS-0120 — Representative program language review gate

- Priority/size: P0 / XL
- Status: **rejected / deferred** (2026-07-31) — premature active gate
- Issue:
  [`LISS-0120`](../issues/LISS-0120-representative-program-language-review-gate.md)
- Rebaseline:
  [`staqex-v1-representative-program-rebaseline.md`](../specs/staqex-v1-representative-program-rebaseline.md)
- Depends on (before any successor showcase): example health (P0), honest
  language coverage ledger (P1), then mission lock (P2)
- Action (deferred): representative program under Physicist × DX harmony —
  research-grade physics reading and Clean Architecture / DDD discipline
  under one meaning — only after prerequisites; not a soft A11 continuation
  under this ID
- Acceptance (when successor opens): one ambitious mission spine; required
  coverage rows closed or explicitly out; green example baseline; findings →
  Issues/ADRs only
- Out until P1 says otherwise: pretending Open Topics are shipped; showcase
  on amber/red examples; provider SDKs / live QPU credentials

### [LISS-0084](../issues/LISS-0084-general-mixed-states-channels-povms.md) — General mixed states, channels, and POVMs

- Priority/size: P1 / XL
- Depends on: LISS-0081, LISS-0082, existing LISS-0011/LISS-0037
- Action: general acting-space density states, Kraus/Choi/superoperator
  boundaries, general effects, mixed-system partial trace, and channel
  composition.
- Acceptance: positivity/trace/completeness rules never silently repair input;
  pure/mixed measurement contracts agree.

### [LISS-0085](../issues/LISS-0085-continuous-equations-numerical-lowering.md) — Continuous equations and numerical lowering

- Priority/size: P1 / XL
- Depends on: LISS-0081, LISS-0083, existing LISS-0036
- Action: equation declarations, domains, bases, boundary conditions,
  differentiation/integration IR, discretization, and explicit numerical
  solver plans.
- Acceptance: no continuous expression becomes finite without a contract;
  convergence/error provenance is reportable.

### [LISS-0086](../issues/LISS-0086-general-second-quantized-mappings.md) — General second-quantized mappings

- Priority/size: P1 / XL
- Depends on: LISS-0081, LISS-0083, existing LISS-0032
- Action: Bravyi-Kitaev/parity mappings, boson/spin mappings, normal ordering,
  exchange-law simplification, symmetry tapering, and external chemistry
  adapter boundary.
- Acceptance: mappings are explicit and numerically checked against small exact
  models; statistics/order provenance is preserved.

## E3 — Planning and optimization

### [LISS-0087](../architecture/documentation-compression-map.md) — Verified pass manager

- Priority/size: P0 / L
- Status: **complete** — integrated A–E scope merged through PR #149; CI passed
  2026-07-30
- Depends on: LISS-0080–LISS-0083
- Action: immutable pass API, pre/post invariant verifiers, exact/approximate
  classification, deterministic configuration, and pass provenance.
- Acceptance: invalid pass output cannot reach a backend.
  Current CH0 plans and NH5 compact plans use the same immutable pass and
  invariant evidence contracts.
- Approval unit: internal dimensions A–E are not independent gates. Use one
  integrated Architecture + Red, Green, Refactor, and final PR/merge sequence.

### [LISS-0088](../architecture/documentation-compression-map.md) — Hamiltonian and algorithm planner

- Priority/size: P1 / XL
- Status: **complete** — integrated planner implementation and tests; merged
  through PR #152; CI workflow completed with no jobs; local verification
  passed
- Depends on: LISS-0083, LISS-0087
- Action: common planner contract for Suzuki orders, QDrift, Krylov,
  qubitization/LCU candidates, QFT variants, and state preparation.
- Acceptance: selection is policy-driven, alternatives/costs are recorded, and
  no runtime-adaptive choice appears without explicit semantics.

### [LISS-0089](../architecture/documentation-compression-map.md) — Exact circuit synthesis and optimization

- Priority/size: P1 / XL
- Status: **complete** — integrated exact optimization implementation and tests
  merged through PR #154; CI succeeded; local verification passed
- Depends on: LISS-0082, LISS-0087
- Action: cancellation, rotation merge, commutation proofs, controlled/adjoint
  specialization, ancilla reuse, and unitary synthesis.
- Acceptance: differential simulation proves equivalence; source term order is
  changed only when legal under declared policy.

### [LISS-0090](../architecture/documentation-compression-map.md) — Measurement grouping and shot allocation

- Priority/size: P1 / L
- Status: **complete** — integrated measurement planning merged through PR
  #155; CI and local verification passed
- Depends on: LISS-0083, LISS-0087
- Action: commuting-group planning, covariance-aware allocation, confidence
  targets, and raw/derived measurement provenance.
- Acceptance: user-declared observables and uncertainty targets remain
  reconstructable from results.
- Approval unit: former internal dimensions A–D are one integrated contract;
  use one Architecture/design + Red, Green, Refactor, and final PR/merge
  sequence completed through PR #155.

### [LISS-0091](../architecture/documentation-compression-map.md) — Resource estimation and feasibility

- Priority/size: P1 / L
- Status: **complete** — integrated resource estimation merged through PR
  #161 (`e1e93a9`)
- Depends on: LISS-0083 **complete**, LISS-0087 **complete**, LISS-0090
  **complete**
- Action: logical qubits/qudits, ancillas, depth, gates, measurements,
  classical-control latency, simulator memory, execution time, power/thermal,
  materialization size, decoder/link/factory loads, and cost estimates.
- Acceptance: semantic, logical, and physical resources remain distinct;
  estimates state assumptions and uncertainty; pre/post-routing estimates
  remain distinct; magnitudes beyond unsigned 64-bit range remain exact or
  symbolic, and failure budgets carry compositional assumptions.
- Approval unit: former internal dimensions A–E are one integrated contract;
  Architecture + Red, Green, Refactor, and final PR/merge sequence completed
  through PR #161. Host `SimulationResourceEstimate` (ADR 0100) stays
  separate.
- Plan: [`staqex-v1-resource-estimation-plan.md`](../specs/staqex-v1-resource-estimation-plan.md)
- Evidence: `compiler/staqex/resource_estimate.py`; Red suite
  `12 passed, 0 failed` after Refactor

### [LISS-0092](../architecture/documentation-compression-map.md) — Layout, routing, native translation, and scheduling

- Priority/size: P1 / XL
- Status: **complete** — integrated target routing merged through PR
  #163 (`afdbfa9`)
- Depends on: LISS-0089 **complete**, LISS-0091 **complete**; LISS-0099 live
  ports deferred (synthetic `TargetSnapshot` fixtures for this Issue)
- Action: target pipeline stages, logical/physical mapping, SWAP insertion,
  native gates, timing, barriers, and post-routing validation.
- Acceptance: logical register provenance survives; no target constraint leaks
  back into Theory.
- Approval unit: former internal dimensions A–E are one integrated contract;
  Architecture + Red, Green, Refactor, and final PR/merge sequence completed
  through PR #163.
- Plan: [`staqex-v1-target-routing-plan.md`](../specs/staqex-v1-target-routing-plan.md)
- Evidence: `compiler/staqex/target_routing.py`; Red suite
  `11 passed, 0 failed` after Refactor

### [LISS-0093](../issues/LISS-0093-explicit-error-mitigation.md) — Explicit error mitigation transforms

- Priority/size: **P1** / XL (promoted by proposed ADR 0111; bounded current
  slice first)
- Depends on: LISS-0090, LISS-0092, LISS-0103
- Action: readout mitigation, ZNE, PEC, symmetry verification, calibration
  dependencies, uncertainty, and sampling overhead.
- Acceptance: raw and mitigated results both remain available; method is not
  labelled semantics-preserving.

## E4 — Simulators and portable backends

### [LISS-0094](../architecture/documentation-compression-map.md) — Simulator port and capability profiles

- Priority/size: P0 / L
- Status: **complete** — PR #166 (`b6d2dda`); `simulator_port.py`
- Depends on: LISS-0082 **complete**, LISS-0083 **complete**
- Plan: [simulator-port plan](../specs/staqex-v1-simulator-port-plan.md)
- Action: define simulator plan/result ports, capability negotiation,
  observation plans, deterministic RNG, budgets, and rejection behavior as
  one integrated package (A–E internal review dimensions).
- Acceptance: core tests use fake ports; engine limitations do not change
  source semantics; `SIM0_EXACT` is the first portable oracle and rejects
  over-budget plans before allocation; `SIM1_MIXED` fixtures fail closed.

### [LISS-0095](../issues/LISS-0095-simulator-engine-adoption.md) — [要決定] Simulator engine adoption

- Priority/size: P1 / L
- Depends on: LISS-0094
- Decision: select initial exact state-vector, stabilizer, tensor-network,
  density/open-system engines and dependency boundaries.
- Required evidence: correctness POC, precision, platform support, license,
  vulnerability posture, performance envelope, diagnostics, and minimal
  real-file tests.

### [LISS-0096](../issues/LISS-0096-dynamic-mixed-simulator-execution.md) — Dynamic and mixed-state simulator execution

- Priority/size: P1 / XL
- Depends on: LISS-0077, LISS-0084, LISS-0094/0095
- Action: dynamic measurement/feed-forward, density/channel execution,
  trajectories, Lindblad plans, and conformance across equivalent cases.
- Acceptance: supplied seeds/outcomes are reproducible; unsupported
  combinations fail without fallback.

### [LISS-0097](../architecture/documentation-compression-map.md) — OpenQASM 3.1 backend completion

- Priority/size: P0 / XL (P0 package L; D/E/F deferred)
- Status: **complete** (P0 package) — PR #167 (`83b34e7`); `ch0_emit.py`;
  D/E/F deferred
- Depends on: LISS-0082/0083/0087 **complete**; LISS-0094 **complete**;
  LISS-0099 **complete**
- Plan: [openqasm-ch0 plan](../specs/staqex-v1-openqasm-ch0-plan.md)
- Action: P0 integrated static CH0 emit (manifest, parameters, measure/
  diagnostics, Fake independent parse); defer subroutine/dynamic/timing.
- Acceptance: no empty-program or simulator fallback; emitted version/subset
  explicit; diagnostics map to source; D/E/F remain fail-closed rejects.

### LISS-0098 — [要決定] QIR profile and toolchain

- Priority/size: **P2** / L (moved behind current OpenQASM path while Rust is
  deferred; proposed ADR 0111)
- Depends on: LISS-0082, LISS-0070
- Decision: QIR profile(s), LLVM version, runtime ABI, validator, packaging,
  and ownership boundary.
- Acceptance evidence: static and dynamic Bell/teleportation POCs, output
  metadata round-trip, platform/toolchain matrix, dependency review.

### [LISS-0099](../architecture/documentation-compression-map.md) — Target capability profile and physical target port

- Priority/size: P0 / L
- Status: **complete** — PR #165 (`ad89d15`); `target_capability.py`
- Depends on: LISS-0082 **complete**, LISS-0067 **complete**; LISS-0092
  **complete** (routing consumer)
- Action: versioned native gates, connectivity, measurement/reset, dynamic
  latency, qudit support, computation-model and deployment profiles,
  local/offline/network behavior, modular topology, logical/physical
  capacities, timing, power/thermal/memory limits, calibration snapshot, and
  resource policy.
- Acceptance: stale/unknown capabilities are explicit; provider data is
  adapter-owned; local, on-premises, remote, and facility targets reject
  unsupported semantics without implicit simulator or remote fallback;
  current CH0/CH1 and roadmap NH5 fixtures use the same versioned schema.
- Approval unit: former internal dimensions A–E are one integrated contract;
  Architecture + Red, Green, Refactor, and final PR/merge sequence completed
  on branch.
- Plan: [`staqex-v1-target-capability-plan.md`](../specs/staqex-v1-target-capability-plan.md)
- Evidence: `compiler/staqex/target_capability.py`; Red suite
  `10 passed, 0 failed` after Refactor

### [LISS-0100](../issues/LISS-0100-first-live-qpu-provider-adapter.md) — [要決定] First live QPU provider adapter

- Priority/size: **P1** / XL (promoted to current-hardware integration endcap
  by proposed ADR 0111)
- Depends on: LISS-0097 or LISS-0098, LISS-0099, LISS-0102
- Decision: provider, SDK/version, authentication, retry/session behavior,
  quotas/cost controls, and integration-test environment.
- Recommended selection criterion: best contract coverage and testability, not
  brand preference.

## E5 — Host workflow and tools

### [LISS-0101](../issues/LISS-0101-scientific-input-bundle-provenance.md) — Scientific input bundle and provenance schema

- Priority/size: P1 / L
- Depends on: LISS-0079
- Action: versioned immutable scalar/array/table input bundle, units, schema,
  hashes, capture time, validation, and adapters for initial text formats.
- Acceptance: same validated contract feeds simulator and QPU execution;
  credentials and paths are not persisted as scientific values.

### [LISS-0102](../issues/LISS-0102-job-session-batch-orchestration.md) — Job, Session, Batch, cancellation, and retry orchestration

- Priority/size: P1 / XL
- Depends on: existing LISS-0065/0066, LISS-0099
- Action: provider-neutral lifecycle, idempotency, attempts, cancellation,
  complete/partial result policy, session/batch semantics, local/on-premises/
  remote deployment decisions, explicit remote consent, and cost budgets.
- Acceptance: lifecycle state machine is deterministic; adapter failures map to
  stable Host results; local insufficiency never triggers implicit remote or
  simulator fallback; Kernel code is unchanged.

### [LISS-0103](../issues/LISS-0103-result-uncertainty-report-model.md) — Result, uncertainty, and report model

- Priority/size: P1 / XL
- Depends on: LISS-0090, LISS-0101, LISS-0102
- Action: typed measurements/expectations, uncertainty, raw versus transformed
  results, input/lowering/target provenance, and export adapters.
- Acceptance: a published result can identify source, data, compiler, target,
  shots, mapping, mitigation, and attempts.

### [LISS-0104](../issues/LISS-0104-compiler-simulator-hardware-debugging.md) — Compiler, simulator, and hardware debugging

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
- quantum safety: 0075 → **0114** (hardening) → 0077 (Dynamic QPU; still needs
  0076 + 0082);
- scientific domains: 0074 → 0112 (D=3 SV), 0084, 0085, 0086;
- real-world data: 0079 -> 0101 -> 0103.

## Current next issue

- Issue: **(next)** Showcase **S2** — full mission scale
- Path/phase: Feature Path; **awaiting Adjudicator authorize**
- Depends on: S1 + WP-0031 + LISS-0138 (language surface)
- Required approval: Authorize **S2** for a named Issue (**LISS-0188+**;
  historical note: this section once said LISS-0140+ before WP-0032+ numbering)

### Reserved follow-up IDs (do not reuse)

| ID | Topic | State |
|---|---|---|
| LISS-0128 | Open Topics before S1 program | **complete** |
| LISS-0129 | Typed surface annotations | **complete** |
| LISS-0130 | `evolve until` ledger reconcile | **complete** |
| LISS-0131 | ADR 0057 showcase boundary | **complete** |
| LISS-0132 | Open Topics permanent-out | **complete** |
| LISS-0133 | Expression residuals | **complete** |
| LISS-0134 | Showcase S1 thin slice | **complete** (#179) |
| LISS-0135 | QPU capability honesty | **complete** |
| LISS-0136 | Sparse Pauli Operator return | **complete** (#180) |
| LISS-0137 | Classical Float + param Operator factory | **complete** (PR pending) |
| LISS-0138 | `when` ket prepare arms | **complete** (PR pending) |
| LISS-0139 | Operator method Call return | **complete** (PR pending) |

Next free for **new** ad-hoc work: **LISS-0188+** (see
`docs/collaboration/local-issue-planning.md`). Historical reserved rows below
still must not be reused for unrelated topics; the old “LISS-0140+” pointer is
obsolete.

### Completed issues (reference)

- LISS-0081 (Physics IR equations / operator algebra): **complete** 2026-07-29
- LISS-0091 (Resource estimation and feasibility): **complete** 2026-07-31
- LISS-0094 (Simulator port and capability profiles): **complete** 2026-07-31, PR #166 (`b6d2dda`)
- LISS-0097 (OpenQASM static CH0 P0 package): **complete** 2026-07-31, PR #167 (`83b34e7`)
- LISS-0092 (Layout, routing, native translation, and scheduling): **complete**
  2026-07-31
- LISS-0099 (Target capability profile and physical target port): **complete**
  2026-07-31
- LISS-0115 (HIR→Physics IR lowering): **complete** 2026-07-29 A–D
- LISS-0116 (Equation / Unit DTO): **complete** 2026-07-29 A–C
- LISS-0117 (source-backed Physics IR goldens): **complete** 2026-07-29 A–C
- LISS-0076 (body-level scientific phase typing): **complete** 2026-07-29 A–E;
  residuals → LISS-0118
- LISS-0118 (0076 residuals: transitive taint / Report / short-name):
  **complete** 2026-07-29 A–C
- LISS-0075 (linear quantum usage): **complete** 2026-07-29; residuals → 0114
- LISS-0080 (phase-resolved typed HIR): **complete** 2026-07-29, PR #117
- LISS-0113 (QPex → Staqex rename): **complete** 2026-07-29, PR #118
- LISS-0114 (linear verifier hardening A–F): **complete** 2026-07-29

## Verification for this plan

- all existing LISS/ADR references resolve;
- proposed IDs do not reuse an existing LISS;
- source/backend/provider boundaries agree with accepted ADRs unless the
  migration table explicitly marks a proposed supersession;
- Markdown and links are checked deterministically;
- no compiler source or test file changes in this Architecture Path task.
