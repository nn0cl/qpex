# A07 — Open-system sensor

**Lindblad** detector readout with explicit `JumpSet` inputs — applied narrative
for decoherence / open-system sensing (see also B12).

Legacy source: Lindblad slice from `examples/16_quantum_observatory/`.

## Honesty

| Claim | Status |
|-------|--------|
| Calibrated detector quantum tomography | **No** |
| Continuous Fock/grid sensor models | **No** (see `16/cpu/continuous_models.sqx` reference) |
| Explicit `lindblad` + terminal `measure` on `DensityState` | **Yes** |

## Bibliography

- Lindblad, G. "On the generators of quantum dynamical semigroups." *Communications in Mathematical Physics* **48**, 119–130 (1976).

## Run

```bash
python3 -m compiler.staqex run examples/applied/A07_open_system_sensor/main_open_system_sensor.qpex --seed 0
```
