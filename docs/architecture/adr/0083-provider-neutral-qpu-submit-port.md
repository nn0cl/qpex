# ADR 0083: Provider-neutral QPU submission port

## Status

Accepted (2026-07-24). The provider-neutral DTO and port contract slice is
implemented and reviewed. Python library port first, fixed lifecycle states,
Host-owned idempotency keys, explicit retry only, opaque Provider Job IDs, and
local fake adapter first remain the accepted boundary.

Companion: [LISS-0016](../../issues/LISS-0016-host-qpu-submit.md).

## Context

ADR 0059 makes OpenQASM emission a zero-dependency compiler boundary. ADR 0065
defines a provider-neutral Job/JobResult boundary. A cloud submission feature
must connect those boundaries without allowing credentials, provider SDKs, or
retry policy to enter the Kernel.

## Proposed decision

1. The compiler produces an immutable `QpuArtifact` containing OpenQASM text,
   target profile, provenance, and a content hash. Compilation never submits.
2. A Host `QpuSubmitPort` accepts a `QpuSubmitRequest` and returns a
   provider-neutral `ProviderJobId`. A separate `QpuJobPort` exposes status,
   wait, result, and cancel operations.
3. Core tests use a local fake adapter. Braket, IBM, or other providers are
   optional adapters and are not selected or imported by the Kernel.
4. Retry, idempotency, cancellation, and resume are explicit contract fields.
   An adapter must not silently resubmit an operation whose idempotency policy
   is unknown.
5. Credentials are supplied through a Host secret/settings port; they never
   appear in Staqex source, QPU IR, compiler diagnostics, or persisted Kernel
   values.

## Candidate DTOs

```text
QpuArtifact { qasm, target_profile, provenance, content_hash }
QpuSubmitRequest { artifact, execution_settings, idempotency_key, retry_policy }
ProviderJobId { provider, opaque_id }
ProviderJobState { queued | running | succeeded | failed | cancelled }
QpuResult { status, measurements, metadata, provider_reference }
```

The exact field names and serialization are not yet normative.

## Resolved decisions

- Python library port comes before a CLI adapter.
- Lifecycle states are `queued`, `running`, `succeeded`, `failed`, and
  `cancelled`; terminal states never transition again.
- The Host owns idempotency-key generation.
- No automatic retry occurs. Retry is performed only when an explicit policy is
  supplied and the operation is declared retryable.
- The first adapter is local fake-only. No cloud Provider is selected yet.
- Provider Job IDs are opaque DTOs and may be retained only by the Host layer.

## Consequences

Positive:

- Kernel remains portable and provider-neutral.
- Fake adapter tests can validate lifecycle behavior without network access.
- OpenQASM provenance and job identity remain observable at the Host boundary.

Deferred:

- SDK selection and installation;
- credentials and secret storage;
- live submission, polling, retry, and provider-specific mapping.
