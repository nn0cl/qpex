# Agent sync addendum: P1 locks (ADR 0026)

Date: 2026-07-23.

| Item | Lock |
|------|------|
| Function keyword | `fn` only — `fun` retired (ADR 0066) |
| Fallible type | `Result<T, E>` |
| `project` $Z=0$ | → `Vacuum` (never throw) |
| Packages | Required for `class` / `interface` / top-level `fn` |

Cheat sheet: `docs/collaboration/spelling-cheat-sheet.md`.
