# A06 — Topological edge memory

SSH edge occupation as pedagogical **topological memory** on a tight-binding chain.

Legacy source: `examples/10_topological_physics/`.

## Layout

```text
examples/applied/A06_topological_edge_memory/
├── domain/
│   ├── topology.qpex
│   └── ssh_parameters.qpex
├── operators/
│   └── hamiltonian_builder.qpex
└── main_topological_edge_memory.qpex
```

## Honesty

| Claim | Status |
|-------|--------|
| Full SSH phase diagram / disorder / finite-size scaling | **No** |
| OOP domain + multi-file `import` + `evolve` on `hop` Hamiltonian | **Yes** |
| Production topological qubit / Majorana hardware | **No** |

## Bibliography

- Su, W. P., Schrieffer, J. R., Heeger, A. J. "Solitons in polyacetylene." *Phys. Rev. Lett.* **42**, 1698 (1979).

## Run

```bash
python3 -m compiler.qpex run examples/applied/A06_topological_edge_memory/main_topological_edge_memory.qpex --seed 0
```
