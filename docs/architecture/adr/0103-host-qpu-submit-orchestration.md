# ADR 0103: Host QPU submit orchestration boundary

- Status: Accepted
- Date: 2026-07-27
- Related: ADR 0083, ADR 0065, LISS-0016, LISS-0022, LISS-0041,
  LISS-0064, LISS-0065

## Context

QPex now has provider-neutral QPU submit ports, immutable QASM artifacts,
Job/JobResult DTOs, and resource/capability rejection before a QPU boundary.
The remaining gap is orchestration between those contracts. The local
Simulator `submit_source` path must not become a mixed local/provider entry
point, and provider SDK choices must remain outside the compiler Kernel.

## Decisions

### 1. Use a dedicated Host use case

QPU submission is exposed through a dedicated Host orchestration use case. The
existing `submit_source` and `submit_path` functions remain local Job adapter
entry points and are not extended with provider branches.

The QPU flow is:

```text
source or QASM artifact
  → compile / validate
  → QpuSubmitRequest
  → QpuSubmitPort
  → ProviderJobId
  → QpuJobPort lifecycle
  → provider-neutral JobResult
```

### 2. Keep `JobRequest` and `QpuArtifact` separate

`JobRequest` remains the Workflow-layer description of an experiment,
bindings, and execution policy. `QpuArtifact` remains the compiled QASM,
target profile, provenance, and content hash.

The orchestration layer performs an explicit mapping:

```text
JobRequest → QpuSubmitRequest
                 ├─ QpuArtifact
                 ├─ execution_settings
                 ├─ idempotency_key
                 └─ retry_policy
```

Neither type is flattened into the other, and existing `JobRequest` fields are
not reinterpreted as provider fields.

### 3. Reuse the fixed lifecycle vocabulary

The provider-neutral lifecycle is exactly:

```text
queued | running | succeeded | failed | cancelled
```

Provider-specific states are converted by the Host adapter. Provider state
names and SDK objects do not cross the port.

### 4. Do not expose partial results

Only `succeeded` jobs may carry measurement results. `failed`, `cancelled`,
`queued`, and `running` results contain no measurements. Cancellation is an
explicit operation and never implies an automatically recovered or partial
success.

### 5. Make retry attempts explicit

`QpuSubmitRequest` carries a one-based `attempt` field. The Host owns the
logical idempotency key and explicitly requests each retry; adapters must not
retry silently.

## Error vocabulary

The orchestration boundary uses provider-neutral diagnostics:

- `QPU_SUBMIT_REJECTED`
- `QPU_SUBMIT_FAILED`
- `QPU_JOB_FAILED`
- `QPU_JOB_CANCELLED`
- `QPU_RESULT_UNAVAILABLE`
- `QPU_RETRY_NOT_AUTHORIZED`

Existing resource and capability diagnostics remain the source diagnostics for
pre-submit rejection and are not silently replaced.

## Consequences

- Local execution and QPU submission have separate entry points.
- Workflow semantics, compiled artifacts, and provider lifecycle remain
  independently typed.
- Retry and cancellation are observable and reproducible.
- A local fake adapter can validate the contract without credentials or
  network access.
- The orchestration layer needs an explicit mapper from `JobRequest` to
  `QpuSubmitRequest`.

## Non-goals

- No provider or SDK selection.
- No authentication, credential storage, network transport, or automatic retry.
- No changes to QPex language syntax or compiler Kernel dependencies.

## Acceptance gate

This ADR authorizes the LISS-0065 Phase 1 Red contract after test review. It
does not authorize provider technology selection or live integration.
