# WP-0072: S01 coverage residuals (Joint NYI + shipped-surface wiring)

| Field | Value |
|---|---|
| Status | **complete** (2026-08-01) |
| Branch | `batch/wp-0072-s01-coverage-residuals` |
| Batch | [execution-batch-wp-0072.json](../collaboration/reviews/execution-batch-wp-0072.json) |
| Discovery | WP-0071 re-check; scorecard residuals |

## Issues

| ID | Title | Status |
|---|---|---|
| [LISS-0228](../issues/LISS-0228-joint-apply-qft-runtime.md) | Joint `apply(qft/iqft/cqft, …)` runtime | **complete** |
| [LISS-0229](../issues/LISS-0229-inner-outer-joint-runtime-call.md) | `inner`/`outer` Joint runtime Call | **complete** |
| [LISS-0230](../issues/LISS-0230-s01-wire-shipped-surfaces.md) | S01 wire Basis / Trace-Out / Algebraic Fusion / Rankine·troy | **complete** |
| [LISS-0231](../issues/LISS-0231-s01-impl-interface-dispatch.md) | S01 `impl` interface-mediated dispatch | **complete** |
| [LISS-0232](../issues/LISS-0232-s01-index-lattice-beyond-two-wires.md) | S01 Index lattice beyond 2-wire toy | **complete** |

## Verification

```bash
python3 tests/test_liss_0228_joint_apply_qft_runtime_red.py
python3 tests/test_liss_0229_inner_outer_joint_runtime_call_red.py
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_disaster_response.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_burst_spectrum.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_fidelity_inner_check.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_lattice_four.sqx --seed 0
```
