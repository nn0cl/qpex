# Trace: LISS-0069 Slice C Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0069 |
| Path | Feature Path |
| Phase | Phase 1 Red (Slice C) |
| Branch | `feature/liss-0069-slice-c-red` |
| Production code | **none** (tests + docs only) |

## [DESIGN CHECK]

- Scope: Failing CLI acceptance tests for `staqex migrate` per
  `staqex-unicode-math-migrate-cli.md`.
- Specs: approved Slice C companion; fixtures under
  `tests/fixtures/migration/`.
- Boundaries: tests call `compiler.staqex.cli.main`; no `cli.py` implementation.
- Ambiguities: none beyond approved plan.
- Routing: deterministic Red harness.
- Verification: `python3 tests/test_unicode_math_migrate_cli_red.py` → failures
  (missing `migrate` subcommand / remapped to `run`).

## Red evidence

- Preview / `--write` / `--check` / `-o` scenarios asserted against ket_basic goldens.
- Expected failure mode: `migrate` not registered; `main` allowlist remaps to `run`.

## Next safe action

Adjudicator Red approval → Phase 2 Green (`cmd_migrate` only).
