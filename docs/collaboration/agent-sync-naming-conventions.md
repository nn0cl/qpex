# Agent sync addendum: naming conventions

Date: 2026-07-22. Append to `agent-sync-staqex-baseline.md` read order.

## Lock (ADR 0023)

Canonical: `docs/style-guide/naming-conventions.md`.

| Role | Case |
|------|------|
| `State` / superposition | `snake_case` / single lowercase (`psi`, `x`) |
| Classical constants | `ALL_CAPS` (`DT`) |
| `system` / `trait` / types | `PascalCase` |
| Functions | `snake_case` |
| Ancilla locals | leading `_name` (style; Trace-Out GC still by liveness) |

## Hold

No styler / linter implementation until tooling unseal. Prefer these names in
all new normative examples.
