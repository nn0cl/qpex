# Staqex open-work register

This is the canonical cross-reference for capabilities that are intentionally
open, deferred, or still awaiting a dedicated local Issue. It complements the
completed Issue ledger; an item listed here is not implementation approval.

The shipping Kernel remains the Python package under `compiler/staqex/`. Any
future feature must first have an accepted specification or ADR, an explicit
phase request, and the required ports/adapters review described in
[`AGENTS.md`](../../AGENTS.md).

## Staqex v1 north-star rebaseline

| Area | Current status | Tracking | Boundary / acceptance note |
|---|---|---|---|
| Ideal v1 language and compiler | **Accepted with conditions** | [ADR 0106](decision-themes/dec-0003-language-surface-and-physicist-first-dx.md); [LISS-0068](documentation-compression-map.md); [WP-0025](../work-plans/WP-0025-staqex-v1-north-star.md); [rebaseline register](../specs/staqex-v1-normative-rebaseline-register.md) | North-star target architecture accepted 2026-07-27. LISS-0068 slice 2 may proceed; implementation remains per-Issue gated.

## Explicit deferred work

| Area | Current status | Tracking | Boundary / acceptance note |
|---|---|---|---|
| **QPex → Staqex rename** | **complete** | [LISS-0113](documentation-compression-map.md) | Renamed project from `QPex` to `Staqex`, `.sqx` → `.sqx`; 43 example files, ~136 Python import paths, ~340 doc files, agent instruction files; PR #118 merged 2026-07-29. |
|---|---|---|---|
| Function signatures / returns | Complete | [LISS-0021](documentation-compression-map.md); ADR 0064, ADR 0068 | Explicit return types, terminal `return`, `main -> Unit`, and arity/type checks are shipped and normative. QASM function-call lowering split to LISS-0049; an Operator-return typecheck gap split to LISS-0048. |
| Operator-return typecheck gap | Complete | [LISS-0048](documentation-compression-map.md) | Operator locals are registered before return checking; mismatches produce `RETURN_TYPE_MISMATCH` before runtime evaluation. Adjudicator final review approved 2026-07-25. |
| QASM function-call lowering | Complete (Option B scope) | [LISS-0049](documentation-compression-map.md) | Split from LISS-0021. Architecture Path selected Option B (2026-07-25): calling a user-defined `fn` from `main` rejects with `QASM_FUNCTION_CALL_UNSUPPORTED` (backend `reject_code` and CLI exit code) instead of silently falling back to the empty-program sketch. Adjudicator final review approved 2026-07-25. Option A (correct inlined output) remains a possible future follow-up, not scheduled. |
| Function keyword migration | Complete | [LISS-0023](documentation-compression-map.md); ADR 0066 | `fn` is canonical; `fun` is retired with no alias. |
| Visibility keyword migration | Complete | [LISS-0024](documentation-compression-map.md); ADR 0067 | `pub` is canonical; `public` is retired with no fallback. |
| Explicit returns / lexical scope | Complete | [LISS-0025](documentation-compression-map.md); ADR 0068 | Explicit terminal returns and no hidden Operator harvest. |
| Kernel classical boundary / static `forEach` | Historical slice complete; superseded surface tracked | [LISS-0026](documentation-compression-map.md); [ADR 0069](decision-themes/dec-0005-quantum-operations-and-runtime.md) | Static elaboration remains shipped; normative `QubitRegister<N>` migration/resource boundary is complete in LISS-0029. |
| Static Hilbert Kernel type surface | Phase 3 reviewed | [LISS-0029](documentation-compression-map.md); ADR 0069 | `QubitRegister<N>` is normative; MVP logical-shape/resource checks are explicit; target routing profiles remain separate. |
| Parametric Circuit | **Runtime complete** | [LISS-0027](../issues/LISS-0027-parametric-circuit.md); ADR 0070 | Symbolic parameters in QPU IR/OpenQASM; Host binding validation before submission. |
| Dynamic QPU lane | Phase 3 reviewed | [LISS-0028](../issues/LISS-0028-dynamic-qpu-lane.md); ADR 0071 | Rejection/capability boundary complete; mid-circuit semantics, timing, and JobResult composition remain open. |
| Real `qft` / `iqft` | Phase 3 reviewed; official example complete | [LISS-0010](documentation-compression-map.md); [LISS-0020](documentation-compression-map.md); [LISS-0042](../issues/LISS-0042-qft-basic-gate-lowering.md); [ADR 0078](decision-themes/dec-0005-quantum-operations-and-runtime.md) | Exact register-typed QFT/IQFT boundary and basic-gate lowering are complete; `examples/basics/B11_qft_registers/` is the canonical Basics path; integration capstone `examples/applied/A10_mission_observatory/`. Exact single-control `cqft`/`ciqft` shipped (ADR 0120 / LISS-0151); approximate QFT remains deferred. |
| Density matrix / Lindblad CPTP | Complete | [LISS-0011](documentation-compression-map.md); [ADR 0057](decision-themes/dec-0003-language-surface-and-physicist-first-dx.md) | Numeric/runtime/source slices are complete; symbolic Hamiltonian/jump operators now support any qubit count (dimension is derived from the actual `DensityState` source, not a hardcoded 1-qubit assumption). Adjudicator final review approved 2026-07-25. Adaptive integration, positivity projection, and QPU execution remain a possible future follow-up, not scheduled. |
| Explicit Lindblad jump inputs | Phase 3 reviewed | [LISS-0039](documentation-compression-map.md); [WP-0005](../work-plans/WP-0005-lindblad-jump-inputs.md) | `JumpSet([RawMatrix(...)])` lowers through the existing RK4 CPU lane; Channel reuse and symbolic jumps remain out of scope. |
| Symbolic Lindblad jump lowering | Phase 3 reviewed | [LISS-0040](documentation-compression-map.md); [WP-0018](../work-plans/WP-0018-symbolic-lindblad-jump-lowering.md) | Bound one-qubit `Operator` entries in `JumpSet` lower through the RK4 CPU lane; general operator algebra and QPU execution remain out of scope. |
| `evolve ... until` | **Runtime complete** | [LISS-0012](documentation-compression-map.md); [ADR 0079](decision-themes/dec-0005-quantum-operations-and-runtime.md) | Bounded pure repetition in the Joint evaluator; QPU emission remains unsupported. |
| Pipeline `|>` / currying | Phase 3 reviewed | [LISS-0013](../issues/LISS-0013-pipeline-currying.md); ADR 0080 / 0122–0123 / 0131 / 0133 / **0137** | Unary bare, Partial, stepwise, hole fill, and thin unary-fn Operator Fusion MVP shipped; ADR 0022 quartet MVPs shipped (0137–0140). |
| Trait `impl` / `system` expression model | Phase 3 reviewed | [LISS-0014](../issues/LISS-0014-trait-impl-system.md); [ADR 0082](decision-themes/dec-0005-quantum-operations-and-runtime.md) | Inline `<T: Interface>` bounds, post-merge coherence, marker `System`, and no `pub` in `impl` are shipped; dispatch and specialization remain deferred. |
| Effect marking | Phase 3 reviewed | [LISS-0015](../issues/LISS-0015-effect-marking.md); [ADR 0081](decision-themes/dec-0005-quantum-operations-and-runtime.md) | Fixed effect annotations and transitive call/pipeline diagnostics are shipped; effect rows and provider-specific effects remain deferred. |
| Host-side Braket / QPU submit | Phase 3 reviewed | [LISS-0016](../issues/LISS-0016-host-qpu-submit.md); [ADR 0083](decision-themes/dec-0006-host-qpu-and-external-ports.md) | Provider-neutral DTOs and submit/job ports are shipped; provider SDK, credentials, network adapter, and automatic retry remain deferred. |
| Job-based host execution/result boundary | Phase 3 complete | [LISS-0022](../issues/LISS-0022-job-based-host-execution.md); ADR 0065 | Local Job/JobResult boundary, linked-file APIs, CLI, and REPL integration are complete; provider submission, retries, and sessions remain deferred. |
| Operator-position bare `H` | Deferred | [LISS-0009](documentation-compression-map.md); ADR 0062 §7 | Existing `Hadamard` / explicit Operator forms remain authoritative until sugar receives a surface/typecheck specification. |
| Higher-order Suzuki / error control | **S2+S4 shipped** | [LISS-0017](../issues/LISS-0017-higher-order-suzuki.md); [LISS-0142](documentation-compression-map.md); [ADR 0084](decision-themes/dec-0006-host-qpu-and-external-ports.md) | S2 and S4 QASM lowering, static Bound/EmpiricalEstimate step derivation (order-aware), and `lowering_policy` provenance are shipped; adaptive selection remains deferred. |
| Concrete QPU IR lowering | Phase 3 reviewed | [LISS-0041](../issues/LISS-0041-qpu-ir-lowering.md); [ADR 0085](decision-themes/dec-0006-host-qpu-and-external-ports.md) | Immutable in-memory gate/parameter/measurement IR, provenance-preserving projection, and direct OpenQASM adapter input are shipped; dynamic opcodes and serialization remain deferred. |
| QFT/IQFT basic-gate lowering | Phase 3 reviewed | [LISS-0042](../issues/LISS-0042-qft-basic-gate-lowering.md); [ADR 0086](decision-themes/dec-0006-host-qpu-and-external-ports.md) | QFT/IQFT decompose controlled phase and register reversal into ADR 0085 basic gates; controlled/approximate QFT remains deferred. |
| Trotter step-count silent clamp | Complete | [LISS-0050](documentation-compression-map.md); [ADR 0094](decision-themes/dec-0005-quantum-operations-and-runtime.md) | QASM emission of a plain `evolve ... under H for t` (no `using Suzuki(...)` policy) rejects with `QASM_TROTTER_STEPS_REQUIRED` instead of silently clamping to 64 steps; the silently-clamped `trotter_step_count`/`trotter_gates` functions were removed. `using Suzuki(order = 2, steps/tolerance = ...)` (LISS-0017/ADR 0084) is the one remaining, already-correct mechanism. SV `evolve` (`expm_ih`) is unaffected. Adjudicator final review approved 2026-07-25. |
| Operator Pauli-atom-call parsing gap | Complete | [LISS-0051](documentation-compression-map.md) | Canonical bracketed references such as `Operator H = Z[0] * Z[1]` parse as `OpIndexed`/`OpBin`; genuine factory calls remain generic calls. The former parenthesized operator-index spelling is retired by LISS-0054. |

## Future theory-to-QPU coverage

The following proposed LISS are the next design inventory for writing common
theoretical-physics expressions without collapsing the Kernel/execution
boundary. Their complete dependency order and non-goals are recorded in
[`WP-0013`](../work-plans/WP-0013-theory-to-qpu-feature-roadmap.md) and the
research roadmap
[`theory-to-qpu-feature-roadmap.md`](../research/2026-07-23-theory-to-qpu-feature-roadmap.md).

| Area | Current status | Tracking | Boundary / acceptance note |
|---|---|---|---|
| Mathematical binders, finite domains, indexed expressions | Phase 3 reviewed | [LISS-0030](../issues/LISS-0030-mathematical-binders-and-indexed-expressions.md); [LISS-0055](../issues/LISS-0055-binder-body-as-operator-expression.md) | `sum`/`product` remain pure mathematical binders; the approved finite executable slice now lowers nested bodies, guards, products, and supported second-quantized expressions. Broader model-size acceptance remains open. |
| Finite mathematical binder lowering | Complete | [LISS-0052](documentation-compression-map.md); [LISS-0043](../issues/LISS-0043-finite-binder-lowering.md); [ADR 0088](decision-themes/dec-0002-state-first-semantics-and-measurement.md) | Inclusive finite sums retain inspection provenance and now also produce executable `OpExpr` trees consumed by the SV and QASM Hamiltonian paths. Literal indexed Pauli sites are supported wherever site-qualified Pauli operators are valid; Adjudicator completion approved 2026-07-27. |
| Binder composition and honest deferral | Phase 3 complete | [LISS-0053](documentation-compression-map.md); [LISS-0055](../issues/LISS-0055-binder-body-as-operator-expression.md); [ADR 0096](decision-themes/dec-0005-quantum-operations-and-runtime.md) | Composed finite sums and named scalar coefficients lower through existing execution paths. The LISS-0055 executable slice also handles supported `product`, nested binders, guards, and second-quantized bodies; unsupported forms remain explicit hard diagnostics. |
| Indexed operator and binder surface (final form) | LISS-0054…LISS-0058 complete; multi-register follow-up open | [ADR 0096](decision-themes/dec-0005-quantum-operations-and-runtime.md); [WP-0024](../work-plans/WP-0024-indexed-operator-and-binder-surface.md); [ADR 0102](decision-themes/dec-0002-state-first-semantics-and-measurement.md) | LISS-0054 ships one bracket notation `Op[i]`; LISS-0055 covers the approved executable binder slice; LISS-0056 defines empty-domain identities; LISS-0057 adds explicit periodic `wrap(i)`; LISS-0058 carries single-register acting space through operator values. Remaining empty-body/guard diagnostics and multi-register systems remain explicit follow-ups. |
| ADR deferred finite slices (honesty / `&&` / S4 / `J[i]`) | **complete** (WP-0032) | [WP-0032](documentation-compression-map.md); [LISS-0140](documentation-compression-map.md)–[LISS-0143](documentation-compression-map.md) | Binder honesty diagnostics; compound `where &&`; Suzuki S4; 1D `Float[N]` + `J[i]`. Still deferred: `rev`/dependent ranges, Basis expansion, Host tensors, cQFT. |
| ND Kernel coefficient tensors | **complete** (WP-0033) | [WP-0033](documentation-compression-map.md); [LISS-0144](documentation-compression-map.md); ADR 0096 | `Float[N][M]…` literals + full-rank `a[i][j]…` binder lookup. Host/Param tensors and partial slices remain deferred. |
| Binder endpoints / `where \|\|` / `rev` | **complete** (WP-0034) | [WP-0034](documentation-compression-map.md); [ADR 0117](decision-themes/dec-0002-state-first-semantics-and-measurement.md); LISS-0145–0147 | Static additive Index endpoints, dependent ranges, `rev(D)`, binder `\|\|`. |
| Basis binder / partial Float | **complete** (WP-0035) | [WP-0035](documentation-compression-map.md); [ADR 0118](decision-themes/dec-0004-type-first-scientific-model.md); LISS-0148–0149 | `Basis<N>` expansion; classical `Float[M…] row = h[i]`. |
| Host tensors + exact cqft | **complete** (WP-0036) | [WP-0036](documentation-compression-map.md); ADR 0119–0120; LISS-0150–0151 | In-memory `CoefficientTensor` + `host("…")`; exact `cqft`/`ciqft`. Approx QFT, file adapters, permanent-out remain out. |
| Acting-space typing | Phase 3 complete | [LISS-0058](documentation-compression-map.md); [ADR 0102](decision-themes/dec-0002-state-first-semantics-and-measurement.md); ADR 0096 D12 | Acting space is carried by operator values, with `QubitRegister<N>` as the canonical single-register shape and enclosing context as a secondary resolver. Declared shape is used during Hamiltonian evolution, context-free site-free identities fail explicitly, and no syntax-derived or one-qubit execution fallback is allowed. Multi-register naming and provider mapping remain deferred. |
| Multi-register acting-space and QPU mapping | Phase 3 reviewed | [LISS-0067](documentation-compression-map.md); [ADR 0105](decision-themes/dec-0006-host-qpu-and-external-ports.md) | Named static registers, RegisterSet typing, qualified-site checks, and logical/flat QPU mapping are reviewed complete; provider selection and physical routing remain gated. |
| Staqex v1 normative rebaseline | **closed — promoted** | [LISS-0068](documentation-compression-map.md), [spec v1.0](../specs/staqex-language-specification.md), [migration matrix](../specs/staqex-v1-migration-matrix.md) | Spec promotion 2026-07-28; next was LISS-0069. |
| Canonical Unicode math source | **closed — Slice A/B/C** | [LISS-0069](../issues/LISS-0069-canonical-mathematical-source-and-migration.md), [`cli.py` migrate](../../compiler/staqex/cli.py) | Dual-accept + library + CLI shipped 2026-07-28; NFC/A.1/M-P01/M-P05 separate. |
| Versioned conformance / differential oracle | **closed — Slice A/B/C** | [LISS-0071](documentation-compression-map.md), [scenario catalog](../specs/staqex-v1-conformance-scenario-catalog.md) | Completed 2026-07-28; E-07/13/14 deferred; Rust differential with LISS-0070. |
| Lossless CST / formatter / source versioning | **closed — Slice A/B/C/D** | [LISS-0072](documentation-compression-map.md), [CST/formatter plan](../specs/staqex-v1-cst-formatter-plan.md) | Completed 2026-07-28; NFC / full pretty-print / LSP remain separate; no Rust gate. |
| Named Dirac notation / algebra AST | **closed — A–G** | [LISS-0073](documentation-compression-map.md), [Dirac algebra AST plan](../specs/staqex-v1-dirac-algebra-ast-plan.md) | Completed 2026-07-29; formula→AST frozen; M-P06 dual-accept retained; formatter emit policy documented. |
| Qutrit / qudit / finite local dimension | **complete** | [LISS-0074](documentation-compression-map.md), [qudit plan](../specs/staqex-v1-qudit-local-dimension-plan.md) | A–E complete; SV deferred to LISS-0112. |
| Qutrit / qudit D=3 state-vector MVP | **complete** | [LISS-0112](documentation-compression-map.md), [D=3 SV plan](../specs/staqex-v1-qudit-d3-sv-plan.md) | A–C complete; measure + Identity; QASM/D≠3 reject; E06-003. |
| Phase-resolved typed HIR | **complete** | [LISS-0080](documentation-compression-map.md), [HIR plan](../specs/staqex-v1-phase-resolved-hir-plan.md) | A–D complete; unlocks LISS-0075. |
| Linear quantum usage and safe uncomputation | **complete** | [LISS-0075](documentation-compression-map.md) | A–D complete; residuals triaged to LISS-0114 (not LISS-0077). |
| Linear verifier hardening / residual risks | **complete** | [LISS-0114](documentation-compression-map.md), [ADR 0107](decision-themes/dec-0002-state-first-semantics-and-measurement.md) (**Accepted**) | A–F complete; runtime ≈\|0⟩ tol 1e-12 locked by ADR 0107. |
| Rust compiler infrastructure | **deferred — next version** | [LISS-0070](../issues/LISS-0070-rust-compiler-infrastructure-deferred.md) (WP-0025 north-star) | Shipping Kernel stays Python; Rust VM later behind same semantics. |
| Numeric representation horizon | proposed | [ADR 0097](decision-themes/dec-0004-type-first-scientific-model.md); ADR 0076 | `f64` stays the concrete Kernel representation but is recorded as provisional, not permanent. The coefficient type is deliberately **not** genericised now; instead the `f64` conversion boundary and rounding rules must be explicit so a future exact/symbolic layer is additive. |
| Operator algebra and Dirac notation | Phase 3 reviewed; Unicode sugar **closed via LISS-0073** | [LISS-0031](../issues/LISS-0031-operator-algebra-and-dirac-notation.md); [ADR 0087](decision-themes/dec-0002-state-first-semantics-and-measurement.md); [LISS-0073](documentation-compression-map.md) | Function-shaped typed algebra (LISS-0031) + punctuation surface (LISS-0073 A–G) shipped; M-P06 dual-accept retained. |
| Typed second quantization | Complete (Jordan-Wigner scope) | [LISS-0032](documentation-compression-map.md); [ADR 0093](decision-themes/dec-0005-quantum-operations-and-runtime.md) | Fermion/boson/spin/qubit family boundaries, statistics provenance, and explicit mapping metadata are shipped. Jordan-Wigner numerical mapping for `FermionOperator` (one-body and two-body terms) is shipped: a mapped Hamiltonian runs on the SV simulator and emits QASM. Adjudicator final review approved 2026-07-25. Bravyi-Kitaev, Boson, and Spin mappings, and exchange-law normalization beyond canonical ordering, remain a possible future follow-up, not scheduled. |
| Symbolic expression IR and provenance | Phase 3 reviewed | [LISS-0033](../issues/LISS-0033-symbolic-expression-ir-and-provenance.md) | Source-preserving Symbolic/Resolved IR inspection boundary is shipped; serialized interchange and executable lowering records remain deferred. |
| Phase-separated scientific scopes | Phase 3 reviewed | [LISS-0034](../issues/LISS-0034-phase-separated-scientific-scopes.md) | Sealed contracts complete; body-level → [LISS-0076](documentation-compression-map.md). |
| Body-level scientific phase typing | **complete** | [LISS-0076](documentation-compression-map.md), [scientific-scopes](../specs/staqex-scientific-scopes.md) | A–E complete 2026-07-29; Execution leaks → PHASE_TYPE_VISIBILITY_ERROR across CU, Exp/Wf, import, call/method. Residuals → [LISS-0118](documentation-compression-map.md) (**not** 0116). |
| Physics IR (equations / operator algebra) | **complete** | [LISS-0081](documentation-compression-map.md), [physics-ir plan](../specs/staqex-v1-physics-ir-plan.md) | A–D + E + follow-ups 0115–0117 (WP-0028 closed). Soft `CompileResult.physics_ir`; Equation DTOs; oscillator lowered-IR evidence. Full six-family public oracle deferred (0119+). PR #124 / #133. |
| Quantum Semantic IR | **complete** (A–F) | [LISS-0082](documentation-compression-map.md), [quantum-semantic-ir plan](../specs/staqex-v1-quantum-semantic-ir-plan.md), [detailed contract](quantum-semantic-ir-contract.md), [ADR 0108](decision-themes/dec-0006-host-qpu-and-external-ports.md) (**Accepted**) | Slices A–E merged (PR #145); Slice F soft `CompileResult.quantum_semantic_ir` merged (PR #160). |
| Resource estimation and feasibility | **complete** (PR #161) | [LISS-0091](documentation-compression-map.md), [resource-estimation plan](../specs/staqex-v1-resource-estimation-plan.md) | Integrated A–E; `compiler/staqex/resource_estimate.py`; Red `12/12`. Distinct from host `SimulationResourceEstimate` (ADR 0100). No provider prices/SDK. |
| Target layout / routing / schedule | **complete** (PR #163) | [LISS-0092](documentation-compression-map.md), [target-routing plan](../specs/staqex-v1-target-routing-plan.md) | Integrated A–E; `compiler/staqex/target_routing.py`; Red `11/11`. Synthetic `TargetSnapshot` fixtures; LISS-0099 live ports deferred. No provider SDK / Theory leakage. |
| Target capability profile / physical port | **complete** (PR #165) | [LISS-0099](documentation-compression-map.md), [target-capability plan](../specs/staqex-v1-target-capability-plan.md) | Integrated A–E; `compiler/staqex/target_capability.py`; Red `10/10`. Fake port + CH0/CH1/NH5 fixtures; projection to LISS-0092 snapshot. No provider SDK / Semantic leakage. |
| Simulator port / capability profiles | **complete** (PR #166) | [LISS-0094](documentation-compression-map.md), [simulator-port plan](../specs/staqex-v1-simulator-port-plan.md) | Integrated A–E; `compiler/staqex/simulator_port.py`; Red `11/11`. Fake `SIM0_EXACT`/`SIM1_MIXED`; no engine selection (LISS-0095). |
| OpenQASM static CH0 subset | **complete** (P0, PR #167) | [LISS-0097](documentation-compression-map.md), [openqasm-ch0 plan](../specs/staqex-v1-openqasm-ch0-plan.md) | P0 integrated A–C; `backend/qasm/ch0_emit.py`; Red `10/10`. D/E/F deferred. |
| Dynamic QPU controller / feed-forward | **complete** (P0) | [LISS-0077](documentation-compression-map.md), [dynamic-qpu plan](../specs/staqex-v1-dynamic-qpu-plan.md) | P0 integrated A–D; `dynamic_qpu.py`; Red `10/10`. Fake supplied-outcome exec. E deferred. |
| Quantum machine scale/model envelope | **Accepted** (ADR 0109) | [detailed envelope](quantum-machine-scale-and-model-envelope.md), [ADR 0109](decision-themes/dec-0006-host-qpu-and-external-ports.md), [research](../research/2026-07-30-quantum-machine-scale-and-model-horizon.md) | One semantics from Personal Quantum Appliance to utility-scale FTQC; hierarchical/symbolic plans; no implicit remote fallback. Not language maxima. |
| Optimistic quantum capacity horizon | **Accepted** (ADR 0110) | [scenario envelope](quantum-capacity-horizon-scenarios.md), [ADR 0110](decision-themes/dec-0006-host-qpu-and-external-ports.md) | Non-normative QP-1/QP-2/QS-2 stress loads from BQ-0; never delivery forecasts or language limits. |
| Current and five-year delivery horizon | **Accepted** (ADR 0111) | [delivery envelope](current-hardware-delivery-envelope.md), [ADR 0111](decision-themes/dec-0006-host-qpu-and-external-ports.md), [WP-0029](../work-plans/WP-0029-current-hardware-delivery-horizon.md), [research](../research/2026-07-30-current-quantum-hardware-delivery-envelope.md) | CH*/SIM* current profiles + NH5 roadmap stress; provider selection remains separate Technology approval. |
| Representative program language review | **rejected / deferred** (LISS-0120) | [LISS-0120](../issues/LISS-0120-representative-program-language-review-gate.md), [rebaseline](../specs/staqex-v1-representative-program-rebaseline.md) (**Accepted** 2026-07-31) | Premature gate closed. P0/P1 start authorized; LISS-0119 complete. |
| Examples health (rebaseline Gate P0) | **complete** (0119/0122/0123) | [LISS-0119](documentation-compression-map.md), [LISS-0122](documentation-compression-map.md), [LISS-0123](documentation-compression-map.md) | Basics+applied catalogs green; A11 on SV-09. |
| Language coverage ledger (Gate P1) | **complete** | [LISS-0124](documentation-compression-map.md), [ledger](../specs/staqex-v1-language-coverage-ledger.md) | Option B complete; typed surface shipped; permanent-out recorded; S1 authorize unblocked. |
| Showcase mission lock (Gate P2) | **complete** | [LISS-0126](documentation-compression-map.md), [mission lock](../specs/staqex-v1-showcase-mission-lock.md) | Quantum-matter / Noether Forge lineage locked 2026-07-31. |
| Showcase S0 specification | **complete** (docs) | [LISS-0127](documentation-compression-map.md), [S0 spec](../specs/staqex-v1-showcase-s0-specification.md) | Docs only; S1 authorized and shipped as LISS-0134. |
| Showcase S1 thin slice | **complete** | [LISS-0134](../issues/LISS-0134-showcase-s1-thin-slice.md), `examples/showcase/quantum_matter_discovery/` | Merged #179. |
| Sparse Pauli Operator return | **complete** | [LISS-0136](../issues/LISS-0136-sparse-pauli-operator-return.md) | Merged #180; factory local Float fold. |
| Classical Float → Operator / evolve + param factory | **complete** (PR pending) | [LISS-0137](../issues/LISS-0137-classical-float-operator-evolve-binding.md) | \(H(J,h)\); field/`evolve for` binding. |
| Operator method Call return | **complete** (PR pending) | [LISS-0139](../issues/LISS-0139-operator-method-call-return.md) | `Operator H = m.hamiltonian()`. |
| `when` ket prepare arms | **complete** (PR pending) | [LISS-0138](../issues/LISS-0138-when-ket-prepare-arms.md) | Ket arms in `when`; B02 + showcase updated. |
| Hamiltonian library surface program | **complete** (PR pending) | [WP-0031](../work-plans/WP-0031-hamiltonian-library-surface.md), [plan](../specs/staqex-v1-hamiltonian-library-surface-plan.md) | 0137+0139+showcase. |
| Open Topics before S1 (Option B) | **complete** | [LISS-0128](documentation-compression-map.md), [WP-0030](documentation-compression-map.md) | 0129–0133 + 0135 done; S1 shipped. |
| Open Topics permanent-out | **reopened** | [LISS-0152](documentation-compression-map.md), [note](../specs/staqex-v1-open-topics-permanent-out.md), [WP-0037](documentation-compression-map.md) | Pre-S1 out lifted 2026-07-31. Thin ships: ADR 0121–0122 / LISS-0153–0154. Follow-on WP-0038. |
| Permanent-out thin Kernel slices | **complete** (WP-0037) | ADR 0121–0122; LISS-0152–0154 | `Current`/`Temperature` dims; unary bare `\|\> f`. |
| Partial holes + SI `to` + design ADRs | **complete** (WP-0038) | [WP-0038](documentation-compression-map.md); ADR 0123–0128; LISS-0155–0160 | Ship Partial `_` + `expr to unit`; design boundaries for rational/PDF/live QPU/trait. |
| SI catalog wave-2 + KetLit fn args | **complete** (WP-0039) | [WP-0039](documentation-compression-map.md); ADR 0129–0130; LISS-0161–0162 | `ps`/`us`/`km`/`kHz`/`MHz` scales; user-fn KetLit Call args. |
| Stepwise Partial + eV↔J | **complete** (WP-0040) | [WP-0040](documentation-compression-map.md); ADR 0131–0132; LISS-0163–0164 | Left-to-right Partial fill; exact SI `eV`↔`J`. |
| Pipe hole fill + °C↔K | **complete** (WP-0041) | [WP-0041](documentation-compression-map.md); ADR 0133–0134; LISS-0165–0166 | Pipe fills leftmost `_`; affine Celsius↔Kelvin. |
| Fahrenheit + gram scale | **complete** (WP-0042) | [WP-0042](documentation-compression-map.md); ADR 0135–0136; LISS-0167–0168 | Affine °F↔K/C; `g`↔`kg`. |
| Pipeline Operator Fusion MVP | **complete** (WP-0043) | [WP-0043](documentation-compression-map.md); ADR 0137; LISS-0169 | Hold partial unseal; pure unary `fn` pipe chains fuse to one Joint pass. |
| Trace-Out GC fn-scope MVP | **complete** (WP-0044) | [WP-0044](documentation-compression-map.md); ADR 0138; LISS-0170 | Drop dead fn-local Joint axes after library `fn` Calls. |
| Interference prune MVP | **complete** (WP-0045) | [WP-0045](documentation-compression-map.md); ADR 0139; LISS-0171 | Amp-sum support merge + exact-zero prune via `Joint.merge_support`. |
| Deferred Pushforward MVP | **complete** (WP-0046) | [WP-0046](documentation-compression-map.md); ADR 0140; LISS-0172 | Eligible mains batch StateBind materialization at `measure`. |
| Algebraic Operator Fusion MVP | **complete** (WP-0047) | [WP-0047](documentation-compression-map.md); ADR 0141; LISS-0173 | Affine `scale·x+bias` collapse on unary pipe Fusion. |
| Evolve Trace-Out GC MVP | **complete** (WP-0048) | [WP-0048](documentation-compression-map.md); ADR 0142; LISS-0174 | Drop block-evolve `let` temps after exit. |
| Call/Partial pipe Fusion MVP | **complete** (WP-0049) | [WP-0049](documentation-compression-map.md); ADR 0143; LISS-0175 | One-hole Call/Partial stages in pipe Fusion. |
| Rankine affine | **complete** (WP-0050) | [WP-0050](documentation-compression-map.md); ADR 0144; LISS-0176 | `.R` ↔ K/F/C via Kelvin affine. |
| Imperial pound mass | **complete** (WP-0051) | [WP-0051](documentation-compression-map.md); ADR 0145; LISS-0177 | `.lb` ↔ kg/g (exact 0.45359237 kg). |
| Imperial ounce mass | **complete** (WP-0052) | [WP-0052](documentation-compression-map.md); ADR 0146; LISS-0178 | `.oz` ↔ lb/kg (16 oz = 1 lb). |
| Imperial stone mass | **complete** (WP-0053) | [WP-0053](documentation-compression-map.md); ADR 0147; LISS-0179 | `.st` ↔ lb/oz/kg (14 lb = 1 st). |
| Metric tonne mass | **complete** (WP-0054) | [WP-0054](documentation-compression-map.md); ADR 0148; LISS-0180 | `.t` ↔ kg (10³ kg). |
| Multi-hole Partial pipe fill | **complete** (WP-0055) | [WP-0055](documentation-compression-map.md); ADR 0149; LISS-0181 | Bare `|>` fills leftmost Partial hole; mid result may stay Partial. (Tuple simultaneous fill: ADR 0152.) |
| US/UK ton mass | **complete** (WP-0056) | [WP-0056](documentation-compression-map.md); ADR 0150; LISS-0182 | `.ton_us` = 2000 lb; `.ton_uk` = 2240 lb; share kg with `.t`. |
| Troy ounce mass | **complete** (WP-0057) | [WP-0057](documentation-compression-map.md); ADR 0151; LISS-0183 | `.oz_t` = 31.1034768 g; distinct from avoirdupois `.oz`. |
| Tuple multi-hole Fusion fill | **complete** (WP-0058) | [WP-0058](documentation-compression-map.md); ADR 0152; LISS-0184 | `(a,b) |> f(_, _)` fills all holes; Fusion peels tuple head. |
| Bare-block Trace-Out GC | **complete** (WP-0059) | [WP-0059](documentation-compression-map.md); ADR 0153; LISS-0185 | `{ let …; e }` BlockExpr; drop dead let axes. |
| Mixed-unit arithmetic reject | **superseded** (WP-0060) | ADR 0154 → [0155](decision-themes/dec-0004-type-first-scientific-model.md) | Reject-only policy withdrawn for shared-canonical families. |
| Mixed-unit canonical promote | **complete** (WP-0061) | [WP-0061](documentation-compression-map.md); ADR 0155; LISS-0187 | Mixed known units → canonical then `+`/`-`. |
| ADR 0057 showcase boundary | **complete** | [LISS-0131](documentation-compression-map.md) | Boundary doc only. |
| QPU capability honesty | **complete** | [LISS-0135](documentation-compression-map.md), [catalog](../specs/staqex-v1-qpu-capability-honesty.md) | Writable ≠ QPU-executable table. |
| Typed surface annotations | **complete** | [LISS-0129](documentation-compression-map.md), ADR 0115 | `state x: State<T> = …` shipped. |
| Expression residuals | **complete** | [LISS-0133](documentation-compression-map.md), ADR 0116 | LINEAR return, Float return, MULTI FP, Classical⊕State. |
| Physicist source friction ledger | **working** | [friction ledger](physicist-source-friction-ledger.md) | F-02/F-05 closed (ADR 0114 + LISS-0121); residual sample debt feeds P0; ledger seeds P1. Not an ADR. |
| Adjudicator language vision | **Accepted** (2026-07-31) | [vision](adjudicator-language-vision.md) | Physicist-first; ideal form first; §2.1 writeable≠executable; §3.1 Outer/Kernel/lanes; §6 Stop narrowed; §6.1 friction ops. Wired into agent contracts + spec §1.1. |
| HIR BinOp expr children | **complete** (LISS-0125) | [LISS-0125](documentation-compression-map.md), [suite](../../tests/test_liss_0125_hir_binop_expr_children_red.py) | `BinOp.lhs/rhs` walk; unblocks B03/A01 compile crash. |

| HIR → Physics IR lowering | **complete** (A–D) | [LISS-0115](documentation-compression-map.md) | `physics_ir_lower.py` + soft `CompileResult.physics_ir`; equations still explicit. **Do not reuse ID.** |
| Equation / Unit DTO | **complete** (Agent A A–C) | [LISS-0116](documentation-compression-map.md) | `physics_equation.py` shipped; not re-exported into frozen `physics_ir.py`. **Do not reuse ID.** |
| Source-backed Physics IR goldens | **complete** (Agent C A–C) | [LISS-0117](documentation-compression-map.md) | Loader + oscillator lowered-IR evidence; full six-family public oracle deferred. **Do not reuse ID.** |
| Body-level phase typing residuals | **complete** | [LISS-0118](documentation-compression-map.md) | A–C complete 2026-07-29: transitive taint, Report matrix, short-name fail-closed + catalog closeout. |
| Hybrid scientific workflow | Phase 4 reviewed | [LISS-0035](../issues/LISS-0035-hybrid-scientific-workflow.md), [ADR 0072](decision-themes/dec-0006-host-qpu-and-external-ports.md), [ADR 0073](decision-themes/dec-0006-host-qpu-and-external-ports.md) | Immutable provider-neutral Workflow/Job DTO boundary; declarative surface and named Host update callback, no provider SDK. |
| Continuous operators and discretization | Phase 3 reviewed | [LISS-0036](../issues/LISS-0036-continuous-operator-and-discretization-boundary.md), [ADR 0074](decision-themes/dec-0004-type-first-scientific-model.md), [LISS-0111](../issues/LISS-0111-continuous-discretization-numerical-lowering-mvp.md) | No hidden discretization; explicit contract and Theory-to-Kernel Bridge. MVP numerical lowering (`Position` + `UniformGrid` + periodic FD order 2) ships via `grid_hamiltonians` and Joint evolve. |
| POVM, measurement, and channel contracts | Phase 3 reviewed | [LISS-0037](documentation-compression-map.md); [ADR 0075](decision-themes/dec-0002-state-first-semantics-and-measurement.md); [WP-0014](../work-plans/WP-0014-povm-measurement-contract.md) | Terminal computational-basis measurement works for pure/mixed one-qubit states; general effects and dynamic measurement remain out of scope. |
| Semantic discrete carriers and phase-local types | Phase 3 reviewed | [LISS-0038](../issues/LISS-0038-semantic-discrete-carriers.md) | Separate dimensions, indices, counts, basis labels, and physical discrete values before indexed syntax; indexed syntax remains LISS-0030. |
| Numerical representation and continuous PDFs | Phase 3 reviewed | [LISS-0018](documentation-compression-map.md); [ADR 0076](decision-themes/dec-0004-type-first-scientific-model.md); [WP-0015](../work-plans/WP-0015-numeric-representation-policy.md) | Shared dependency-free f64/complex-f64 policy and non-repair validation are shipped; continuous PDFs and exact arithmetic remain deferred. |
| Observation checkpoints and execution diagnostics | Phase 3 reviewed | [LISS-0044](../issues/LISS-0044-observation-checkpoints-and-execution-diagnostics.md); [ADR 0089](decision-themes/dec-0002-state-first-semantics-and-measurement.md); [WP-0021](../work-plans/WP-0021-observation-checkpoints-and-execution-diagnostics.md) | Dependency-free Host observation requests/reports, simulator-only snapshot capability, no hidden measurement, explicit resource cost, and readability review are complete; execution adapters remain deferred. |
| Scientific input and parameter binding | Phase 3 complete | [LISS-0045](documentation-compression-map.md); [ADR 0090](decision-themes/dec-0004-type-first-scientific-model.md); [WP-0020](../work-plans/WP-0020-scientific-input-and-parameter-binding.md) | Dependency-free scalar Host input, `Param<T>` bindings, immutable sweeps, provenance validation, and readability refactor are complete; result-envelope integration and provider SDKs remain deferred. |
| JobResult observation integration | Phase 3 reviewed | [LISS-0046](../issues/LISS-0046-jobresult-observation-integration.md); [ADR 0091](decision-themes/dec-0006-host-qpu-and-external-ports.md); [WP-0022](../work-plans/WP-0022-jobresult-observation-integration.md) | Additive immutable `JobResult.observations` preserves existing positional construction and measurement separation; provider adapters, partial-result policy, and WorkflowReport composition remain deferred. |
| Local observation plan execution | Phase 3 reviewed | [LISS-0047](../issues/LISS-0047-local-observation-plan-execution.md); [ADR 0092](decision-themes/dec-0006-host-qpu-and-external-ports.md); [WP-0023](../work-plans/WP-0023-local-observation-plan-execution.md) | Dependency-free local adapter, deterministic fake source, portable reports, cost-only separate jobs, and hard unsupported-projection diagnostics are reviewed complete; provider/QPU execution remains deferred. |
| Resource profile manifest and simulator budget | Phase 3 reviewed; local execution wiring complete | [LISS-0062](documentation-compression-map.md); [LISS-0063](../issues/LISS-0063-simulator-resource-enforcement.md); [LISS-0064](../issues/LISS-0064-simulator-resource-execution-wiring.md); [ADR 0100](decision-themes/dec-0005-quantum-operations-and-runtime.md) | Host-side manifest/estimate boundary, provider-neutral Warn/Abort decision, and local run/QASM enforcement are complete. Provider submission and benchmark calibration remain deferred. |
| Host QPU submit orchestration | Phase 3 Refactor complete | [LISS-0065](documentation-compression-map.md); [LISS-0016](../issues/LISS-0016-host-qpu-submit.md); [ADR 0083](decision-themes/dec-0006-host-qpu-and-external-ports.md); [ADR 0103](decision-themes/dec-0006-host-qpu-and-external-ports.md) | Dedicated Host use case, explicit JobRequest/QpuArtifact mapping, fixed lifecycle, no partial measurements, explicit retry attempts, and provider-neutral orchestration are implemented and refactored. Provider SDK, credentials, network, and technology selection remain out of scope. |
| QPU observation/result integration | Phase 3 Refactor complete | [LISS-0066](documentation-compression-map.md); [ADR 0104](decision-themes/dec-0006-host-qpu-and-external-ports.md) | Host projector maps structured QPU payloads into ordered immutable JobResult observations, fails closed on incomplete results, preserves attempt metadata, and keeps separate jobs metadata-only; live provider integration remains deferred. |
| Numeric literal separators | Phase 3 Refactor complete | [LISS-0061](documentation-compression-map.md); [ADR 0101](decision-themes/dec-0004-type-first-scientific-model.md) | Java-compatible placement between digits is implemented; leading-underscore private identifiers remain unchanged; formatter and QPU provenance remain deferred. |

## Related open evaluations

These are broader research or technology questions already listed in the
architecture overview and remain unassigned unless a row above or a future
Issue gives them a concrete scope:

- Broader SI / atomic mass / bare `.ton` (WP-0062 / ADR 0156 when merged);
  **display-unit restore shipped**
  [ADR 0186](decision-themes/dec-0004-type-first-scientific-model.md) /
  [LISS-0314](documentation-compression-map.md)
  (LISS-0197 superseded);
  continuous PDF Kernel values (ADR 0126 boundary) — strategy
  [ADR 0162](decision-themes/dec-0006-host-qpu-and-external-ports.md); Host inject MVP
  [ADR 0163](decision-themes/dec-0006-host-qpu-and-external-ports.md) /
  [LISS-0195](documentation-compression-map.md) (**complete**);
  Host seam [ADR 0164](decision-themes/dec-0006-host-qpu-and-external-ports.md) /
  [LISS-0198](documentation-compression-map.md) /
  [WP-0068](documentation-compression-map.md) (**complete**);
  **finiteize surface shipped** [ADR 0185](decision-themes/dec-0004-type-first-scientific-model.md)
  Lane A / [LISS-0313](documentation-compression-map.md) **complete**
  (`finiteize` + B18); mid-program Continuous still deferred — **expressiveness
  seats** [scenarios](../specs/staqex-v1-continuous-lane-b-expressiveness-scenarios.md)
  / [LISS-0315](documentation-compression-map.md);
  **CH-field-compose baseline frozen weak** (Ideal §2A + Host 0317 + H→E 0318;
  [LISS-0319](documentation-compression-map.md));
  Joint rational mode still ADR 0125 (classical path: ADR 0160 shipped);
  numeric literal lifting: [LISS-0018](documentation-compression-map.md).
- Concrete live QPU provider **SDK** after honesty ports (ADR 0127);
  CredentialPort shipped ADR 0161: [LISS-0019](documentation-compression-map.md),
  [ADR 0077](decision-themes/dec-0006-host-qpu-and-external-ports.md).
- Trait specialization / effect-row surface examples (ADR 0128):
  [LISS-0196](documentation-compression-map.md) —
  **complete** (Adjudicator 採択 2026-08-03: examples accepted, **no ship ADR**)
  ([examples](../specs/staqex-v1-trait-effect-surface-examples.md)); no Kernel Red
  until a future ship ADR is Accepted separately.
- Whether numeric literals are sugar for `dirac`.
- **Kernel External Resources ports (ADR 0166) — shipped:**
  `RngPort` (WP-0082 / LISS-0235 / ADR 0170),
  `MeasureSinkPort` (WP-0083 / LISS-0236 / ADR 0171),
  `SourcePort` (WP-0084 / LISS-0237 / ADR 0172; below `load_module_graph`).
  Design [ADR 0166](decision-themes/dec-0006-host-qpu-and-external-ports.md) (**Accepted**) /
  [LISS-0218](documentation-compression-map.md) (**complete** — design).
  Binding constraint: seeded outputs must stay bit-identical.
- Dirac paper spelling `⟨φ|ψ⟩` as sugar over `inner`/`outer` (**shipped**
  WP-0081 / LISS-0234 / ADR 0169; ledger F-04):
  [ADR 0165](decision-themes/dec-0003-language-surface-and-physicist-first-dx.md) (**Accepted**) /
  [LISS-0217](documentation-compression-map.md) (**complete** — design).
- `inspect` vs measure teaching risk and circuit-vs-Hamiltonian lane choice
  (friction ledger F-06 / F-10, Class B, no ADR yet):
  [LISS-0219](documentation-compression-map.md) (**complete** — docs guidance).
- **Not open — decided:** user-defined operator overloading is out of scope per
  [ADR 0114 §D5](decision-themes/dec-0002-state-first-semantics-and-measurement.md).
  Friction ledger F-08 cites that decision
  ([LISS-0215](documentation-compression-map.md)
  **complete**).
- **Quantum mental-model follow-up:** design is open under
  [WP-0092](../work-plans/WP-0092-quantum-mental-model-follow-up.md), following
  accepted [ADR 0189](adr/0189-quantum-mental-model-and-observation-contract.md).
  Specification approval and Phase 1 approval are still required before
  grammar, conformance tests, or implementation changes.
- Living backlog: WP-0062–0068 shipped; next free WP-0069+ / LISS-0199+.

## Repository health (2026-08-02)

Root suites and spec-verification are green locally and gated in CI:

- Blocking `kernel-tests`: `python3 -m pytest tests/ -q` (WP-0080 / LISS-0209).
- Blocking `spec-verification`: `python3 tests/spec_verification/run_all.py`
  (WP-0086 / LISS-0241).
- Floor observed 2026-08-02: **1084+** pytest passed; SV gate **161/161**.

Historical note: the 2026-08-01 operations review recorded ~50 root failures and
no CI tests ([WP-0069](../work-plans/WP-0069-operations-review-intake.md)); that
floor was closed by WP-0079–0080 and WP-0086.

## Status rule

`Open` means the design question is known but not accepted for implementation.
`Deferred` means the current Kernel deliberately stops before that boundary.
`Done` on a related Issue does not close a later follow-on listed here; for
example, first-order Trotter is done while higher-order Suzuki remains
deferred.
