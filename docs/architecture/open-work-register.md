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
| Function signatures / returns | Open | [LISS-0021](../issues/LISS-0021-function-signatures-and-returns.md) | Define explicit return types and final-expression returns while keeping `main` as the terminal measurement owner. |
| Function keyword migration | Complete | [LISS-0023](../issues/LISS-0023-fn-function-keyword-migration.md); ADR 0066 | `fn` is canonical; `fun` is retired with no alias. |
| Visibility keyword migration | Complete | [LISS-0024](../issues/LISS-0024-pub-only-visibility-keyword.md); ADR 0067 | `pub` is canonical; `public` is retired with no fallback. |
| Explicit returns / lexical scope | Complete | [LISS-0025](../issues/LISS-0025-explicit-return-and-lexical-scope.md); ADR 0068 | Explicit terminal returns and no hidden Operator harvest. |
| Kernel classical boundary / static `forEach` | Complete for bounded `register(N)` slice; follow-up open | [LISS-0026](../issues/LISS-0026-kernel-classical-boundary-and-static-foreach.md); [ADR 0069](adr/0069-kernel-static-hilbert-space.md) | Static elaboration is shipped. Final register syntax, expansion limits, parameterized QPU values, and dynamic circuits remain open architecture work. |
| Static Hilbert Kernel type surface | Open | [LISS-0029](../issues/LISS-0029-static-hilbert-kernel-surface.md); ADR 0069 | Replace the implementation fixture with type-level `QubitRegister<N>` and explicit logical/resource checks. |
| Parametric Circuit | Open | [LISS-0027](../issues/LISS-0027-parametric-circuit.md); ADR 0070 | Separate symbolic `Param<T>` from `Host<T>` and `State<T>`; gate arguments only. |
| Dynamic QPU lane | Open | [LISS-0028](../issues/LISS-0028-dynamic-qpu-lane.md); ADR 0071 | Separate mid-circuit measurement/feed-forward and target capability negotiation from static Kernel. |
| Real `qft` / `iqft` | Deferred | [LISS-0010](../issues/LISS-0010-kernel-qft-surface.md) | No fake QFT example; define register typing, unitarity, Kernel semantics, SV cases, and an honest-scale example first. |
| Density matrix / Lindblad CPTP | Open | [LISS-0011](../issues/LISS-0011-density-matrix-lindblad.md); ADR 0057 | Requires a separate mixed-state representation and CPTP evolution decision; not implemented in the PMF/amplitude Kernel. |
| `evolve ... until` | Open | [LISS-0012](../issues/LISS-0012-evolve-until.md) | Define predicate domain, termination/bounds, deferred-state semantics, and nontermination/error behavior before parser work. |
| Pipeline `|>` / currying | Open | [LISS-0013](../issues/LISS-0013-pipeline-currying.md) | Specify composition direction, call-chain grammar, partial application, and Operator Fusion interaction. |
| Trait `impl` / `system` expression model | Open | [LISS-0014](../issues/LISS-0014-trait-impl-system.md); ADR 0019 | Decide `impl` syntax and whether `system` is an expression or declaration-only package. |
| Effect marking | Open | [LISS-0015](../issues/LISS-0015-effect-marking.md) | Distinguish measure-capable/host-effectful functions from pure `fn` while preserving the terminal-collapse law. |
| Host-side Braket / QPU submit | Deferred outside Kernel | [LISS-0016](../issues/LISS-0016-host-qpu-submit.md); ADR 0059 | OpenQASM emission is complete. Credentials, provider SDKs, job submission, polling, and retry policy belong to a host adapter, not `compiler/qpex/`. |
| Job-based host execution/result boundary | Open | [LISS-0022](../issues/LISS-0022-job-based-host-execution.md); ADR 0065 | Define provider-neutral Job/Task lifecycle and opaque JobResult before provider submission. |
| Operator-position bare `H` | Deferred | [LISS-0009](../issues/LISS-0009-chalkboard-dx.md); ADR 0062 §7 | Existing `Hadamard` / explicit Operator forms remain authoritative until sugar receives a surface/typecheck specification. |
| Higher-order Suzuki / error control | Deferred | [LISS-0017](../issues/LISS-0017-higher-order-suzuki.md); ADR 0063 | Current QASM lowering is first-order Pauli Trotter with fixed policy; higher-order formulas and user-visible error bounds are later work. |

## Future theory-to-QPU coverage

The following proposed LISS are the next design inventory for writing common
theoretical-physics expressions without collapsing the Kernel/execution
boundary. Their complete dependency order and non-goals are recorded in
[`WP-0013`](../work-plans/WP-0013-theory-to-qpu-feature-roadmap.md) and the
research roadmap
[`theory-to-qpu-feature-roadmap.md`](../research/2026-07-23-theory-to-qpu-feature-roadmap.md).

| Area | Current status | Tracking | Boundary / acceptance note |
|---|---|---|---|
| Mathematical binders, finite domains, indexed expressions | Proposed | [LISS-0030](../issues/LISS-0030-mathematical-binders-and-indexed-expressions.md) | `sum`/`product` are pure symbolic binders, not imperative loops. |
| Operator algebra and Dirac notation | Proposed | [LISS-0031](../issues/LISS-0031-operator-algebra-and-dirac-notation.md) | Bra/ket, adjoint, products, commutators, and typed operator domains. |
| Typed second quantization | Proposed | [LISS-0032](../issues/LISS-0032-typed-second-quantized-operators.md) | Fermion/boson/spin/qubit families and explicit mapping boundary. |
| Symbolic expression IR and provenance | Proposed | [LISS-0033](../issues/LISS-0033-symbolic-expression-ir-and-provenance.md) | Preserve formulas, mappings, discretization, and approximation metadata. |
| Phase-separated scientific scopes | Proposed | [LISS-0034](../issues/LISS-0034-phase-separated-scientific-scopes.md) | `execution → workflow → experiment → theory`; declaration order may defer. |
| Hybrid scientific workflow | Phase 4 Green | [LISS-0035](../issues/LISS-0035-hybrid-scientific-workflow.md), [ADR 0072](adr/0072-hybrid-workflow-host-contract.md), [ADR 0073](adr/0073-declarative-workflow-surface.md) | Immutable provider-neutral Workflow/Job DTO boundary; declarative surface and named Host update callback, no provider SDK. |
| Continuous operators and discretization | Phase 3 Green | [LISS-0036](../issues/LISS-0036-continuous-operator-and-discretization-boundary.md), [ADR 0074](adr/0074-explicit-discretization-contract.md) | No hidden discretization; explicit contract and Theory-to-Kernel Bridge. |
| POVM, measurement, and channel contracts | Proposed | [LISS-0037](../issues/LISS-0037-povm-measurement-and-channel-contracts.md) | Extends, but does not replace, density/CPTP decisions in LISS-0011. |
| Semantic discrete carriers and phase-local types | Proposed | [LISS-0038](../issues/LISS-0038-semantic-discrete-carriers.md) | Separate dimensions, indices, counts, basis labels, and physical discrete values before indexed syntax. |

## Related open evaluations

These are broader research or technology questions already listed in the
architecture overview and remain unassigned unless a row above or a future
Issue gives them a concrete scope:

- SI scale conversion beyond `(L, M, T)`, continuous PDF / Monte Carlo
  representations, exact rational versus `f64` masses, and numeric literal
  lifting: [LISS-0018](../issues/LISS-0018-numerical-representation.md).
- Concrete QPU IR after the amplitude model: [LISS-0019](../issues/LISS-0019-qpu-ir.md).
- Whether numeric literals are sugar for `dirac`.

## Status rule

`Open` means the design question is known but not accepted for implementation.
`Deferred` means the current Kernel deliberately stops before that boundary.
`Done` on a related Issue does not close a later follow-on listed here; for
example, first-order Trotter is done while higher-order Suzuki remains
deferred.
