# LISS-0142: Suzuki S4 QASM lowering

## Metadata

- Local issue ID: LISS-0142
- Status: **complete** — 2026-07-31
- Phase: Feature Path Red → Green → Refactor
- Type: Kernel / QASM
- Priority: P0 (WP-0032)
- Depends on: ADR 0084 S4 amendment; LISS-0017 S2 shipped
- Program: [WP-0032](../work-plans/WP-0032-adr-deferred-finite-slices.md)
- Implementation permission: **yes** (Adjudicator Plan 承認 2026-07-31)
- Branch: `feature/wp-0032-adr-deferred-finite`
- Tests: `tests/test_higher_order_suzuki_red.py` (extended)

## Summary

`using Suzuki(order = 4, …)` emits recursive S4 product formula gates with
order-4 static step derivation. Orders other than 2 and 4 remain hard
rejected. SV `expm_ih` unchanged.

## Exit

- [x] Red/Green: order=4 accepted; order=3 rejected
- [x] QASM emits S4 sequence; Bound/Empirical use S4 contract
- [x] ADR 0084 amended
