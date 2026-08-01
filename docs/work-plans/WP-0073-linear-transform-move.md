# WP-0073: Type-driven linear Call move (Wave 1)

| Field | Value |
|---|---|
| Status | **complete** (2026-08-01) |
| Branch | `batch/wp-0073-linear-transform-move` |
| Batch | [execution-batch-wp-0073.json](../collaboration/reviews/execution-batch-wp-0073.json) |
| Parent | WP-0069 residual / Adjudicator Wave 1 selection |

## Goal

Implement [LISS-0221](../issues/LISS-0221-state-transforming-calls-move-their-input-root.md)
(type-driven move) and close the residual of
[LISS-0202](../issues/LISS-0202-linear-discipline-regression-cluster.md)
(density/Lindblad + slice_b discard).

## Issues

| ID | Title | Status |
|---|---|---|
| [LISS-0221](../issues/LISS-0221-state-transforming-calls-move-their-input-root.md) | State-transforming Calls move their input root | **complete** |
| [LISS-0202](../issues/LISS-0202-linear-discipline-regression-cluster.md) | Linear-discipline regression cluster residual | **complete** |

## Out of this batch

LISS-0199–0201, 0204–0207, 0209–0210, 0212–0219; CI gate; design ADRs 0165/0166.

## Architecture

[ADR 0168](../architecture/adr/0168-type-driven-linear-call-move.md) (**Accepted**).

## Order

1. Batch record + ADR 0168 + ledger/trace
2. LISS-0221 Red → Green in `compiler/staqex/hir.py`
3. Close LISS-0202 residual suites
4. PR

## Verification

```bash
python3 tests/test_liss_0221_state_transforming_calls_move_red.py
python3 tests/test_linear_hardening_slice_b_red.py
python3 tests/test_density_cptp_lindblad_red.py
python3 tests/test_density_cptp_lindblad_numeric_red.py
python3 tests/test_density_cptp_lindblad_source_red.py
python3 tests/test_density_cptp_lindblad_symbolic_red.py
python3 tests/test_lindblad_jump_inputs_red.py
python3 scripts/check-execution-batch-reviews.py --branch batch/wp-0073-linear-transform-move
```
