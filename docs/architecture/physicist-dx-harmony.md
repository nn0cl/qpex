# Physicist mental model × programmer DX

QPex aims at **both**:

1. **Physicist aesthetics** — blackboard surface (states, operators, dimensions,
   exclusive classifications), not enterprise boilerplate.
2. **Programmer DX** — `enum` / `struct` / `namespace` / visibility so large
   simulations stay typed and maintainable.

Importing Java ceremony (`protected`, mandatory `module-info`) fails (1).
Omitting structure fails (2). Every DX feature must have a **physics reading**.

| DX feature | Physics reading |
|------------|-----------------|
| `enum` | Mutually exclusive geometry / bases (`Periodic` \| `Open`) |
| `struct` | Immutable parameter packs (\(v,w,\hbar\)) — value objects |
| `class` | **Physical system** (setup + evolving state), not “OOP class” |
| `fun init` + `Type(…)` | Experimental setup (no `new`) |
| `namespace` | Theory sectors (`Topology`, `Hamiltonian`, …) |
| default / `pub` / `_` | Local law visible; library API marked `pub`; internals `_` |
| `module-info` | Optional metadata only — **not required for scripts** |

## Access (ADR 0058 revised)

- Default = module-private (no keyword noise on everyday equations).
- `pub` (alias `public`) = export across modules.
- Leading `_` = class-private → `PRIVATE_ACCESS_VIOLATION_ERROR`.
- Cross-module use of non-`pub` → `MODULE_PRIVATE_ACCESS_ERROR`.
- No `protected`, no inheritance — compose parameters / systems.
- Method keyword is **`fun`** (`fn` is Retired).

## Roadmap status (Kernel)

| Phase | Step | Status |
|-------|------|--------|
| 1 Geometry & parameters | 1.1 `enum` | **Shipped** |
| 1 | 1.2 `struct` | **Shipped** |
| 2 Domain & encapsulation | 2.1 `namespace` | **Shipped** |
| 2 | 2.2 visibility (`pub` / `_`) | **Shipped** |
| 3 Stateful systems | 3.1 `class` / `this` / `fun init` | **Shipped** |
| Open systems | ADR 0057 density / Lindblad | **Open** |

## Entry points

- Humans: `QUICKSTART.md` / `QUICKSTART.ja.md`
- Spec: `docs/specs/qpex-language-specification.md` §6.4–§6.5
- Example: `examples/10_topological_physics/`
- Tests: `tests/test_modern_oop_and_visibility.py`

Verification: `python3 tests/spec_verification/run_all.py`
