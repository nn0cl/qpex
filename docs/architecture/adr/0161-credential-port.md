# ADR 0161: CredentialPort + Env adapter (extends ADR 0127)

## Status

**Accepted** (2026-07-31) — unlocks LISS-0194 under WP-0066.
Extends [ADR 0127](0127-live-qpu-credentials-boundary.md) /
[ADR 0083](0083-provider-neutral-qpu-submit-port.md).

## Decisions

1. Host `CredentialPort` looks up named credentials; missing → `None`
   (never invent secrets).
2. `EnvCredentialAdapter` reads an injected mapping or `os.environ`.
3. `CredentialGatedMockSubmit` is a fail-closed mock `QpuSubmitPort`: missing
   required credentials raise `CredentialSubmitError` with
   `CREDENTIAL_MISSING`; success returns a local opaque job id.
4. **No** cloud SDK, network adapter, or technology selection in this ADR.
5. Kernel syntax still must not embed credentials (ADR 0127).

## Non-goals

Selecting AWS/Azure/IBM/… SDKs; retries; live network submit.

## Consequences

- Honesty catalog / technology selection remain separate approvals.
- Agents must not invent API keys or ship provider SDKs under this ADR.
