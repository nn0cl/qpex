# Agent sync addendum: P1 locks (ADR 0026)

Date: 2026-07-23.

| Item | Lock |
|------|------|
| Function keyword | `fun` only — `fn` abolished |
| Fallible type | `Result<T, E>` |
| `project` $Z=0$ | → `Vacuum` (never throw) |
| Packages | Required for `class` / `interface` / top-level `fun` |

Cheat sheet: `docs/collaboration/spelling-cheat-sheet.md`.
