# Agent sync addendum: stdlib packages (ADR 0031)

Date: 2026-07-23.

## Lock

```text
staqex.math / staqex.io / staqex.state / staqex.collection / staqex.debug
```

- `Math.sin: State<Float> → State<Float>` via pointwise `map` (not scalar Math).
- `coin` / `dirac` ↔ `staqex.state.Distribution`.
- I/O / inspect per ADR 0029–0030.

Canonical: `docs/architecture/staqex-stdlib-packages.md`.
