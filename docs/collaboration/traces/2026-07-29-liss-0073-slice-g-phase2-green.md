# Trace: LISS-0073 Slice G Phase 2 Green + Phase 3 Refactor

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0073 |
| Slice | G — formula→AST freeze + emit policy |
| Phase | phase-2-green + phase-3-refactor |
| Branch | `feature/liss-0073-slice-g-red` |

## [DESIGN CHECK]

- Scope: freeze §4 map; add formatter emit policy; Green proof suite; mark
  Issue complete. No new punctuation / runtime.
- Refactor: docs-only clarity (section titles).
- Verification: `tests/test_dirac_slice_g_red.py` PASS.

## Delivered

- `docs/specs/staqex-v1-dirac-algebra-ast-plan.md` — frozen §4 + emit policy
- `docs/issues/LISS-0073-…` — acceptance notes checked; status **complete**
- `docs/architecture/open-work-register.md` — closed A–G

## Verification

- `python3 tests/test_dirac_slice_g_red.py` PASS

### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: LISS-0073 の formula→AST 表を凍結し、
  formatter emit 方針を文書化し、証明スイートと acceptance notes で Issue を
  クローズ可能にした。

### 残存リスク・検証の溝 (Verification Gap)
- Formatter の単一 emit スペル選択は LISS-0072 フォロー（意図的 defer）。
- baseline 表（plan §2）は歴史的ギャップ表のまま — 凍結の正典は §4。

## Next safe action

Adjudicator confirm Issue complete → PR / merge.
