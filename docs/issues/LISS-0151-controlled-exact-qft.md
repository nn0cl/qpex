# LISS-0151: Controlled exact QFT (`cqft` / `ciqft`)

## Metadata

- Local issue ID: LISS-0151
- Status: **complete** — 2026-07-31
- Phase: Feature Path Red → Green
- Depends on: [ADR 0120](../architecture/adr/0120-controlled-exact-qft.md) Accepted
- Program: [WP-0036](../work-plans/WP-0036-host-tensor-cqft.md)
- Branch: `feature/wp-0036-host-tensor-cqft`
- Tests: `tests/test_controlled_qft_red.py`

## Summary

Exact single-control `cqft(ctrl, reg)` / `ciqft(ctrl, reg)` with ADR 0086
basic-gate lowering. Approximate QFT remains out.

## Exit

- [x] Typecheck accepts cqft/ciqft; rejects bad arity
- [x] QPU IR opcodes ⊆ basic vocabulary; provenance source cqft/ciqft
