# ADR 0127: Live QPU credentials — Architecture Path boundary

## Status

**Accepted as design boundary** (2026-07-31) — LISS-0159 docs.

## Decision

1. Reopen allows Architecture Path work on **provider-neutral** submit ports
   already sketched (ADR 0083 / LISS-0016).
2. Credentials, network adapters, and vendor SDKs remain **Host adapters** —
   never Kernel syntax, never embedded secrets in source.
3. Honesty catalog ([qpu-capability-honesty](../../specs/staqex-v1-qpu-capability-honesty.md))
   stays normative: Kernel must not claim live submit until an adapter ADR
   selects a provider under Adjudicator technology approval.

## Non-goals

Shipping a concrete cloud provider SDK in this ADR; inventing API keys.

Provider-neutral `CredentialPort` + env adapter + fail-closed mock submit are
unsealed by [ADR 0161](0161-credential-port.md); real cloud SDKs remain
technology-selection gated.
