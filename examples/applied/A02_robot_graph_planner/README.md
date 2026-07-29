# A02 — Robot graph planner

Discrete **configuration-space graph** search: DTQW spread (harvested from
`07`/`09`/`15`) plus a Grover-style corridor oracle (`04`/`12`).

## Honesty

| Claim | Status |
|-------|--------|
| Real-time robot control / SLAM / collision checking | **No** |
| DTQW on `Position` + Grover phase/diffuse toy | **Yes** |
| Production smart-city or orbital routing | **No** |

## Bibliography

- Kempe, J. "Quantum random walks – an introductory overview." *Contemporary Physics* **44** (4), 307–327 (2003).
- Childs, A. M. et al. "Exponential algorithmic speedup by a quantum walk." *STOC* (2003). (Graph search context.)
- Grover, L. K. "A fast quantum mechanical algorithm for database search." *STOC* (1996).

## Run

```bash
python3 -m compiler.staqex run examples/applied/A02_robot_graph_planner/main_robot_graph_planner.sqx --seed 0
```
