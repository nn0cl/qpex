# Host MC → finite State inject (ADR 0163 / 0164)

Runnable Host demo: continuous draw → equal-width histogram finiteization →
finite Joint Born masses. No Kernel `Continuous` type.

**Notebook surface (preferred teaching path):** ADR 0185 Lane A

```bash
python3 -m compiler.staqex run --seed 0 \
  examples/basics/B18_finiteize/finiteize_surface.sqx
```

```bash
python3 examples/host/mc_finite_inject_demo.py
```
