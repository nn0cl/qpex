# AI work trace — WP-0083 LISS-0236 Kernel MeasureSinkPort

| Field | Value |
|---|---|
| Date | 2026-08-02 |
| Branch | `batch/wp-0083-kernel-measure-sink-port` |
| Issue | LISS-0236 |
| Ship ADR | 0171 |

## Change

- New `compiler/staqex/measure_sink_port.py`: `MeasureSinkPort`,
  TextIO / file adapters, `resolve_measure_sink`.
- Evaluator `measure` / `snapshot` / `inspect` emit via the port;
  optional `measure_sink=` override for tests.
- `write_sink` delegates to the same adapters.
- Red suite `tests/test_liss0236_kernel_measure_sink_port_red.py`.

## Verification

`.venv/bin/pytest tests/` → 1078 passed / 0 failed.
