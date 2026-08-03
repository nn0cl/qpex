# Quantum-matter discovery (Showcase S1)

Finite spin-chain discovery spine for the locked mission
([mission lock](../../../docs/specs/staqex-v1-showcase-mission-lock.md),
[S0](../../../docs/specs/staqex-v1-showcase-s0-specification.md)).

Surface face (LISS-0298): selective import, struct + free scores / Operator
factories; `DiscoveryModel` remains `class` only for the mutable step clock.

## Run

```bash
python3 -m compiler.staqex run examples/showcase/quantum_matter_discovery/main_quantum_matter_discovery.sqx --seed 0
```

## Layout

| Path | Role |
|---|---|
| `main_quantum_matter_discovery.sqx` | Application spine |
| `domain/` | Couplings + model packs |
| `physics/` | Named-coeff Ising Operator free factories |
| `protocol/` | Quench duration / observation-intent tags |
| `provenance/` | SIM honesty tag (no live QPU) |

No provider SDK. Soft `QSEM_*` diagnostics may appear; hard failures must not.
