# Trace: LISS-0069 Slice C Phase 2 Green

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0069 |
| Path | Feature Path |
| Phase | Phase 2 Green (Slice C) |
| Branch | `feature/liss-0069-slice-c-green` |

## [DESIGN CHECK]

- Scope: Minimal `cmd_migrate` + subparser; wire
  `migrate_unicode_math_source` only; no rewrite-rule changes.
- Specs: `staqex-unicode-math-migrate-cli.md`; Red tests unchanged in assertions.
- Boundaries: CLI adapter I/O; spelling policy stays in Slice B library.
- Ambiguities: none.
- Verification:
  - `python3 tests/test_unicode_math_migrate_cli_red.py` → 5/5 PASS
  - `python3 tests/test_unicode_math_migrator_red.py` → PASS
  - SV 160/160 PASS

## Changes

- `compiler/staqex/cli.py`: `cmd_migrate`, `migrate` subparser, allowlist entry

## Next safe action

Adjudicator Green approval → Phase 3 Refactor (optional readability).
