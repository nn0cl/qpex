# LISS-0150: Host coefficient tensor inject

## Metadata

- Local issue ID: LISS-0150
- Status: **complete** — 2026-07-31
- Phase: Feature Path Red → Green
- Depends on: [ADR 0119](../architecture/adr/0119-host-coefficient-tensor-inject.md) Accepted
- Program: [WP-0036](../work-plans/WP-0036-host-tensor-cqft.md)
- Branch: `feature/wp-0036-host-tensor-cqft`
- Tests: `tests/test_host_coefficient_tensor_red.py`

## Summary

In-memory Host `CoefficientTensor` binds into Kernel `Float[…] = host("key")`
placeholders for binder coefficient lookup.

## Exit

- [x] CoefficientTensor validates shape / finiteness / provenance
- [x] Host overlay lowers binders; missing/shape/conflict diagnostics
