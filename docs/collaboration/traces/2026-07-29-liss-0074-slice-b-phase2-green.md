# Trace: LISS-0074 Slice B Phase 2 Green + Phase 3 Refactor

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0074 |
| Slice | B — ket/bra label vs local dimension |
| Phase | phase-2-green + phase-3-refactor |
| Branch | `feature/liss-0074-slice-b-red` |

## [DESIGN CHECK]

- Scope: numeric ket/bra labels on `State<Qutrit>` / `State<Qudit<D>>` must
  satisfy `0 ≤ k < D`; out-of-range → `LOCAL_DIMENSION_TYPE_ERROR`; alone ket
  unchanged. No acting-space (C), SV (D), backend (E).
- Refactor: helpers stay next to Slice A surface validation; no further
  structural split needed for this small Green.
- Verification: `tests/test_qudit_slice_b_red.py` PASS; Slice A regression PASS.

## Delivered

- `compiler/qpex/typecheck.py` — `_local_dim_of_state_carrier`,
  `_check_ket_bra_local_dimension` on typed StateBind

## Verification

- `python3 tests/test_qudit_slice_b_red.py` PASS
- `python3 tests/test_qudit_slice_a_red.py` PASS

### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: 宣言された局所次元に対する ket/bra
  数値ラベルの基数検査を型検査に入れ、範囲外を fail-closed にした。

### 残存リスク・検証の溝 (Verification Gap)
- Acting-space / Operator / tensor（Slice C）は未着手。
- SV / backend（D/E）は未着手。
- 非数値ラベルは Slice B 外。

## Next safe action

Adjudicator Slice B completion → PR / merge; Slice C plan intake.
