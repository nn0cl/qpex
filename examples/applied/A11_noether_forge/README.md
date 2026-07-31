# A11 — Noether Forge (static slice)

Finite review spine for a quench / spectroscopy **toy**: prepare, local
Hamiltonian evolve, magnetization intent, terminal `measure`. Ownership
modules under `domain/` / `physics/` / `application/` document policy; the
official entry is `main_static.sqx` (self-contained runnable via path or
source).

## Layout

```text
examples/applied/A11_noether_forge/
├── domain/
├── physics/
├── application/
├── presentation/
└── main_static.sqx
```

## Honesty

| Claim | Status |
|-------|--------|
| Full Noether theorem automation / symbolic symmetry engine | **No** |
| Production lattice QCD / condensed-matter forge | **No** |
| Static `|+>` prepare → `evolve` under local `H` → `expect(Z)` → `measure` | **Yes** |
| Multi-module ownership layout for later showcase salvage | **Yes** (docs only until S*) |

## Kernel surfaces

- Type-First `state` / `Operator`
- `evolve … under H for t`
- `expect`, `inspect`, terminal `measure`

## Run

```bash
python3 -m compiler.staqex check examples/applied/A11_noether_forge/main_static.sqx
python3 -m compiler.staqex run examples/applied/A11_noether_forge/main_static.sqx --seed 0
```
