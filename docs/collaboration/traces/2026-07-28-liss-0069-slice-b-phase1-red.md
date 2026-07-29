# Trace: LISS-0069 Slice B Phase 1 Red

- Date: 2026-07-28
- Task: Failing migrator golden tests
- Agent: Cursor (Auto)
- Phase: Feature Path / Phase 1 Red (Slice B)
- Branch: `feature/liss-0069-slice-b-red`

## Plan approval

- Adjudicator: “承認” (2026-07-28)
- PR #71 (plan) merged
- Green not authorized until Red review

## Delivered

- `tests/fixtures/migration/v0.1/*.staqex` and `v1/*.staqex` (6 pairs)
- `tests/test_unicode_math_migrator_red.py`

## Red evidence

```text
python3 tests/test_unicode_math_migrator_red.py
→ 6 RED (ModuleNotFoundError: compiler.staqex.migrate_unicode_math)
```

## Next safe action

Adjudicator Red review → Phase 2 Green.
