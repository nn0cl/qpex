# LISS-0063: SimulatorResourceBudget runtime enforcement

## Metadata

- Local issue ID: LISS-0063
- GitHub issue: none
- Status: Phase 3 Refactor complete for the provider-neutral decision boundary; runtime wiring follow-up open
- Phase: Architecture/Feature boundary — Phase 0 design intake → Phase 1 Red → Phase 2 Green → Phase 3 Refactor
- Type: simulator execution safety
- Priority: P1
- Initial planning size: M
- Current planning size: M
- Owner/agent: Codex
- Depends on: LISS-0062, ADR 0100
- Related work plan: WP-0004

## Summary

Apply the already accepted `SimulatorResourceBudget` to local simulator
execution. The estimate must be checked before state allocation or numerical
evolution crosses the execution boundary. The implementation must preserve
the distinction between compiler expansion safety, simulator capacity, and
QPU target capability.

This Issue does not add provider SDKs, QPU capability discovery, or new
mathematical syntax.

## [DESIGN CHECK]

- Scope and expected behavior: Load the existing `ResourceProfile`, estimate
  the selected simulator representation, and either continue with an explicit
  warning or abort before producing a simulator result.
- Specifications and files inspected: ADR 0100, LISS-0062,
  `compiler/staqex/resource_profile.py`, `compiler/staqex/run.py`, and the QASM
  compiler boundary.
- Component boundaries, ports/adapters, and VO/DTO candidates: manifest
  loading remains the Host configuration adapter; `ResourceProfile` and
  `SimulationResourceEstimate` remain immutable DTOs; the simulator execution
  boundary consumes the DTO and returns structured diagnostics. The Kernel
  does not read `staqex.toml`.
- Applicable constraints: `Warn` is local-simulator-only. `Abort` produces no
  executable simulator result. QASM and QPU lanes always reject an exceeded
  simulator budget. No truncation, normalization, state reduction, symbolic
  fallback, or silent continuation is permitted.
- Decisions, assumptions, and unresolved ambiguities: `Warn` diagnostics are
  returned in the existing structured result diagnostics rather than printed
  directly by the runtime. The estimate is checked before evaluator state
  allocation. CPU-time prediction remains out of scope. The exact adapter
  method name is intentionally left to Phase 1 implementation design.
- Included and omitted AI context: included ADR 0100, LISS-0062, the resource
  DTO implementation, and run/QASM boundaries; omitted provider SDKs, cloud
  credentials, and unrelated numerical models.
- Task routing: Codex with deterministic repository tests and local simulator
  inspection; no external provider or model is required.
- Input/output evidence contract: input is a `ResourceProfile` plus a
  representation-aware execution request; output is either a simulator result
  with any `SIMULATOR_RESOURCE_WARNING`, or a structured hard diagnostic
  `SIMULATOR_RESOURCE_ERROR` with estimate, limit, representation, and policy.
- Verification plan: Phase 1 Red tests cover Warn continuation, Abort before
  execution, default profile behavior, DensityState/Lindblad estimates, and
  QASM/QPU rejection. Phase 2 Green wires the smallest execution boundary.

## Accepted behavior

### Local simulator

| Policy | Estimate <= limit | Estimate > limit |
|---|---|---|
| `Warn` | Continue without warning | Continue and emit `SIMULATOR_RESOURCE_WARNING` |
| `Abort` | Continue | Stop before evaluation and emit `SIMULATOR_RESOURCE_ERROR` |

The warning or error must preserve the immutable estimate and the selected
profile metadata. A warning is not printed as an incidental side effect and
does not authorize a partial result.

### QASM and QPU lanes

An exceeded `SimulatorResourceBudget` is always a hard rejection with
`SIMULATOR_RESOURCE_ERROR`, regardless of the manifest's simulator policy.
The lanes must not emit QASM, QPU IR, or a provider submission after rejection.

## Diagnostics

- `SIMULATOR_RESOURCE_WARNING`: local simulation continues under explicit
  `Warn` policy.
- `SIMULATOR_RESOURCE_ERROR`: execution is rejected before allocation or
  lowering crosses a protected boundary.

Diagnostics include the representation, logical-qubit count, estimated bytes,
configured limit, policy, workspace factor, and formula version when known.

## Non-goals

- No CPU-time or wall-clock prediction.
- No benchmark recalibration of ADR 0100 factors.
- No provider SDK, credentials, network, retry, or target-capability logic.
- No changes to binder expansion budgets or the static Hilbert 1024-qubit
  compiler boundary.
- No truncation, normalization, approximation, or state-space reduction.

## Phase 1 Red record

Added `tests/test_simulator_resource_enforcement_red.py`. The four tests define
the provider-neutral decision boundary for local `Warn`, local `Abort`, QASM
lane hard rejection, and the exact-at-limit continuation case. They currently
fail because no enforcement module exists; no production code or manifest
semantics were changed.

Phase 2 Green required explicit approval after the Red results were reviewed.

## Open-work relationship

LISS-0062 remains complete for manifest loading and deterministic estimation.
LISS-0063 promotes only its explicitly deferred runtime enforcement slice.
ADR 0100 remains the authoritative policy; no new architecture decision is
required unless implementation discovers a boundary not covered by that ADR.

## Phase 2 Green record

- Added `compiler/staqex/resource_enforcement.py` as the immutable, provider-
  neutral execution decision boundary.
- Local simulator `Warn` continues with
  `SIMULATOR_RESOURCE_WARNING`; local `Abort`, QASM, and QPU lanes stop with
  `SIMULATOR_RESOURCE_ERROR`.
- Under-limit estimates continue without a diagnostic.
- The module does not load manifests, allocate state, emit QASM, or contact a
  provider; those integrations remain explicit follow-up wiring within the
  accepted boundary.
- Verification: LISS-0063 tests and LISS-0062 resource-profile tests pass;
  Python compilation and `git diff --check` pass.

## Phase 3 Refactor record

- Separated lane policy evaluation from contextual diagnostic construction.
- Preserved the immutable decision DTO, warning/error codes, and all lane
  semantics without changing assertions or behavior.
- Reviewer empathy: the public decision function now reads as a short policy
  flow, while diagnostic formatting is isolated in a named helper.
- Runtime wiring into `run` and QASM emission is tracked separately in
  [LISS-0064](LISS-0064-simulator-resource-execution-wiring.md). Provider
  submission remains a later Host adapter follow-up because this slice
  intentionally stops at the decision boundary.
