# WP-0066: Classical rational + CredentialPort

| Field | Value |
|---|---|
| Status | **complete** (2026-07-31) |
| Branch | `feature/wp-0066-rational-credentials` |
| Parent | WP-0038 / ADR 0125–0127 |

## Issue rows

| ID | Topic | Mode | Status |
|---|---|---|---|
| LISS-0193 | Classical Fraction → f64 at State (ADR 0160) | ship | complete |
| LISS-0194 | CredentialPort + Env + mock (ADR 0161) | ship | complete |

## Verification

- `python3 tests/test_classical_rational_red.py`
- `python3 tests/test_credential_port_red.py`
