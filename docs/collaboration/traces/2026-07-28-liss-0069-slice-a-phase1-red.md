# Trace: LISS-0069 Slice A Phase 1 Red

- Date: 2026-07-28
- Task: Failing tests for Unicode math dual-accept
- Agent: Cursor (Auto)
- Phase: Feature Path / Phase 1 Red
- Branch: `feature/liss-0069-unicode-math-source`

## Plan approval record

- Adjudicator: “承認” (2026-07-28)
- Slice A authorized for Phase 1 Red only (stop before Green)
- Bra–ket `inner` desugar deferred; lexer `BRA` remains in Red scope
- PR #68 (plan) merged to main

## Delivered

- `tests/test_unicode_math_source_red.py`

## Red evidence

```text
python3 tests/test_unicode_math_source_red.py
→ 8 RED (Unicode ket/tensor/dagger/bra/pipeline compile+lex)
→ 1 already-PASS (unterminated ASCII ket LEX_ERROR — regression guard)
```

Failure mode: compile/assertion failure and `LEX_ERROR` on `⟩` / `⊗` / `†` /
missing `BRA`/`DAGGER` kinds — **not** missing-module import errors.

## Explicitly not done

- Phase 2 Green lexer/parser changes
- Migrator / fixtures (Slice B)
- Pauli ASCII removal

## Next safe action

Adjudicator Red review → Phase 2 Green approval.
