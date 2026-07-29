# Trace: LISS-0080 Slice A Phase 2 Green + Phase 3 Refactor

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0080 |
| Slice | A — immutable HIR DTO + build API |
| Phase | phase-2-green + phase-3-refactor |
| Branch | `feature/liss-0080-slice-a-red` |

## [DESIGN CHECK]

- Scope: add `compiler/qpex/hir.py` with frozen `HirModule` and
  `build_hir(TypeChecker)` copying `env` / `typed` into `MappingProxyType`.
  No evaluator/pipeline rewire; no phase/effects/provenance (B–D).
- Specs: Slice A Red approval (“承認”).
- Verification: `tests/test_hir_slice_a_red.py` PASS.

## Delivered

- `compiler/qpex/hir.py` — `HirModule`, `build_hir`

## Verification

- `python3 tests/test_hir_slice_a_red.py` PASS

### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: TypeChecker から不変 HIR ビュー
  （symbols + typed）を切り出し、後続の phase/effects/線形解析の土台にした。

### 残存リスク・検証の溝 (Verification Gap)
- Slice A は DTO/API のみ。pipeline はまだ HIR を保持しない。
- phase / effects / provenance は B–D。線形解析は LISS-0075。

## Next safe action

Adjudicator Slice A complete → PR merge → Slice B plan.
