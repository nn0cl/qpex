# LISS-0194: CredentialPort + Env adapter + mock submit

## Metadata

- Local issue ID: LISS-0194
- Status: **complete**
- ADR: [0161](../architecture/adr/0161-credential-port.md)
- Program: [WP-0066](../work-plans/WP-0066-classical-rational-credentials.md)
- Tests: `tests/test_credential_port_red.py`
- Extends: ADR 0127 / LISS-0016

## Exit

- [x] `CredentialPort` + `EnvCredentialAdapter`
- [x] Mock submit fail-closed on missing credentials
- [x] Mock submit succeeds with injected env; no cloud SDK
