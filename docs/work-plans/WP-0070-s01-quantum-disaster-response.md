# WP-0070: S01 Quantum Disaster Response OS

| Field | Value |
|---|---|
| Status | **complete** (2026-08-01) |
| Branch | `feature/wp-0069-s01-disaster-response` (content id WP-0070; branch name retained) |
| Issue | LISS-0222 |
| Path | `examples/showcase/S01_quantum_disaster_response/` |

## Issue rows

| ID | Topic | Status |
|---|---|---|
| LISS-0222 | Disaster OS showcase + full shipped coverage | **complete** |

## Verification

```bash
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_disaster_response.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_morning_collect.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_day2_recovery.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_route_interference.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_comms_channel.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_burst_spectrum.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_tri_register.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_fidelity_inner_check.sqx --seed 0
python3 examples/showcase/S01_quantum_disaster_response/host/demand_inject.py
STAQEX_AGENCY_TOKEN=demo python3 examples/showcase/S01_quantum_disaster_response/host/agency_share.py
python3 examples/showcase/S01_quantum_disaster_response/host/rolling_replan_job.py
```

Scorecard A+B evidence filled in
[`staqex-v1-s01-coverage-scorecard.md`](../specs/staqex-v1-s01-coverage-scorecard.md).
