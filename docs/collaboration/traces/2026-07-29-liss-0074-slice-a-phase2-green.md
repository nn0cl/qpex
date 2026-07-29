# Trace: LISS-0074 Slice A Phase 2 Green + Phase 3 Refactor

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0074 |
| Slice | A — qutrit/qudit type surface |
| Phase | phase-2-green + phase-3-refactor |
| Branch | `feature/liss-0074-slice-a-red` |

## [DESIGN CHECK]

- Scope: validate `Qutrit`/`Qudit<D>`/registers; hard `LOCAL_DIMENSION_TYPE_ERROR`;
  EBNF; register env binding. No label checks (B).
- Refactor: `_validate_local_dimension_surface` + helpers.
- Verification: `tests/test_qudit_slice_a_red.py` PASS.

## Delivered

- `compiler/qpex/typecheck.py` — local-dimension surface validation
- `compiler/qpex/pipeline.py` — hard code registration
- `docs/specs/grammar/qpex.ebnf` — qutrit/qudit productions

## Verification

- `python3 tests/test_qudit_slice_a_red.py` PASS

### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: qutrit/qudit の型レベル形状を検証し、不正な
  `D`/`N`/arity を `LOCAL_DIMENSION_TYPE_ERROR` で fail-closed にした。

### 残存リスク・検証の溝 (Verification Gap)
- ラベル基数検査（Slice B）は未着手 — `|3⟩` on `Qutrit` はまだ通る可能性。
- Acting-space / SV（C/D）は未着手。

## Next safe action

Adjudicator Slice A completion → PR / merge; Slice B plan intake.
