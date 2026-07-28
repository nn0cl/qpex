# Trace: LISS-0069 Slice B Phase 2 Green

- Date: 2026-07-28
- Task: Implement `migrate_unicode_math_source`
- Agent: Cursor (Auto)
- Phase: Feature Path / Phase 2 Green (Slice B)
- Branch: `feature/liss-0069-slice-b-red`

## Implementation

- `compiler/qpex/migrate_unicode_math.py`
  - R-KET: `|label>` → `|label⟩` (not `|>`)
  - R-TENSOR: `*|*` → `⊗`
  - R-ADJ-SIMPLE: `adjoint(Ident)` → `Ident†`
  - Comments / strings copied verbatim; idempotent on Unicode input

## Verification

- `python3 tests/test_unicode_math_migrator_red.py` — PASS
- `python3 tests/test_unicode_math_source_red.py` — PASS
- `python3 tests/spec_verification/run_all.py` — **160/160 PASS**

## Not in this Green

- CLI `qpex migrate` (Slice C)
- Examples tree bulk rewrite
- Complex `adjoint(...)` peel
- Phase 3 Refactor

## Next safe action

Phase 3 Refactor (optional) or Slice C plan.
