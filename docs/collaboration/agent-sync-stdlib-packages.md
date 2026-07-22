# Agent sync addendum: stdlib packages (ADR 0031)

Date: 2026-07-23.

## Lock

```text
qpex.math / qpex.io / qpex.state / qpex.collection / qpex.debug
```

- `Math.sin: State<Float> → State<Float>` via pointwise `map` (not scalar Math).
- `coin` / `dirac` ↔ `qpex.state.Distribution`.
- I/O / inspect per ADR 0029–0030.

Canonical: `docs/architecture/qpex-stdlib-packages.md`.
