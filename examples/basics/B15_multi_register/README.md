# B15 — Multi-register Basics

Introduces declarative `system` shapes, `RegisterSet` acting space, and
register-qualified sites (`data[0]`, `ancilla[0]`) per LISS-0067 / ADR 0105.
Provider physical routing is **out of scope** (see Applied [A08](../../applied/A08_entangled_compute_ancilla/)
for a longer narrative).

## Run

```bash
python3 -m compiler.staqex check examples/basics/B15_multi_register/main_multi_register.sqx
python3 -m compiler.staqex run examples/basics/B15_multi_register/main_multi_register.sqx --seed 0
```
