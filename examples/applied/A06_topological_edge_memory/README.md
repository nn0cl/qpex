# A06 — Topological edge memory

SSH edge occupation as pedagogical **topological memory** on a tight-binding chain.

Legacy source: `examples/10_topological_physics/`.

## Layout

```text
examples/applied/A06_topological_edge_memory/
├── domain/
│   ├── topology.sqx
│   └── ssh_parameters.sqx
├── operators/
│   └── hamiltonian_builder.sqx
└── main_topological_edge_memory.sqx
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
python3 -m compiler.staqex run examples/applied/A06_topological_edge_memory/main_topological_edge_memory.sqx --seed 0
```
