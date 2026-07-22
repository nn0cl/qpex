# 12 — City route search (Grover toy)

Dream: a **congestion-free city** that evaluates arterial corridors in
superposition and amplifies the free path.

## Layout

```text
examples/12_city_route_search/
├── domain/
│   └── city_graph.qpex         # CorridorMap + Corridor enum
├── operators/
│   └── route_oracle.qpex       # classical target index note
└── main_city_route.qpex        # Grover phase + diffuse on N=4
```

## Honesty

| Claim | Status |
|-------|--------|
| Real metro / traffic assignment | **No** — 4 corridors only |
| Full routing + capacity constraints | **No** — single marked index |
| Grover amplify skeleton | **Yes** |

## Run

```bash
python3 -m compiler.qpex run examples/12_city_route_search/main_city_route.qpex --seed 0
```
