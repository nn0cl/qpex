# QPex open-work register

This is the canonical cross-reference for capabilities that are intentionally
open, deferred, or still awaiting a dedicated local Issue. It complements the
completed Issue ledger; an item listed here is not implementation approval.

The shipping Kernel remains the Python package under `compiler/qpex/`. Any
future feature must first have an accepted specification or ADR, an explicit
phase request, and the required ports/adapters review described in
[`AGENTS.md`](../../AGENTS.md).

## Explicit deferred work

| Area | Current status | Tracking | Boundary / acceptance note |
|---|---|---|---|
| Function signatures / returns | Complete | [LISS-0021](../issues/LISS-0021-function-signatures-and-returns.md); ADR 0064, ADR 0068 | Explicit return types, terminal `return`, `main -> Unit`, and arity/type checks are shipped and normative. QASM function-call lowering split to LISS-0049; an Operator-return typecheck gap split to LISS-0048. |
| Operator-return typecheck gap | Complete | [LISS-0048](../issues/LISS-0048-operator-return-typecheck-gap.md) | Operator locals are registered before return checking; mismatches produce `RETURN_TYPE_MISMATCH` before runtime evaluation. Adjudicator final review approved 2026-07-25. |
| QASM function-call lowering | Complete (Option B scope) | [LISS-0049](../issues/LISS-0049-qasm-function-call-lowering.md) | Split from LISS-0021. Architecture Path selected Option B (2026-07-25): calling a user-defined `fn` from `main` rejects with `QASM_FUNCTION_CALL_UNSUPPORTED` (backend `reject_code` and CLI exit code) instead of silently falling back to the empty-program sketch. Adjudicator final review approved 2026-07-25. Option A (correct inlined output) remains a possible future follow-up, not scheduled. |
| Function keyword migration | Complete | [LISS-0023](../issues/LISS-0023-fn-function-keyword-migration.md); ADR 0066 | `fn` is canonical; `fun` is retired with no alias. |
| Visibility keyword migration | Complete | [LISS-0024](../issues/LISS-0024-pub-only-visibility-keyword.md); ADR 0067 | `pub` is canonical; `public` is retired with no fallback. |
| Explicit returns / lexical scope | Complete | [LISS-0025](../issues/LISS-0025-explicit-return-and-lexical-scope.md); ADR 0068 | Explicit terminal returns and no hidden Operator harvest. |
| Kernel classical boundary / static `forEach` | Historical slice complete; superseded surface tracked | [LISS-0026](../issues/LISS-0026-kernel-classical-boundary-and-static-foreach.md); [ADR 0069](adr/0069-kernel-static-hilbert-space.md) | Static elaboration remains shipped; normative `QubitRegister<N>` migration/resource boundary is complete in LISS-0029. |
| Static Hilbert Kernel type surface | Phase 3 reviewed | [LISS-0029](../issues/LISS-0029-static-hilbert-kernel-surface.md); ADR 0069 | `QubitRegister<N>` is normative; MVP logical-shape/resource checks are explicit; target routing profiles remain separate. |
| Parametric Circuit | Phase 3 reviewed | [LISS-0027](../issues/LISS-0027-parametric-circuit.md); ADR 0070 | Type/diagnostic boundary complete; QPU IR preservation and Host binding remain open. |
| Dynamic QPU lane | Phase 3 reviewed | [LISS-0028](../issues/LISS-0028-dynamic-qpu-lane.md); ADR 0071 | Rejection/capability boundary complete; mid-circuit semantics, timing, and JobResult composition remain open. |
| Real `qft` / `iqft` | Phase 3 reviewed | [LISS-0010](../issues/LISS-0010-kernel-qft-surface.md); [ADR 0078](adr/0078-kernel-qft-iqft-surface.md) | Exact register-typed QFT/IQFT type/provenance boundary complete; gate lowering and official example remain deferred. |
| Density matrix / Lindblad CPTP | Phase 3 reviewed | [LISS-0011](../issues/LISS-0011-density-matrix-lindblad.md); [ADR 0057](adr/0057-density-cptp-lindblad.md) | Numeric/runtime/source and one-qubit symbolic jump slices are complete; general operator algebra, adaptive policy, and QPU execution remain deferred. |
| Explicit Lindblad jump inputs | Phase 3 reviewed | [LISS-0039](../issues/LISS-0039-lindblad-jump-inputs.md); [WP-0005](../work-plans/WP-0005-lindblad-jump-inputs.md) | `JumpSet([RawMatrix(...)])` lowers through the existing RK4 CPU lane; Channel reuse and symbolic jumps remain out of scope. |
| Symbolic Lindblad jump lowering | Phase 3 reviewed | [LISS-0040](../issues/LISS-0040-symbolic-lindblad-jump-lowering.md); [WP-0018](../work-plans/WP-0018-symbolic-lindblad-jump-lowering.md) | Bound one-qubit `Operator` entries in `JumpSet` lower through the RK4 CPU lane; general operator algebra and QPU execution remain out of scope. |
| `evolve ... until` | Phase 3 reviewed | [LISS-0012](../issues/LISS-0012-evolve-until.md); [ADR 0079](adr/0079-evolve-until-kernel-semantics.md) | Grammar/type boundary complete; pure bounded semantics accepted, runtime repetition remains deferred. |
| Pipeline `|>` / currying | Phase 3 reviewed | [LISS-0013](../issues/LISS-0013-pipeline-currying.md); [ADR 0080](adr/0080-pipeline-currying-surface.md) | Minimal left-associative callable-call application and hard effect/operator rejection are shipped; partial-application values and fusion remain deferred. |
| Trait `impl` / `system` expression model | Phase 3 reviewed | [LISS-0014](../issues/LISS-0014-trait-impl-system.md); [ADR 0082](adr/0082-interface-impl-and-system-boundary.md) | Inline `<T: Interface>` bounds, post-merge coherence, marker `System`, and no `pub` in `impl` are shipped; dispatch and specialization remain deferred. |
| Effect marking | Phase 3 reviewed | [LISS-0015](../issues/LISS-0015-effect-marking.md); [ADR 0081](adr/0081-effect-marking-and-propagation.md) | Fixed effect annotations and transitive call/pipeline diagnostics are shipped; effect rows and provider-specific effects remain deferred. |
| Host-side Braket / QPU submit | Phase 3 reviewed | [LISS-0016](../issues/LISS-0016-host-qpu-submit.md); [ADR 0083](adr/0083-provider-neutral-qpu-submit-port.md) | Provider-neutral DTOs and submit/job ports are shipped; provider SDK, credentials, network adapter, and automatic retry remain deferred. |
| Job-based host execution/result boundary | Phase 3 complete | [LISS-0022](../issues/LISS-0022-job-based-host-execution.md); ADR 0065 | Local Job/JobResult boundary, linked-file APIs, CLI, and REPL integration are complete; provider submission, retries, and sessions remain deferred. |
| Operator-position bare `H` | Deferred | [LISS-0009](../issues/LISS-0009-chalkboard-dx.md); ADR 0062 §7 | Existing `Hadamard` / explicit Operator forms remain authoritative until sugar receives a surface/typecheck specification. |
| Higher-order Suzuki / error control | Phase 3 reviewed | [LISS-0017](../issues/LISS-0017-higher-order-suzuki.md); [ADR 0084](adr/0084-higher-order-suzuki-error-contract.md) | S2 QASM lowering, static Bound/EmpiricalEstimate step derivation, and `lowering_policy` provenance are shipped; S4 and adaptive selection remain deferred. |
| Concrete QPU IR lowering | Phase 3 reviewed | [LISS-0041](../issues/LISS-0041-qpu-ir-lowering.md); [ADR 0085](adr/0085-qpu-ir-lowering-opcodes.md) | Immutable in-memory gate/parameter/measurement IR, provenance-preserving projection, and direct OpenQASM adapter input are shipped; dynamic opcodes and serialization remain deferred. |
| QFT/IQFT basic-gate lowering | Phase 3 reviewed | [LISS-0042](../issues/LISS-0042-qft-basic-gate-lowering.md); [ADR 0086](adr/0086-qft-basic-gate-lowering.md) | QFT/IQFT decompose controlled phase and register reversal into ADR 0085 basic gates; controlled/approximate QFT remains deferred. |

## Future theory-to-QPU coverage

The following proposed LISS are the next design inventory for writing common
theoretical-physics expressions without collapsing the Kernel/execution
boundary. Their complete dependency order and non-goals are recorded in
[`WP-0013`](../work-plans/WP-0013-theory-to-qpu-feature-roadmap.md) and the
research roadmap
[`theory-to-qpu-feature-roadmap.md`](../research/2026-07-23-theory-to-qpu-feature-roadmap.md).

| Area | Current status | Tracking | Boundary / acceptance note |
|---|---|---|---|
| Mathematical binders, finite domains, indexed expressions | Phase 3 reviewed | [LISS-0030](../issues/LISS-0030-mathematical-binders-and-indexed-expressions.md) | `sum`/`product` are pure symbolic binders, not imperative loops; runtime lowering remains deferred. |
| Finite mathematical binder lowering | Phase 3 reviewed | [LISS-0043](../issues/LISS-0043-finite-binder-lowering.md); [ADR 0088](adr/0088-finite-binder-lowering.md) | Inclusive Open ranges lower the restricted Pauli nearest-neighbor sum with diagnostics, resource guard, concrete tree, and provenance; periodic/product/general operators remain deferred. |
| Operator algebra and Dirac notation | Phase 3 reviewed | [LISS-0031](../issues/LISS-0031-operator-algebra-and-dirac-notation.md); [ADR 0087](adr/0087-operator-algebra-dirac-notation.md) | Function-shaped typed algebra is shipped; parser-safe reserved Ket forms remain closed and Unicode/named-Ket sugar is deferred. |
| Typed second quantization | Phase 3 reviewed | [LISS-0032](../issues/LISS-0032-typed-second-quantized-operators.md) | Fermion/boson/spin/qubit family boundaries, statistics provenance, and explicit mapping metadata are shipped; exchange normalization and numerical mapping remain deferred. |
| Symbolic expression IR and provenance | Phase 3 reviewed | [LISS-0033](../issues/LISS-0033-symbolic-expression-ir-and-provenance.md) | Source-preserving Symbolic/Resolved IR inspection boundary is shipped; serialized interchange and executable lowering records remain deferred. |
| Phase-separated scientific scopes | Phase 3 reviewed | [LISS-0034](../issues/LISS-0034-phase-separated-scientific-scopes.md) | Immutable sealed contracts and dependency direction complete; full body-level phase typing remains open. |
| Hybrid scientific workflow | Phase 4 reviewed | [LISS-0035](../issues/LISS-0035-hybrid-scientific-workflow.md), [ADR 0072](adr/0072-hybrid-workflow-host-contract.md), [ADR 0073](adr/0073-declarative-workflow-surface.md) | Immutable provider-neutral Workflow/Job DTO boundary; declarative surface and named Host update callback, no provider SDK. |
| Continuous operators and discretization | Phase 3 reviewed | [LISS-0036](../issues/LISS-0036-continuous-operator-and-discretization-boundary.md), [ADR 0074](adr/0074-explicit-discretization-contract.md) | No hidden discretization; explicit contract and Theory-to-Kernel Bridge. Numerical lowering remains deferred. |
| POVM, measurement, and channel contracts | Phase 3 reviewed | [LISS-0037](../issues/LISS-0037-povm-measurement-and-channel-contracts.md); [ADR 0075](adr/0075-povm-measurement-contract.md); [WP-0014](../work-plans/WP-0014-povm-measurement-contract.md) | Terminal computational-basis measurement works for pure/mixed one-qubit states; general effects and dynamic measurement remain out of scope. |
| Semantic discrete carriers and phase-local types | Phase 3 reviewed | [LISS-0038](../issues/LISS-0038-semantic-discrete-carriers.md) | Separate dimensions, indices, counts, basis labels, and physical discrete values before indexed syntax; indexed syntax remains LISS-0030. |
| Numerical representation and continuous PDFs | Phase 3 reviewed | [LISS-0018](../issues/LISS-0018-numerical-representation.md); [ADR 0076](adr/0076-numeric-representation-policy.md); [WP-0015](../work-plans/WP-0015-numeric-representation-policy.md) | Shared dependency-free f64/complex-f64 policy and non-repair validation are shipped; continuous PDFs and exact arithmetic remain deferred. |
| Observation checkpoints and execution diagnostics | Phase 3 reviewed | [LISS-0044](../issues/LISS-0044-observation-checkpoints-and-execution-diagnostics.md); [ADR 0089](adr/0089-observation-checkpoints-and-execution-diagnostics.md); [WP-0021](../work-plans/WP-0021-observation-checkpoints-and-execution-diagnostics.md) | Dependency-free Host observation requests/reports, simulator-only snapshot capability, no hidden measurement, explicit resource cost, and readability review are complete; execution adapters remain deferred. |
| Scientific input and parameter binding | Phase 3 complete | [LISS-0045](../issues/LISS-0045-scientific-input-and-parameter-binding.md); [ADR 0090](adr/0090-scientific-input-and-parameter-binding.md); [WP-0020](../work-plans/WP-0020-scientific-input-and-parameter-binding.md) | Dependency-free scalar Host input, `Param<T>` bindings, immutable sweeps, provenance validation, and readability refactor are complete; result-envelope integration and provider SDKs remain deferred. |
| JobResult observation integration | Phase 3 reviewed | [LISS-0046](../issues/LISS-0046-jobresult-observation-integration.md); [ADR 0091](adr/0091-jobresult-observation-integration.md); [WP-0022](../work-plans/WP-0022-jobresult-observation-integration.md) | Additive immutable `JobResult.observations` preserves existing positional construction and measurement separation; provider adapters, partial-result policy, and WorkflowReport composition remain deferred. |
| Local observation plan execution | Phase 3 reviewed | [LISS-0047](../issues/LISS-0047-local-observation-plan-execution.md); [ADR 0092](adr/0092-local-observation-plan-execution.md); [WP-0023](../work-plans/WP-0023-local-observation-plan-execution.md) | Dependency-free local adapter, deterministic fake source, portable reports, cost-only separate jobs, and hard unsupported-projection diagnostics are reviewed complete; provider/QPU execution remains deferred. |

## Related open evaluations

These are broader research or technology questions already listed in the
architecture overview and remain unassigned unless a row above or a future
Issue gives them a concrete scope:

- SI scale conversion beyond `(L, M, T)`, continuous PDF / Monte Carlo
  representations, exact rational versus `f64` masses, and numeric literal
  lifting: [LISS-0018](../issues/LISS-0018-numerical-representation.md).
- Concrete QPU IR after the amplitude model: [LISS-0019](../issues/LISS-0019-qpu-ir.md), [ADR 0077](adr/0077-provider-neutral-qpu-ir-boundary.md).
- Whether numeric literals are sugar for `dirac`.

## Status rule

`Open` means the design question is known but not accepted for implementation.
`Deferred` means the current Kernel deliberately stops before that boundary.
`Done` on a related Issue does not close a later follow-on listed here; for
example, first-order Trotter is done while higher-order Suzuki remains
deferred.
