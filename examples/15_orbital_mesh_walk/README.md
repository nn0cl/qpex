# 15 — Orbital mesh walk (DTQW toy)

Dream: a **LEO / deep-space relay mesh** that spreads information ballistically
via a quantum walk on constellation nodes.

## Layout

```text
examples/15_orbital_mesh_walk/
├── domain/
│   └── constellation.qpex      # MeshParams + Role enum
├── operators/
│   └── mesh_walk.qpex          # Coin + step_orbital_hop
└── main_orbital_mesh.qpex      # evolve ×20 DTQW, measure Position
```

## Honesty

| Claim | Status |
|-------|--------|
| Real Kepler / RF / ISL routing | **No** — line Position mesh |
| Galaxy-scale networking | **No** — pedagogical spread |
| Multi-file DTQW skeleton | **Yes** (same pattern as 09) |

## Run

```bash
python3 -m compiler.qpex run examples/15_orbital_mesh_walk/main_orbital_mesh.qpex --seed 0
```
