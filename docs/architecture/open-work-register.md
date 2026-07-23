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
| Real `qft` / `iqft` | Deferred | [LISS-0010](../issues/LISS-0010-kernel-qft-surface.md) | No fake QFT example; define register typing, unitarity, Kernel semantics, SV cases, and an honest-scale example first. |
| Density matrix / Lindblad CPTP | Open | [LISS-0011](../issues/LISS-0011-density-matrix-lindblad.md); ADR 0057 | Requires a separate mixed-state representation and CPTP evolution decision; not implemented in the PMF/amplitude Kernel. |
| `evolve ... until` | Open | [LISS-0012](../issues/LISS-0012-evolve-until.md) | Define predicate domain, termination/bounds, deferred-state semantics, and nontermination/error behavior before parser work. |
| Pipeline `|>` / currying | Open | [LISS-0013](../issues/LISS-0013-pipeline-currying.md) | Specify composition direction, call-chain grammar, partial application, and Operator Fusion interaction. |
| Trait `impl` / `system` expression model | Open | [LISS-0014](../issues/LISS-0014-trait-impl-system.md); ADR 0019 | Decide `impl` syntax and whether `system` is an expression or declaration-only package. |
| Effect marking | Open | [LISS-0015](../issues/LISS-0015-effect-marking.md) | Distinguish measure-capable/host-effectful functions from pure `fun` while preserving the terminal-collapse law. |
| Host-side Braket / QPU submit | Deferred outside Kernel | [LISS-0016](../issues/LISS-0016-host-qpu-submit.md); ADR 0059 | OpenQASM emission is complete. Credentials, provider SDKs, job submission, polling, and retry policy belong to a host adapter, not `compiler/qpex/`. |
| Job-based host execution/result boundary | Open | [LISS-0022](../issues/LISS-0022-job-based-host-execution.md); ADR 0065 | Define provider-neutral Job/Task lifecycle and opaque JobResult before provider submission. |
| Operator-position bare `H` | Deferred | [LISS-0009](../issues/LISS-0009-chalkboard-dx.md); ADR 0062 §7 | Existing `Hadamard` / explicit Operator forms remain authoritative until sugar receives a surface/typecheck specification. |
| Higher-order Suzuki / error control | Deferred | [LISS-0017](../issues/LISS-0017-higher-order-suzuki.md); ADR 0063 | Current QASM lowering is first-order Pauli Trotter with fixed policy; higher-order formulas and user-visible error bounds are later work. |

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
