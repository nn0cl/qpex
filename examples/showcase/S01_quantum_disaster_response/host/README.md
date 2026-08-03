# S01 Host (H-lane)

Ops shell companions — not the E-lane tonight spine.

| Script | Role |
|---|---|
| `demand_inject.py` | Demand noise → finite inject (ADR 0163/0164) |
| `field_compose_inject.py` | **CH-field-compose Host substitute** — weight → mask → finiteize with `continuous_pipeline` provenance ([LISS-0317](../../../../docs/issues/LISS-0317-ch-field-compose-host-demo.md); Ideal [§2A](../../../../docs/specs/staqex-v1-continuous-lane-b-expressiveness-scenarios.md)) |
| `agency_share.py` | CredentialPort gate (fail-closed without token) |
| `rolling_replan_job.py` | Job-shaped replan envelope |
| `export_tonight_ticket.py` | TonightTicket structured handoff |

```bash
python3 examples/showcase/S01_quantum_disaster_response/host/field_compose_inject.py
python3 examples/showcase/S01_quantum_disaster_response/host/demand_inject.py
```

**Honesty:** multi-step continuous algebra in `field_compose_inject.py` is **Host
Python**, not mid-program Kernel `Continuous`. Ideal form remains §2A; Runtime
seat status stays **weak** until a future Lane B ship ADR.
