# Agent sync addendum: no exceptions

Date: 2026-07-23. ADR **0025**.

## Lock

- No `throw` / `try` / `catch` / `Exception` in object language.
- Failure = orthogonal world-line (`Success` / `Error` via `when`).
- Drop failure arms with **`project`** (+ renorm), not exceptions.
- Fallible type: **`Result<T, E>`**. `$Z=0$` `project` → **`Vacuum`** (ADR 0026).

Canonical narrative: `docs/architecture/staqex-language-spec.md` §1.3.
