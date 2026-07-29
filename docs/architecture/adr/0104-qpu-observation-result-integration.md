# ADR 0104: QPU observation/result integration boundary

- Status: Accepted
- Date: 2026-07-27
- Related: ADR 0091, ADR 0092, ADR 0103, LISS-0044, LISS-0046, LISS-0047,
  LISS-0065, LISS-0066

## Context

Staqex now has explicit observation plans, an immutable `JobResult.observations`
field, provider-neutral QPU submit orchestration, and a fixed QPU lifecycle.
The remaining boundary is the projection of a completed QPU job into those
observation contracts without exposing provider objects or simulator-only
state.

## Decisions

Keep QPU observation integration in a Host use case. The Kernel and existing
language semantics remain unchanged. The flow is:

```text
ObservationPlan + QPU Job handle
  → terminal lifecycle gate
  → provider-neutral observation payload
  → immutable ObservationReport values
  → JobResult.observations
```

Only successful jobs may publish measurements or observation values. QPU
results cannot contain internal state-vector or density-matrix snapshots.
Provider-specific result schemas remain inside adapters.

### 1. Reuse a structured provider-neutral result payload

`QpuJobPort.result()` remains the single result input. Its observation entries
are structured provider-neutral mappings, and the Host projector maps them to
`ObservationReport`. A separate `ObservationValueSource` port is not added to
the QPU lane.

### 2. Preserve source-plan order

Reports are emitted in the order of `ObservationPlan.requests`, not provider
completion order. Every requested checkpoint must be matched exactly once.

### 3. Fail closed on incomplete observations

If a successful provider job is missing a requested observation, contains an
unknown checkpoint, or contains an unsupported projection, the Host result is
`failed` with `QPU_OBSERVATION_INCOMPLETE` (or the more specific hard
diagnostic). No measurements or observation values are returned.

### 4. Keep logical identity across explicit attempts

Retries preserve the logical Job identity. Each attempt retains its opaque
provider Job ID and one-based attempt number in result metadata. Results from
different attempts are never merged.

### 5. Keep `separate_job` metadata-only in the MVP

`separate_job` and its cost remain recorded in the plan/result metadata. This
slice does not create child jobs.

## Candidate boundary

- `QpuJobPort` supplies lifecycle and a provider-neutral result payload.
- A Host projection service validates the observation plan and maps portable
  values to `ObservationReport`.
- `JobResult` remains the external Host DTO; `Joint`, AST, provider SDK
  objects, and raw simulator state do not cross the boundary.
- The first implementation, if accepted, uses deterministic fake ports and no
  external dependency.

## Consequences

- QPU observations become consumable through the same provider-neutral Host
  result family as local observations.
- Partial results and hidden measurement cannot leak through the boundary.
- Provider technology remains a later, separate decision.
- A small fake adapter can validate the contract without credentials or a live
  service.

## Approval status

This ADR is accepted for LISS-0066 Phase 1 Red. It does not authorize Phase 2
implementation, provider selection, or live QPU integration.
