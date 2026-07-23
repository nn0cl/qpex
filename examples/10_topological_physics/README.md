# 10 — Topological SSH (namespace / enum / struct / class + `fn init`)

Demonstrates OOP as **physical systems + parameter packs**, ADR **0054** linking,
and tight-binding `hop(i,j)` Schrödinger evolution.

## Layout

```text
examples/10_topological_physics/
├── domain/
│   ├── topology.qpex          # Topology { enum, struct }
│   └── ssh_parameters.qpex     # Topology.SSH { struct, class + init, `_t` }
├── operators/
│   └── hamiltonian_builder.qpex
└── main_ssh_topological.qpex
```

No `module-info.qpex` required.

## Honesty notes

| Feature | Status |
|---------|--------|
| `namespace` / `enum` / `struct` / `class`+`this` | Implemented |
| `fn init` + `ClassName(…)` | Implemented |
| `pub` / leading `_` (ADR 0058) | Implemented |
| `fn` (not Retired `fn`) | Active |
| `new` / `protected` | **Forbidden** |
| Lindblad / density matrix (ADR 0057) | **Open** |

## Run

```bash
python3 -m compiler.qpex run examples/10_topological_physics/main_ssh_topological.qpex --seed 0
```
