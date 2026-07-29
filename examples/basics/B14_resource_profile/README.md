# B14 — Resource profile

Teaches the Host-side `qpex.toml` resource manifest and simulator budget check
(LISS-0062 / LISS-0063 / ADR 0100). The Kernel does not read project files;
the Python helper loads the profile and passes an immutable DTO to `run`.

## Run (Kernel only)

```bash
python3 -m compiler.staqex run examples/basics/B14_resource_profile/main_resource_profile.qpex --seed 0
```

## Run with manifest + budget check

```bash
python3 examples/basics/B14_resource_profile/run_with_profile.py
```

The local `qpex.toml` sets simulator policy to `Warn` so an exceeded estimate
emits `SIMULATOR_RESOURCE_WARNING` while execution continues.
